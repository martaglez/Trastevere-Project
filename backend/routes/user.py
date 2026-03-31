import os
import uuid
from flask import Blueprint, request, jsonify, session
from database.database import SessionLocal
from database.schema.models import User

user_bp = Blueprint('user', __name__)

STORAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../storage/images'))

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

        # Lógica de Plan y Foto Default
        plan_name = "PREMIUM" if user.is_premium else "BASIC"
        
        # Si no tiene foto, usamos la default de storage
        profile_pic = user.profile_pic if hasattr(user, 'profile_pic') and user.profile_pic else "/storage/images/default_user.jpg"
        
        # Aseguramos que la ruta empiece por / si es una imagen subida
        if profile_pic and not profile_pic.startswith('/') and not profile_pic.startswith('http'):
            profile_pic = f"/storage/images/{profile_pic}"

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_premium": user.is_premium,
            "plan": plan_name,
            "phone_number": user.phone_number or "",
            "dni": user.dni or "",
            "profile_pic": profile_pic
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
        if not user: return jsonify({"error": "Usuario no encontrado"}), 404

        # 1. Guardar archivo físico
        ext = os.path.splitext(file.filename)[1]
        filename = f"user_{user_id}_{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(STORAGE_FOLDER, filename)
        file.save(save_path)
        
        # 2. LA CLAVE: Guardar la ruta en la base de datos
        # Guardamos la URL pública que entiende el navegador
        db_path = f"/storage/images/{filename}"
        user.profile_pic = db_path 
        
        db.commit() # Confirmamos cambios en la DB
        
        return jsonify({"status": "success", "url": db_path})
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
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'dni' in data:
            user.dni = data['dni']

        db.commit()
        db.refresh(user) # Confirmación de escritura
        return jsonify({"message": "Perfil actualizado con éxito"})
    except Exception as e:
        db.rollback()
        print(f"Error en /update: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@user_bp.route('/about', methods=['GET'])
def about():
    return jsonify({
        "version": "1.0.4",
        "build": "2026-03-30",
        "authors": "Hugo & Trastevere Team"
    })