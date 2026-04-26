import json
from flask import Blueprint, jsonify, request, session
from database.database import SessionLocal
from database.schema.models import User, Publication, Follow

user_profile_bp = Blueprint('user_profile', __name__)


def _pub_to_dict(pub):
    meta = pub.image_meta or {}
    if isinstance(meta, str):
        try: meta = json.loads(meta)
        except: meta = {}
    urls = meta.get('urls', [])
    return {
        'id':    pub.id,
        'title': pub.title,
        'image': urls[0] if urls else '/storage/images/default_photo.jpg',
        'tags':  meta.get('tags', []),
    }

def _pic(user):
    pic = user.profile_pic or '/storage/images/default_user.jpg'
    if pic and not pic.startswith('/') and not pic.startswith('http'):
        pic = f'/storage/images/{pic}'
    return pic


# ── Perfil público ──────────────────────────────────────────────────────────────
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
def public_profile(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        current_id = session.get('user_id')
        is_following = False
        if current_id and current_id != user_id:
            is_following = db.query(Follow).filter(
                Follow.follower_id == current_id,
                Follow.following_id == user_id
            ).first() is not None

        follower_count  = db.query(Follow).filter(Follow.following_id == user_id).count()
        following_count = db.query(Follow).filter(Follow.follower_id  == user_id).count()
        publications    = db.query(Publication).filter(
            Publication.user_id == user_id
        ).order_by(Publication.id.desc()).all()

        return jsonify({
            'id':              user.id,
            'username':        user.username,
            'profile_pic':     _pic(user),
            'stars':           round(float(user.stars or 0), 1),
            'bio':             getattr(user, 'bio', None) or '',
            'is_premium':      user.is_premium,
            'follower_count':  follower_count,
            'following_count': following_count,
            'pub_count':       len(publications),
            'is_following':    is_following,
            'is_own_profile':  current_id == user_id,
            'publications':    [_pub_to_dict(p) for p in publications],
        })
    finally:
        db.close()


# ── Seguir / dejar de seguir ────────────────────────────────────────────────────
@user_profile_bp.route('/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    current_id = session.get('user_id')
    if not current_id:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    if current_id == user_id:
        return jsonify({'error': 'No puedes seguirte a ti mismo'}), 400

    db = SessionLocal()
    try:
        existing = db.query(Follow).filter(
            Follow.follower_id  == current_id,
            Follow.following_id == user_id
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            action = 'unfollowed'
        else:
            db.add(Follow(follower_id=current_id, following_id=user_id))
            db.commit()
            action = 'followed'

        count = db.query(Follow).filter(Follow.following_id == user_id).count()
        return jsonify({'action': action, 'follower_count': count})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ── Buscar usuarios ─────────────────────────────────────────────────────────────
@user_profile_bp.route('/search', methods=['GET'])
def search_users():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.username.ilike(f'%{q}%')).limit(20).all()
        return jsonify([{
            'id':          u.id,
            'username':    u.username,
            'profile_pic': _pic(u),
            'is_premium':  u.is_premium,
            'stars':       round(float(u.stars or 0), 1),
        } for u in users])
    finally:
        db.close()

# ── Valorar usuario (1-5 estrellas) — una por usuario, modificable ─────────────
@user_profile_bp.route('/<int:user_id>/rate', methods=['POST'])
def rate_user(user_id):
    from flask import request
    from database.schema.models import UserRating
    from sqlalchemy import func as _func

    current_id = session.get('user_id')
    if not current_id:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    if current_id == user_id:
        return jsonify({'error': 'No puedes valorarte a ti mismo'}), 400

    try:
        stars = int(request.json.get('stars', 0))
    except (TypeError, ValueError):
        stars = 0
    if not (1 <= stars <= 5):
        return jsonify({'error': 'Valoración inválida (1-5)'}), 400

    db = SessionLocal()
    try:
        # Upsert: si ya existe una valoración del mismo usuario, la actualiza
        existing = db.query(UserRating).filter(
            UserRating.rater_id == current_id,
            UserRating.rated_id == user_id
        ).first()

        if existing:
            existing.stars = stars          # Actualizar valoración existente
        else:
            db.add(UserRating(rater_id=current_id, rated_id=user_id, stars=stars))

        db.commit()

        # Recalcular media real de todas las valoraciones
        avg = db.query(_func.avg(UserRating.stars)).filter(
            UserRating.rated_id == user_id
        ).scalar() or 0.0

        # Guardar la media en el campo stars del usuario
        target = db.query(User).filter(User.id == user_id).first()
        if target:
            target.stars = round(float(avg), 2)
            db.commit()

        # Devolver también si es nueva o actualizada
        action = 'updated' if existing else 'created'
        return jsonify({
            'stars':      round(float(avg), 2),
            'my_rating':  stars,
            'action':     action
        })

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ── Lista de seguidores ─────────────────────────────────────────────────────────
@user_profile_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    db = SessionLocal()
    try:
        follows = db.query(Follow).filter(Follow.following_id == user_id).all()
        result = []
        for f in follows:
            u = db.query(User).filter(User.id == f.follower_id).first()
            if u:
                result.append({
                    'id':          u.id,
                    'username':    u.username,
                    'profile_pic': _pic(u),
                    'is_premium':  u.is_premium,
                })
        return jsonify(result)
    finally:
        db.close()


# ── Lista de siguiendo ──────────────────────────────────────────────────────────
@user_profile_bp.route('/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    db = SessionLocal()
    try:
        follows = db.query(Follow).filter(Follow.follower_id == user_id).all()
        result = []
        for f in follows:
            u = db.query(User).filter(User.id == f.following_id).first()
            if u:
                result.append({
                    'id':          u.id,
                    'username':    u.username,
                    'profile_pic': _pic(u),
                    'is_premium':  u.is_premium,
                })
        return jsonify(result)
    finally:
        db.close()

# ── Obtener mi valoración de un usuario ────────────────────────────────────────
@user_profile_bp.route('/<int:user_id>/my-rating', methods=['GET'])
def get_my_rating(user_id):
    from database.schema.models import UserRating
    current_id = session.get('user_id')
    if not current_id:
        return jsonify({'my_rating': None})

    db = SessionLocal()
    try:
        row = db.query(UserRating).filter(
            UserRating.rater_id == current_id,
            UserRating.rated_id == user_id
        ).first()
        return jsonify({'my_rating': row.stars if row else None})
    finally:
        db.close()