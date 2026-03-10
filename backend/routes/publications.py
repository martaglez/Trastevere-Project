from flask import Blueprint, request, jsonify

publications_bp = Blueprint('publications', __name__)

publications = []

@publications_bp.route('/all', methods=['GET'])
def all_publications():
    return jsonify(publications)

@publications_bp.route('/create', methods=['POST'])
def create_publication():
    data = request.json
    pub_id = len(publications) + 1
    pub = {
        "id": pub_id,
        "title": data.get('title'),
        "description": data.get('description'),
        "ingredients": data.get('ingredients'),
        "steps": data.get('steps'),
        "images": data.get('images'),
        "tags": data.get('tags')
    }
    publications.append(pub)
    return jsonify({"message": "Publicación creada", "publication": pub}), 201

@publications_bp.route('/<int:pub_id>', methods=['GET'])
def publication_detail(pub_id):
    pub = next((p for p in publications if p["id"] == pub_id), None)
    if pub:
        return jsonify(pub)
    return jsonify({"error": "No encontrada"}), 404