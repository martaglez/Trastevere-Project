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
        dni = data.get('dni')
        phone_number = data.get('phone_number')
        want_premium = data.get('wantPremium', False)
        card_number = data.get('card_number') # Nuevo campo

        db = SessionLocal()
        try:
            # Comprobar si ya existe el email
            if db.query(User).filter(User.email == email).first():
                return jsonify({"error": "El email ya está registrado"}), 400

            # Crear nuevo usuario con la lógica de tarjeta
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                dni=dni,
                phone_number=phone_number,
                is_premium=want_premium,
                card_number=card_number if want_premium else None # Solo guardamos tarjeta si es premium
            )
            db.add(new_user)
            db.commit()
            return jsonify({"message": "Usuario creado con éxito"}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            db.close()
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    # 4. LIMPIAMOS LA SESIÓN: Así el navegador olvida quién eres
    session.clear()
    return redirect('/')