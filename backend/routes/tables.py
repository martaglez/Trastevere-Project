import json
from flask import Blueprint, jsonify, request, render_template, session
from database.database import SessionLocal
from database.schema.models import Collection, Publication, CollectionItem

tables_bp = Blueprint('tables', __name__)

# --- ESCUDO DE SEGURIDAD REUTILIZABLE ---
def get_current_user():
    return session.get('user_id')

# 1. Devolver todas las tables (Collections) del usuario logueado
@tables_bp.route('/', methods=['GET'])
def all_tables():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    db = SessionLocal()
    try:
        # FILTRADO REAL: Solo las tablas que pertenecen al usuario
        collections = db.query(Collection).filter(Collection.user_id == user_id).all()
        
        result = []
        for col in collections:
            previews = []
            # Sacamos las fotos de las recetas guardadas en esta tabla
            for item in col.items[:3]:
                meta = item.publication.image_meta
                # Manejo de meta como dict o string (Data Cleaning)
                if isinstance(meta, str):
                    try: meta = json.loads(meta)
                    except: meta = {}
                
                if meta and "urls" in meta and len(meta["urls"]) > 0:
                    previews.append(meta["urls"][0])
                else:
                    previews.append("/storage/images/default_photo.jpg")

            result.append({
                "id": col.id,
                "name": col.name,
                "previews": previews
            })
        return jsonify(result)
    finally:
        db.close()

# 2. Devolver detalle de una table (con sus recetas)
@tables_bp.route('/<int:table_id>', methods=['GET'])
def table_detail(table_id):
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    db = SessionLocal()
    try:
        # Verificamos que la tabla exista Y pertenezca al usuario
        col = db.query(Collection).filter(Collection.id == table_id, Collection.user_id == user_id).first()
        if not col:
            return jsonify({"error": "No encontrada o no tienes permiso"}), 404

        pubs = []
        for item in col.items:
            pub = item.publication
            meta = pub.image_meta
            if isinstance(meta, str):
                try: meta = json.loads(meta)
                except: meta = {}

            img = "/storage/images/default_photo.jpg"
            if meta and "urls" in meta and len(meta["urls"]) > 0:
                img = meta["urls"][0]

            pubs.append({
                "id": pub.id,
                "title": pub.title,
                "image": img
            })

        return jsonify({
            "id": col.id,
            "name": col.name,
            "publications": pubs
        })
    finally:
        db.close()

# 3. Añadir receta a table
@tables_bp.route('/add', methods=['POST'])
def add_to_table():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    db = SessionLocal()
    try:
        # Validar que la tabla sea del usuario antes de añadir nada
        col = db.query(Collection).filter(Collection.id == data.get("table_id"), Collection.user_id == user_id).first()
        if not col:
            return jsonify({"error": "Operación no permitida"}), 403

        new_item = CollectionItem(
            collection_id=data.get("table_id"),
            publication_id=data.get("publication_id")
        )
        db.add(new_item)
        db.commit()
        return jsonify({"message": "Receta añadida"})
    except Exception:
        db.rollback()
        return jsonify({"error": "Ya está en la table"}), 400
    finally:
        db.close()

# 4. Crear Table en la DB (ASIGNACIÓN REAL DE USER_ID)
@tables_bp.route('/create', methods=['POST'])
def create_table():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    db = SessionLocal()
    try:
        # YA NO USAMOS EL user_id=1, usamos el de la sesión
        new_col = Collection(name=data.get("name"), user_id=user_id)
        db.add(new_col)
        db.commit()
        return jsonify({"message": "Table creada"})
    finally:
        db.close()

# 5. Eliminar Table
@tables_bp.route('/delete/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    db = SessionLocal()
    try:
        col = db.query(Collection).filter(Collection.id == table_id, Collection.user_id == user_id).first()
        if col:
            db.delete(col)
            db.commit()
            return jsonify({"message": "Eliminada"})
        return jsonify({"error": "No encontrada"}), 404
    finally:
        db.close()

# 6. Quitar receta de la Table
@tables_bp.route('/remove', methods=['POST'])
def remove_from_table():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    db = SessionLocal()
    try:
        # Buscamos el item asegurándonos de que la colección pertenece al usuario
        item = db.query(CollectionItem).join(Collection).filter(
            CollectionItem.collection_id == data.get("table_id"),
            CollectionItem.publication_id == data.get("publication_id"),
            Collection.user_id == user_id
        ).first()
        
        if item:
            db.delete(item)
            db.commit()
            return jsonify({"message": "Receta eliminada"})
        return jsonify({"error": "No encontrada"}), 404
    finally:
        db.close()

# 7. Vista HTML
@tables_bp.route('/view/<int:table_id>')
def view_table(table_id):
    return render_template("table_detail.html")