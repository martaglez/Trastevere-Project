from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database.database import SessionLocal
from database.schema.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        db = SessionLocal()
        # 1. Buscamos al usuario por email en el Docker
        user = db.query(User).filter(User.email == email).first()
        db.close()

        # 2. Comprobamos si el usuario existe y si la contraseña (encriptada) coincide
        if user and check_password_hash(user.password_hash, password):
            # 3. GUARDAMOS LA SESIÓN: Esto es lo que nos permite saber quién eres en otras páginas
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({"message": "Login correcto", "redirect": "/"}), 200
        else:
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        want_premium = data.get('wantPremium', False)
        dni=data.get('dni')

        db = SessionLocal()
        # Comprobar si ya existe
        if db.query(User).filter(User.email == email).first():
            db.close()
            return jsonify({"error": "El email ya está registrado"}), 400

        # Crear nuevo usuario con contraseña encriptada
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_premium=want_premium # ¡Guardamos si es premium!
        )
        db.add(new_user)
        db.commit()
        db.close()
        
        return jsonify({"message": "Usuario creado con éxito"}), 201
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    # 4. LIMPIAMOS LA SESIÓN: Así el navegador olvida quién eres
    session.clear()
    return redirect('/')