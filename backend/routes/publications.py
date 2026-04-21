import os
import json
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify, session, render_template
from database.database import SessionLocal
from database.schema.models import Publication, User

publications_bp = Blueprint('publications', __name__)

# Configurar Cloudinary con variables de entorno
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure     = True
)

def upload_to_cloudinary(file, folder="trastevere/recipes"):
    """Sube un archivo a Cloudinary y devuelve la URL segura."""
    result = cloudinary.uploader.upload(file, folder=folder, resource_type="image")
    return result["secure_url"]


@publications_bp.route('/create', methods=['POST'])
def create_publication():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Debes iniciar sesión para publicar"}), 401

    title       = request.form.get('title')
    description = request.form.get('description')

    try:
        ingredients = json.loads(request.form.get('ingredients', '[]'))
        steps       = json.loads(request.form.get('steps', '[]'))
        tags        = json.loads(request.form.get('tags', '[]'))
    except Exception as e:
        return jsonify({"error": "Formato de datos incorrecto"}), 400

    db = SessionLocal()
    try:
        saved_urls = []
        for i in range(3):
            file = request.files.get(f'file_{i}')
            if file and file.filename != '':
                url = upload_to_cloudinary(file)
                saved_urls.append(url)

        if not saved_urls:
            saved_urls.append("/storage/images/default_photo.jpg")

        new_pub = Publication(
            title      = title,
            body       = description,
            user_id    = user_id,
            image_meta = {
                "urls":        saved_urls,
                "ingredients": list(ingredients),
                "steps":       list(steps),
                "tags":        list(tags)
            },
            save_counter = 0
        )
        db.add(new_pub)
        db.commit()
        db.refresh(new_pub)
        return jsonify({"status": "success", "id": new_pub.id}), 201

    except Exception as e:
        db.rollback()
        print(f"Error al crear publicación: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@publications_bp.route('/all', methods=['GET'])
def all_publications():
    db = SessionLocal()
    try:
        pubs   = db.query(Publication).all()
        result = []
        for p in pubs:
            meta = p.image_meta if isinstance(p.image_meta, dict) else {}
            result.append({
                "id":          p.id,
                "title":       p.title,
                "author":      p.author.username if p.author else "Anónimo",
                "image":       meta.get("urls", ["/storage/images/default_photo.jpg"])[0],
                "tags":        meta.get("tags", []),
                "ingredients": meta.get("ingredients", [])
            })
        return jsonify(result)
    finally:
        db.close()


@publications_bp.route('/<int:pub_id>', methods=['GET'])
def publication_detail(pub_id):
    db = SessionLocal()
    try:
        pub = db.query(Publication).filter(Publication.id == pub_id).first()
        if not pub:
            return jsonify({"error": "No encontrada"}), 404

        meta = pub.image_meta or {}
        if isinstance(meta, str):
            try:    meta = json.loads(meta)
            except: meta = {}

        from database.schema.models import Like
        from flask import session as _sess
        like_count = db.query(Like).filter(Like.publication_id == pub_id).count()
        uid        = _sess.get('user_id')
        user_liked = bool(uid and db.query(Like).filter(
            Like.user_id == uid, Like.publication_id == pub_id).first())

        return jsonify({
            "id":          pub.id,
            "title":       pub.title,
            "description": pub.body,
            "author":      pub.author.username if pub.author else "Anónimo",
            "author_id":   pub.user_id,
            "images":      meta.get("urls", []),
            "ingredients": meta.get("ingredients", []),
            "steps":       meta.get("steps", []),
            "tags":        meta.get("tags", []),
            "like_count":  like_count,
            "user_liked":  user_liked
        })
    finally:
        db.close()


@publications_bp.route('/view/<int:pub_id>')
def publication_view(pub_id):
    return render_template("recipe_detail.html")