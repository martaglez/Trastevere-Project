from flask import Blueprint, jsonify, request, render_template

tables_bp = Blueprint('tables', __name__)

tables = [
    {"id": 1, "name": "Mis Recetas", "publications": [1, 2]}
]

# devolver todas las tables
@tables_bp.route('/', methods=['GET'])
def all_tables():
    return jsonify(tables)


# devolver una table concreta (datos)
@tables_bp.route('/<int:table_id>', methods=['GET'])
def table_detail(table_id):
    table = next((t for t in tables if t["id"] == table_id), None)
    if table:
        pubs = [{"id": p, "title": f"Receta {p}"} for p in table["publications"]]
        return jsonify({
            "id": table_id,
            "name": table["name"],
            "publications": pubs
        })
    return jsonify({"error": "No encontrada"}), 404


# añadir receta a table
@tables_bp.route('/add', methods=['POST'])
def add_to_table():
    data = request.json
    table_id = data.get("table_id")
    publication_id = data.get("publication_id")

    table = next((t for t in tables if t["id"] == table_id), None)

    if not table:
        return jsonify({"error": "Table no encontrada"}), 404

    if publication_id not in table["publications"]:
        table["publications"].append(publication_id)

    return jsonify({"message": "Receta añadida a la table"})


# renderizar página HTML de una table
@tables_bp.route('/view/<int:table_id>')
def view_table(table_id):
    return render_template("table_detail.html")
