import json
from flask import Blueprint, jsonify
from database.database import SessionLocal
from database.schema.models import Publication
from sqlalchemy.sql import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/feed', methods=['GET'])
def get_feed():
    db = SessionLocal()
    try:
        publications_db = db.query(Publication).order_by(func.random()).limit(30).all()
        feed = []
        for pub in publications_db:
            meta = pub.image_meta or {}
            if isinstance(meta, str):
                try:    meta = json.loads(meta)
                except: meta = {}

            urls        = meta.get("urls", [])
            img_url     = urls[0] if urls else "/storage/images/default_photo.jpg"
            tags        = meta.get("tags", [])
            ingredients = meta.get("ingredients", [])

            feed.append({
                "id":          pub.id,
                "title":       pub.title,
                "description": pub.body or "",
                "author":      pub.author.username if pub.author else "Anónimo",
                "author_id":   pub.user_id,
                "image":       img_url,
                "tags":        tags,
                "ingredients": ingredients
            })

        return jsonify(feed)

    except Exception as e:
        print(f"Error en get_feed: {e}")
        return jsonify([])
    finally:
        db.close()