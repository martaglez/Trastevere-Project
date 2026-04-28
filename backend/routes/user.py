import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify, session
from database.database import SessionLocal
from database.schema.models import User

user_bp = Blueprint('user', __name__)

# Configurar Cloudinary
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure     = True
)


@user_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No has iniciado sesión"}), 401

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        plan_name   = "PREMIUM" if user.is_premium else "BASIC"
        profile_pic = user.profile_pic or "/storage/images/default_user.jpg"

        # Si es una ruta local antigua (no URL de Cloudinary), la dejamos tal cual
        if profile_pic and not profile_pic.startswith('/') and not profile_pic.startswith('http'):
            profile_pic = f"/storage/images/{profile_pic}"

        return jsonify({
            "id":           user.id,
            "username":     user.username,
            "email":        user.email,
            "is_premium":   user.is_premium,
            "plan":         plan_name,
            "phone_number": user.phone_number or "",
            "dni":          user.dni or "",
            "profile_pic":  profile_pic
        })
    finally:
        db.close()


@user_bp.route('/upload_pic', methods=['POST'])
def upload_pic():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    file = request.files.get('profile_pic')
    if not file:
        return jsonify({"error": "No hay archivo"}), 400

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Subir a Cloudinary en la carpeta de avatares
        result  = cloudinary.uploader.upload(
            file,
            folder          = "trastevere/avatars",
            resource_type   = "image",
            public_id       = f"user_{user_id}",   # sobreescribe la anterior automáticamente
            overwrite       = True,
            transformation  = [{"width": 400, "height": 400, "crop": "fill", "gravity": "face"}]
        )
        url = result["secure_url"]

        user.profile_pic = url
        db.commit()

        return jsonify({"status": "success", "url": url})
    except Exception as e:
        db.rollback()
        print(f"Error subiendo foto: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route('/update', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    db   = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'dni' in data:
            user.dni = data['dni']

        db.commit()
        db.refresh(user)
        return jsonify({"message": "Perfil actualizado con éxito"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route('/about', methods=['GET'])
def about():
    return jsonify({
        "version": "2.2.0",
        "build":   "2026-04-28",
        "authors": "CEU San Pablo & Trastevere Team"
    })