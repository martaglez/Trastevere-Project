import sys
import os

# 1. Configuración de rutas (Esto tiene que ir arriba del todo)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# 2. Imports de Flask y extensiones
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# 3. Imports de tus Blueprints (TODOS con el prefijo backend.)
from backend.routes.home import home_bp
from backend.routes.user import user_bp
from backend.routes.tables import tables_bp
from backend.routes.publications import publications_bp
from backend.routes.premium import premium_bp
from backend.routes.auth import auth_bp

# 4. Imports de la Base de Datos
from database.database import SessionLocal
from database.schema.models import User, Publication, Comment
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Le decimos a Flask que busque los HTML en la carpeta 'frontend' que está un nivel arriba
app = Flask(__name__, template_folder='../frontend/pages', static_folder='../frontend/static')

# Blueprints
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(tables_bp, url_prefix='/tables')
app.register_blueprint(publications_bp, url_prefix='/publications')
app.register_blueprint(premium_bp, url_prefix='/premium')
app.register_blueprint(auth_bp, url_prefix='/auth')

# --- LÓGICA DE BACKEND PARA MAIN ---

def home_back():
    """
    Función de Back: Extrae las últimas 30 publicaciones de la DB 
    y las convierte en un objeto que el Frontend entienda.
    """
    db = SessionLocal()
    try:
        # Consultamos las publicaciones y sus autores (usando la relación 'author')
        publications_db = db.query(Publication).order_by(func.random()).limit(30).all()

        feed = []
        for pub in publications_db:
            # Lógica para la imagen: si image_meta es un dict con la URL, la sacamos
            # Si vuestro image_meta es simple, ajustamos esto en el Bug Fixing
            img_url = "/static/assets/placeholder.png"
            if pub.image_meta and isinstance(pub.image_meta, dict):
                img_url = pub.image_meta.get("url", img_url)

            feed.append({
                "id": pub.id,
                "title": pub.title,
                "description": pub.body, # En models.py se llama 'body'
                "author_name": pub.author.username if pub.author else "Anónimo",
                "image": img_url,
                "saves": pub.save_counter
            })
        
        return {"publications": feed}
    
    except Exception as e:
        print(f"Error en home_back: {e}")
        return {"publications": []}
    finally:
        db.close()

# Esta es la lógica de FRONT para la API (La que usa tu JS):
@app.route('/home/feed')
def get_home_feed():
    data = home_back()
    return jsonify(data["publications"]) # <-- Devolvemos solo la lista de platos

# Principal page
@app.route('/')
def home():
    return render_template('home.html')

# Routes HTML 

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)