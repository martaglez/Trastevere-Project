from flask import Blueprint, request, jsonify

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

