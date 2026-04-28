import os
import json
import base64
import hashlib
import hmac
from flask import Blueprint, jsonify, request, session, redirect, render_template_string
from database.database import SessionLocal
from database.schema.models import User

premium_bp = Blueprint('premium', __name__)

REDSYS_URL        = "https://sis-t.redsys.es:25443/sis/realizarPago"
MERCHANT_CODE     = os.environ.get("REDSYS_MERCHANT_CODE", "999008881")
MERCHANT_TERMINAL = os.environ.get("REDSYS_TERMINAL", "049")
MERCHANT_SECRET   = os.environ.get("REDSYS_SECRET", "sq7HjrUOBfKmC576ILgskD5srU870gJ7")
PREMIUM_AMOUNT    = "199"
CURRENCY          = "978"


def _encrypt_3des(key, data):
    try:
        from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
    except ImportError:
        from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
    from cryptography.hazmat.primitives.ciphers import Cipher, modes
    from cryptography.hazmat.backends import default_backend
    key_bytes  = base64.b64decode(key)
    data_bytes = data.encode('utf-8')
    pad_len    = (8 - len(data_bytes) % 8) % 8
    data_bytes = data_bytes + b'\x00' * pad_len
    cipher     = Cipher(TripleDES(key_bytes), modes.CBC(b'\x00' * 8), backend=default_backend())
    enc        = cipher.encryptor()
    return enc.update(data_bytes) + enc.finalize()

