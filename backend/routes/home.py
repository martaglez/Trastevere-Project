from flask import Blueprint, render_template, jsonify
from database.database import SessionLocal
from database.schema.models import Publication
from sqlalchemy.sql import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/feed', methods=['GET'])
def get_feed():
    """
    Extrae las publicaciones de la base de datos de Docker 
    en lugar de una lista estática.
    """
    db = SessionLocal()
    try:
        # Consultamos las publicaciones de forma aleatoria (o por fecha si prefieres)
        publications_db = db.query(Publication).order_by(func.random()).limit(30).all()

        feed = []
        for pub in publications_db:
            # Sacamos la primera imagen del JSON image_meta
            # Si no hay imágenes, ponemos el placeholder
            images = pub.image_meta.get("urls", []) if pub.image_meta else []
            img_url = images[0] if images else "/static/assets/placeholder.png"

            feed.append({
                "id": pub.id,
                "title": pub.title,
                "description": pub.body,
                "author": pub.author.username if pub.author else "Anónimo",
                "image": img_url,
                "tags": [] # Puedes ampliar esto luego si guardas tags en la DB
            })
        
        return jsonify(feed)
    
    except Exception as e:
        print(f"Error en get_feed: {e}")
        return jsonify([])
    finally:
        db.close()