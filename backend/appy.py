import sys
import os
import json

# 1. CONFIGURACIÓN DE RUTAS SISTEMA
# Asegura que Python localice los módulos de 'database' y 'backend' en el path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# 2. IMPORTS DE FLASK Y EXTENSIONES
from flask import Flask, render_template, request, jsonify, send_from_directory
from sqlalchemy.sql import func

# 3. IMPORTS DE BLUEPRINTS (Rutas modularizadas)
from backend.routes.home import home_bp
from backend.routes.user import user_bp
from backend.routes.tables import tables_bp
from backend.routes.publications import publications_bp
from backend.routes.premium import premium_bp
from backend.routes.auth import auth_bp

# 4. IMPORTS DE MODELOS Y BASE DE DATOS
from database.database import SessionLocal, engine, Base
from database.schema.models import User, Publication, Collection as Table
from database.schema import models

# --- CONFIGURACIÓN DE LA APP ---
app = Flask(__name__, 
            template_folder='../frontend/pages', 
            static_folder='../frontend/static')

app.secret_key = 'trastevere_clave_secreta_super_segura'

# Registro de Blueprints
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(tables_bp, url_prefix='/tables')
app.register_blueprint(publications_bp, url_prefix='/publications')
app.register_blueprint(premium_bp, url_prefix='/premium')
app.register_blueprint(auth_bp, url_prefix='/auth')

# --- GESTIÓN DE ALMACENAMIENTO (STORAGE) ---
@app.route('/storage/images/<filename>')
def get_storage_image(filename):
    """ Servidor de archivos estáticos para las imágenes de recetas en /storage/images """
    storage_dir = os.path.join(root_path, 'storage', 'images')
    return send_from_directory(storage_dir, filename)

# --- API ENDPOINTS (Lógica de Datos) ---

@app.route('/api/recipes/search')
def get_search_data():
    """
    Endpoint centralizado para el buscador.
    Implementa 'Data Cleaning' en tiempo real: convierte el campo JSONB de la DB
    en diccionarios de Python, asegurando que el frontend siempre reciba arrays válidos.
    """
    db = SessionLocal()
    try:
        publications_db = db.query(Publication).all()
        feed = []
        
        for pub in publications_db:
            # Normalización del campo meta (JSONB)
            # Manejamos casos donde SQLAlchemy pueda devolver el campo como String
            meta = pub.image_meta
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except json.JSONDecodeError:
                    meta = {}
            elif meta is None:
                meta = {}

            # Extracción segura de metadatos con valores por defecto
            tags = meta.get("tags", [])
            ingredients = meta.get("ingredients", [])
            urls = meta.get("urls", [])
            
            # Selección de imagen principal (fallback a default)
            img_url = urls[0] if (isinstance(urls, list) and len(urls) > 0) else "/storage/images/default_photo.jpg"

            feed.append({
                "id": pub.id,
                "title": pub.title,
                "author": pub.author.username if pub.author else "Anónimo",
                "image": img_url,
                "tags": tags,              
                "ingredients": ingredients 
            })
        
        return jsonify(feed)
    except Exception as e:
        print(f"Error crítico en el motor de búsqueda: {e}")
        return jsonify([])
    finally:
        db.close()

@app.route('/home/feed')
def get_home_feed():
    """ Proporciona una selección aleatoria de recetas para el feed principal """
    return get_search_data() # Reutilizamos la lógica robusta de limpieza de datos

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
    return render_template("profile.html")

# --- INICIALIZACIÓN ---
if __name__ == "__main__":
    # 1. Aseguramos la existencia del directorio de almacenamiento físico
    storage_dir = os.path.join(root_path, 'storage', 'images')
    os.makedirs(storage_dir, exist_ok=True)
    
    # 2. LA CLAVE: Creamos las tablas en la base de datos de Docker si no existen
    # Usamos los modelos importados en el punto 4 de tu archivo
    print("Sincronizando base de datos con Docker...")
    Base.metadata.create_all(bind=engine)
    
    print(f"Servidor Trastevere activo en http://localhost:5000")
    app.run(debug=True, port=5000)