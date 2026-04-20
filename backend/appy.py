import sys
import os
import json
import random as _random

# 1. CONFIGURACIÓN DE RUTAS SISTEMA
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# 2. IMPORTS DE FLASK
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect
from sqlalchemy.sql import func

# 3. IMPORTS DE BLUEPRINTS
from backend.routes.home import home_bp
from backend.routes.user import user_bp
from backend.routes.tables import tables_bp
from backend.routes.publications import publications_bp
from backend.routes.premium import premium_bp
from backend.routes.auth import auth_bp
from backend.routes.user_profile import user_profile_bp
from backend.routes.likes import likes_bp

# 4. IMPORTS DE MODELOS Y BASE DE DATOS
from database.database import SessionLocal, engine, Base
from database.schema.models import User, Publication, Collection as Table, UserRating
from database.schema import models

# --- CONFIGURACIÓN DE LA APP ---
app = Flask(__name__,
            template_folder='../frontend/pages',
            static_folder='../frontend/static')

app.secret_key = 'jycpob-syrfoj-qinhU3'

# Registro de Blueprints
app.register_blueprint(home_bp,         url_prefix='/home')
app.register_blueprint(user_bp,         url_prefix='/user')
app.register_blueprint(tables_bp,       url_prefix='/tables')
app.register_blueprint(publications_bp, url_prefix='/publications')
app.register_blueprint(premium_bp,      url_prefix='/premium')
app.register_blueprint(auth_bp,         url_prefix='/auth')
app.register_blueprint(user_profile_bp, url_prefix='/profiles')
app.register_blueprint(likes_bp,        url_prefix='/likes')

# --- ALMACENAMIENTO ESTÁTICO ---
@app.route('/storage/images/<filename>')
def get_storage_image(filename):
    storage_dir = os.path.join(root_path, 'storage', 'images')
    return send_from_directory(storage_dir, filename)

# --- API ENDPOINTS ---
@app.route('/api/recipes/search')
def get_search_data():
    db = SessionLocal()
    try:
        publications_db = db.query(Publication).all()
        feed = []
        for pub in publications_db:
            meta = pub.image_meta
            if isinstance(meta, str):
                try:    meta = json.loads(meta)
                except: meta = {}
            elif meta is None:
                meta = {}

            tags        = meta.get("tags", [])
            ingredients = meta.get("ingredients", [])
            urls        = meta.get("urls", [])
            img_url     = urls[0] if (isinstance(urls, list) and len(urls) > 0) else "/storage/images/default_photo.jpg"

            feed.append({
                "id":          pub.id,
                "title":       pub.title,
                "author":      pub.author.username if pub.author else "Anónimo",
                "author_id":   pub.user_id,
                "image":       img_url,
                "description": pub.body or "",
                "tags":        tags,
                "ingredients": ingredients
            })
        return jsonify(feed)
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return jsonify([])
    finally:
        db.close()

@app.route('/home/feed')
def get_home_feed():
    return get_search_data()

@app.route('/api/recipes/random')
def get_random_recipe():
    """Devuelve una receta aleatoria para el botón dado."""
    db = SessionLocal()
    try:
        pubs = db.query(Publication).all()
        if not pubs:
            return jsonify({"error": "No hay recetas"}), 404
        pub = _random.choice(pubs)
        return jsonify({"id": pub.id, "title": pub.title})
    finally:
        db.close()

# --- RUTAS DE NAVEGACIÓN (HTML) ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/tables/view/<int:table_id>")
def table_detail_view(table_id):
    return render_template("table_detail.html")

@app.route("/profile")
def profile():
    """Ajustes privados del usuario (email, DNI, teléfono, foto)."""
    return render_template("profile.html")

@app.route("/my-profile")
def my_profile():
    """Redirige al perfil público del usuario logueado."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/auth/login')
    return redirect(f'/user/{user_id}')

@app.route("/user/<int:user_id>")
def public_profile_page(user_id):
    """Perfil público de cualquier usuario."""
    return render_template("public_profile.html")

# --- INICIALIZACIÓN ---
if __name__ == "__main__":
    storage_dir = os.path.join(root_path, 'storage', 'images')
    os.makedirs(storage_dir, exist_ok=True)
    print("Sincronizando base de datos con Docker...")
    Base.metadata.create_all(bind=engine)
    print(f"Servidor Trastevere activo en http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)