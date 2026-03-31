import os
import uuid
import json
from flask import Blueprint, request, jsonify, session, render_template
from database.database import SessionLocal
from database.schema.models import Publication, User

publications_bp = Blueprint('publications', __name__)

# Ruta de almacenamiento absoluta
STORAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../storage/images'))

@publications_bp.route('/create', methods=['POST'])
def create_publication():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Debes iniciar sesión para publicar"}), 401

    title = request.form.get('title')
    description = request.form.get('description')
    
    # Procesamos los JSON que vienen del frontend
    try:
        ingredients = json.loads(request.form.get('ingredients', '[]'))
        steps = json.loads(request.form.get('steps', '[]'))
        tags = json.loads(request.form.get('tags', '[]'))
    except Exception as e:
        print(f"Error parseando JSON en creación: {e}")
        return jsonify({"error": "Formato de datos incorrecto"}), 400

    db = SessionLocal()
    try:
        saved_filenames = []
        # Guardamos hasta 3 fotos enviadas desde el grid
        for i in range(3):
            file = request.files.get(f'file_{i}')
            if file and file.filename != '':
                ext = os.path.splitext(file.filename)[1]
                filename = f"pub_{user_id}_{uuid.uuid4().hex}{ext}"
                os.makedirs(STORAGE_FOLDER, exist_ok=True)
                file.save(os.path.join(STORAGE_FOLDER, filename))
                saved_filenames.append(f"/storage/images/{filename}")

        if not saved_filenames:
            saved_filenames.append("/storage/images/default_photo.jpg")

        # CREACIÓN CON REFRESH PARA ASEGURAR PERSISTENCIA
        new_pub = Publication(
            title=title,
            body=description,
            user_id=user_id,
            image_meta={
                "urls": saved_filenames,
                "ingredients": list(ingredients),
                "steps": list(steps),
                "tags": list(tags)
            },
            save_counter=0
        )
        
        db.add(new_pub)
        db.commit()
        db.refresh(new_pub) # Esto sincroniza el objeto con lo que se guardó en la DB
        
        return jsonify({"status": "success", "id": new_pub.id}), 201

    except Exception as e:
        db.rollback()
        print(f"Error en DB al crear: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@publications_bp.route('/all', methods=['GET'])
def all_publications():
    db = SessionLocal()
    try:
        pubs = db.query(Publication).all()
        result = []
        for p in pubs:
            meta = p.image_meta if isinstance(p.image_meta, dict) else {}
            result.append({
                "id": p.id,
                "title": p.title,
                "author": p.author.username if p.author else "Anónimo",
                "image": meta.get("urls", ["/storage/images/default_photo.jpg"])[0],
                "tags": meta.get("tags", []),
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
        
        meta = pub.image_meta if isinstance(pub.image_meta, dict) else {}
        return jsonify({
            "id": pub.id,
            "title": pub.title,
            "description": pub.body,
            "author": pub.author.username if pub.author else "Anónimo",
            "images": meta.get("urls", []),
            "ingredients": meta.get("ingredients", []),
            "steps": meta.get("steps", []),
            "tags": meta.get("tags", [])
        })
    finally:
        db.close()

@publications_bp.route('/view/<int:pub_id>')
def publication_view(pub_id):
    return render_template("recipe_detail.html")