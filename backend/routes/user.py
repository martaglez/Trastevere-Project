from flask import Blueprint, request, jsonify
import os
from flask import current_app

user_bp = Blueprint('user', __name__)

user_data = {
    "id": 1,
    "name": "Marta G",
    "email": "marta@example.com",
    "subscription": "basic",
    "phone": "666123456",
    "dni": "12345678A",
    "profile_pic": "foto.jpg"
}

@user_bp.route('/profile', methods=['GET'])
def profile():
    return jsonify(user_data)

@user_bp.route('/update', methods=['POST'])
def update_profile():
    data = request.json
    for key in ["name", "email", "phone", "dni", "profile_pic"]:
        if key in data:
            user_data[key] = data[key]
    return jsonify({"message": "Perfil actualizado", "user": user_data})

@user_bp.route('/about', methods=['GET'])
def about():
    return jsonify({
        "version": "1.0-beta",
        "build": "2026-03-23",
        "authors": "Equipo Trastevere"
    })


UPLOAD_FOLDER = 'static'

@user_bp.route('/upload_pic', methods=['POST'])
def upload_pic():
    if 'profile_pic' not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files['profile_pic']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # nombre simple (puedes mejorarlo luego)
    filename = file.filename

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # guardar en el "usuario"
    user_data["profile_pic"] = filename

    return jsonify({"filename": filename})