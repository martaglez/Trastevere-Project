from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash
from database.models import User
from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    return jsonify({
        "message": "Login correcto",
        "user_id": user.id,
        "username": user.username,
        "subscription_type": user.subscription_type
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    photo = data.get('photo')

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        subscription_type="basic",
        phone = phone,
        photo = photo
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Usuario creado",
        "user_id": new_user.id,
        "subscription_type": new_user.subscription_type
    }), 201

@app.route('/profile')
def profile():
    user = User.query.first()   # provisional
    return render_template('profile.html', user=user)

