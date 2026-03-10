from flask import Blueprint, jsonify

tables_bp = Blueprint('tables', __name__)

tables = [
    {"id": 1, "name": "Mis Recetas", "publications": [1, 2]}
]

@tables_bp.route('/', methods=['GET'])
def all_tables():
    return jsonify(tables)

@tables_bp.route('/<int:table_id>', methods=['GET'])
def table_detail(table_id):
    table = next((t for t in tables if t["id"] == table_id), None)
    if table:
        pubs = [{"id": p, "title": f"Receta {p}"} for p in table["publications"]]
        return jsonify({"id": table_id, "name": table["name"], "publications": pubs})
    return jsonify({"error": "No encontrada"}), 404