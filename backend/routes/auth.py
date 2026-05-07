import os
import secrets
from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database.database import SessionLocal
from database.schema.models import User

auth_bp = Blueprint('auth', __name__)

# Token store en memoria (reset + delete)
_tokens: dict = {}

def _make_token(user_id: int, token_type: str) -> str:
    token = secrets.token_urlsafe(32)
    _tokens[token] = {
        'user_id': user_id,
        'expires': datetime.now(timezone.utc) + timedelta(hours=1),
        'type':    token_type,
    }
    return token

def _use_token(token: str, token_type: str):
    entry = _tokens.get(token)
    if not entry: return None
    if entry['type'] != token_type: return None
    if datetime.now(timezone.utc) > entry['expires']:
        _tokens.pop(token, None); return None
    _tokens.pop(token, None)
    return entry['user_id']


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
            db.refresh(new_user)
            session['user_id'] = new_user.id

            # Email de bienvenida (no bloqueante)
            try:
                from backend.routes.email_service import send_welcome_email
                lang = data.get('lang', 'es')
                send_welcome_email(email, username, lang)
            except Exception as mail_err:
                print(f"[email] Welcome email failed: {mail_err}")

            return jsonify({"message": "Usuario creado con éxito", "id": new_user.id}), 201
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

# ── FORGOT PASSWORD ──────────────────────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = (request.json or {}).get('email', '').strip()
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
        finally:
            db.close()
        if user:
            token = _make_token(user.id, 'reset')
            try:
                from backend.routes.email_service import send_reset_email
                lang = (request.json or {}).get('lang', 'es')
                send_reset_email(email, user.username, token, lang)
            except Exception as e:
                print(f"[email] Reset email failed: {e}")
        return jsonify({"message": "Si existe esa cuenta recibirás un email."}), 200
    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = (request.json or {}).get('password', '').strip()
        if len(new_password) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
        user_id = _use_token(token, 'reset')
        if not user_id:
            return jsonify({"error": "El enlace no es válido o ha expirado"}), 400
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.password_hash = generate_password_hash(new_password)
                db.commit()
            return jsonify({"message": "Contraseña actualizada correctamente"}), 200
        except Exception as e:
            db.rollback(); return jsonify({"error": str(e)}), 500
        finally:
            db.close()
    entry = _tokens.get(token)
    valid = bool(entry and entry['type'] == 'reset' and datetime.now(timezone.utc) <= entry['expires'])
    return render_template('reset_password.html', token=token, valid=valid)


# ── DELETE ACCOUNT ────────────────────────────────────────────────────────────
@auth_bp.route('/request-delete', methods=['POST'])
def request_delete():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No has iniciado sesión"}), 401
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        token = _make_token(user_id, 'delete')
        try:
            from backend.routes.email_service import send_delete_email
            lang = (request.json or {}).get('lang', 'es')
            send_delete_email(user.email, user.username, token, lang)
        except Exception as e:
            print(f"[email] Delete email failed: {e}")
        return jsonify({"message": "Te hemos enviado un email de confirmación."}), 200
    finally:
        db.close()


@auth_bp.route('/confirm-delete/<token>')
def confirm_delete(token):
    user_id = _use_token(token, 'delete')
    if not user_id:
        return render_template('account_deleted.html', success=False)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user); db.commit()
        session.clear()
        return render_template('account_deleted.html', success=True)
    except Exception as e:
        db.rollback(); return render_template('account_deleted.html', success=False)
    finally:
        db.close()