from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return jsonify({"message": "Login correcto", "user_id": 1}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return jsonify({"message": "Usuario creado", "user_id": 1}), 201