def _build_signature(order_id, params_b64):
    key_enc = _encrypt_3des(MERCHANT_SECRET, order_id)
    sig     = hmac.new(key_enc, params_b64.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(sig).decode('utf-8')

def _build_merchant_params(order_id, base_url):
    params = {
        "DS_MERCHANT_AMOUNT": PREMIUM_AMOUNT, "DS_MERCHANT_CURRENCY": CURRENCY,
        "DS_MERCHANT_ORDER": order_id, "DS_MERCHANT_MERCHANTCODE": MERCHANT_CODE,
        "DS_MERCHANT_TERMINAL": MERCHANT_TERMINAL, "DS_MERCHANT_TRANSACTIONTYPE": "0",
        "DS_MERCHANT_MERCHANTURL": f"{base_url}/premium/redsys-notify",
        "DS_MERCHANT_URLOK": f"{base_url}/premium/payment-ok",
        "DS_MERCHANT_URLKO": f"{base_url}/premium/payment-ko",
        "DS_MERCHANT_MERCHANTNAME": "Trastevere",
        "DS_MERCHANT_PRODUCTDESCRIPTION": "Plan Premium Trastevere",
    }
    return base64.b64encode(json.dumps(params, separators=(',',':')).encode()).decode()

@premium_bp.route('/pay', methods=['GET'])
def start_payment():
    user_id = session.get('user_id')
    if not user_id: return redirect('/auth/login')
    import time
    order_id   = f"{int(time.time()) % 10000000:07d}{user_id:03d}"
    base_url   = request.host_url.rstrip('/')
    params_b64 = _build_merchant_params(order_id, base_url)
    signature  = _build_signature(order_id, params_b64)
    html = f'''<!DOCTYPE html><html><body onload="document.getElementById('f').submit()">
<p style="font-family:sans-serif;text-align:center;margin-top:80px;">Redirigiendo al pago seguro...</p>
<form id="f" action="{REDSYS_URL}" method="POST">
    <input type="hidden" name="Ds_SignatureVersion" value="HMAC_SHA256_V1">
    <input type="hidden" name="Ds_MerchantParameters" value="{params_b64}">
    <input type="hidden" name="Ds_Signature" value="{signature}">
</form></body></html>'''
    return render_template_string(html)

@premium_bp.route('/redsys-notify', methods=['POST'])
def redsys_notify():
    try:
        params_b64 = request.form.get('Ds_MerchantParameters','')
        sig_recv   = request.form.get('Ds_Signature','')
        params     = json.loads(base64.b64decode(params_b64).decode())
        order_id   = params.get('Ds_Order','')
        resp_code  = int(params.get('Ds_Response','9999'))
        if sig_recv.replace('-','+').replace('_','/') != _build_signature(order_id, params_b64).replace('-','+').replace('_','/'):
            return "KO", 400
        if resp_code <= 99:
            user_id = int(order_id[-3:])
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user: user.is_premium = True; db.commit()
            finally: db.close()
            return "OK", 200
        return "KO", 200
    except Exception as e:
        print(f"Redsys error: {e}"); return "KO", 500

@premium_bp.route('/payment-ok')
def payment_ok():
    return render_template_string('''<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="3;url=/"><style>body{font-family:sans-serif;text-align:center;margin-top:100px;}</style>
</head><body><div style="font-size:4rem">✅</div>
<div style="font-size:1.2rem;color:#4caf82;margin:20px 0">¡Pago completado! Bienvenido a Premium 🎉</div>
<p>Redirigiendo...</p></body></html>''')

@premium_bp.route('/payment-ko')
def payment_ko():
    return render_template_string('''<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="3;url=/"><style>body{font-family:sans-serif;text-align:center;margin-top:100px;}</style>
</head><body><div style="font-size:4rem">❌</div>
<div style="font-size:1.2rem;color:#e05252;margin:20px 0">El pago no se ha podido completar.</div>
<p>Redirigiendo...</p></body></html>''')


def _get_user(db):
    """Devuelve el usuario de la sesión o None si no hay sesión."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


# ── Información de features premium ────────────────────────────────────────────
@premium_bp.route('/features', methods=['GET'])
def features():
    db = SessionLocal()
    try:
        # Receta semanal: la publicación con más saves (o la más reciente si no hay)
        from database.schema.models import Publication
        import json as _json
        weekly = db.query(Publication).order_by(Publication.save_counter.desc()).first()
        weekly_data = None
        if weekly:
            meta = weekly.image_meta or {}
            if isinstance(meta, str):
                try: meta = _json.loads(meta)
                except: meta = {}
            urls = meta.get('urls', [])
            weekly_data = {
                "id": weekly.id,
                "title": weekly.title,
                "image": urls[0] if urls else "/storage/images/default_photo.jpg"
            }
    finally:
        db.close()

    return jsonify({
        "weekly_recipe": weekly_data or {"id": 0, "title": "Próximamente", "image": "/storage/images/default_photo.jpg"},
        "coupons": [
            {"name": "10% Mercadona", "code": "TRAST-MER-2024"},
            {"name": "5€ El Corte Inglés", "code": "TRAST-ECI-0512"},
            {"name": "Envío gratis Amazon Fresh", "code": "TRAST-AMZ-FREE"},
        ],
        "themes": ["green", "dark"]
    })


# ── Cancelar suscripción premium ────────────────────────────────────────────────
@premium_bp.route('/cancel', methods=['POST'])
def cancel_premium():
    db = SessionLocal()
    try:
        user = _get_user(db)
        if not user:
            return jsonify({"error": "No has iniciado sesión"}), 401

        if not user.is_premium:
            return jsonify({"error": "No tienes una suscripción Premium activa"}), 400

        user.is_premium = False
        # Borramos la tarjeta al cancelar por seguridad
        user.card_number = None
        db.commit()

        return jsonify({"message": "Suscripción cancelada. Ahora eres usuario Basic."}), 200

    except Exception as e:
        db.rollback()
        print(f"Error cancelando premium: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ── Activar premium (upgrade desde Basic) ───────────────────────────────────────
@premium_bp.route('/upgrade', methods=['POST'])
def upgrade_to_premium():
    db = SessionLocal()
    try:
        user = _get_user(db)
        if not user:
            return jsonify({"error": "No has iniciado sesión"}), 401

        if user.is_premium:
            return jsonify({"error": "Ya tienes el plan Premium"}), 400

        data = request.json or {}
        card_number = data.get('card_number', '').strip()

        if not card_number or len(card_number) < 8:
            return jsonify({"error": "Número de tarjeta inválido"}), 400

        user.is_premium = True
        user.card_number = card_number
        db.commit()

        return jsonify({"message": "¡Bienvenido a Premium! Disfruta de todas las ventajas."}), 200

    except Exception as e:
        db.rollback()
        print(f"Error activando premium: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ── Cambiar método de pago ───────────────────────────────────────────────────────
@premium_bp.route('/update-payment', methods=['POST'])
def update_payment():
    db = SessionLocal()
    try:
        user = _get_user(db)
        if not user:
            return jsonify({"error": "No has iniciado sesión"}), 401

        if not user.is_premium:
            return jsonify({"error": "Solo los usuarios Premium pueden cambiar su método de pago"}), 403

        data = request.json or {}
        card_number = data.get('card_number', '').strip()

        if not card_number or len(card_number) < 8:
            return jsonify({"error": "Número de tarjeta inválido"}), 400

        user.card_number = card_number
        db.commit()

        return jsonify({"message": "Método de pago actualizado correctamente."}), 200

    except Exception as e:
        db.rollback()
        print(f"Error actualizando pago: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ── Estado de suscripción del usuario actual ────────────────────────────────────
@premium_bp.route('/status', methods=['GET'])
def subscription_status():
    db = SessionLocal()
    try:
        user = _get_user(db)
        if not user:
            return jsonify({"is_premium": False, "plan": "BASIC"}), 200

        # Enmascaramos la tarjeta: solo mostramos los últimos 4 dígitos
        card_hint = None
        if user.card_number and len(user.card_number) >= 4:
            card_hint = "•••• " + user.card_number[-4:]

        return jsonify({
            "is_premium": user.is_premium,
            "plan": "PREMIUM" if user.is_premium else "BASIC",
            "card_hint": card_hint
        }), 200

    finally:
        db.close()