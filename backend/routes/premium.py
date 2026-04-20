from flask import Blueprint, jsonify, request, session
from database.database import SessionLocal
from database.schema.models import User

premium_bp = Blueprint('premium', __name__)


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