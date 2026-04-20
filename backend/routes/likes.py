from flask import Blueprint, jsonify, session
from database.database import SessionLocal
from database.schema.models import Like, Publication

likes_bp = Blueprint('likes', __name__)


@likes_bp.route('/<int:pub_id>/toggle', methods=['POST'])
def toggle_like(pub_id):
    """Dar o quitar like a una publicación. Devuelve el nuevo estado y el contador."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Debes iniciar sesión para dar like'}), 401

    db = SessionLocal()
    try:
        existing = db.query(Like).filter(
            Like.user_id == user_id,
            Like.publication_id == pub_id
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            liked = False
        else:
            db.add(Like(user_id=user_id, publication_id=pub_id))
            db.commit()
            liked = True

        count = db.query(Like).filter(Like.publication_id == pub_id).count()
        return jsonify({'liked': liked, 'count': count})

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@likes_bp.route('/<int:pub_id>/status', methods=['GET'])
def like_status(pub_id):
    """Devuelve si el usuario actual ha dado like y el total de likes."""
    user_id = session.get('user_id')
    db = SessionLocal()
    try:
        count = db.query(Like).filter(Like.publication_id == pub_id).count()
        liked = False
        if user_id:
            liked = db.query(Like).filter(
                Like.user_id == user_id,
                Like.publication_id == pub_id
            ).first() is not None
        return jsonify({'liked': liked, 'count': count})
    finally:
        db.close()


@likes_bp.route('/batch', methods=['POST'])
def batch_like_status():
    """Recibe una lista de pub_ids y devuelve likes y estado para cada uno."""
    from flask import request
    user_id = session.get('user_id')
    pub_ids = request.json.get('ids', [])
    if not pub_ids:
        return jsonify({})

    db = SessionLocal()
    try:
        # Contar likes por publicación
        from sqlalchemy import func
        counts = dict(
            db.query(Like.publication_id, func.count(Like.user_id))
            .filter(Like.publication_id.in_(pub_ids))
            .group_by(Like.publication_id)
            .all()
        )

        # Likes del usuario actual
        user_liked = set()
        if user_id:
            rows = db.query(Like.publication_id).filter(
                Like.user_id == user_id,
                Like.publication_id.in_(pub_ids)
            ).all()
            user_liked = {r[0] for r in rows}

        result = {}
        for pid in pub_ids:
            result[str(pid)] = {
                'count': counts.get(pid, 0),
                'liked': pid in user_liked
            }
        return jsonify(result)
    finally:
        db.close()
