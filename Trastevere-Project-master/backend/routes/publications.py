from flask import Blueprint, request, jsonify
from flask import render_template
#from flask_login import current_user


publications_bp = Blueprint('publications', __name__)

publications = [
    {
        "id": 1,
        "title": "Pasta Carbonara",
        "description": "Receta clásica italiana",
        "ingredients": ["Pasta", "Huevo", "Bacon", "Queso"],
        "steps": ["Cocer pasta", "Freír bacon", "Mezclar todo"],
        "images": ["/static/pasta.jpg"],
        "tags": ["pasta", "italiano"]
    },
    {
        "id": 2,
        "title": "Pizza Margherita",
        "description": "Pizza sencilla y deliciosa",
        "ingredients": ["Masa", "Tomate", "Queso", "Albahaca"],
        "steps": ["Preparar masa", "Añadir ingredientes", "Hornear 15 min"],
        "images": ["/static/pizza.jpg"],
        "tags": ["pizza", "queso"]
    }
]
publications += [
    {
        "id": 3,
        "title": "Ensalada César",
        "description": "Fresca y saludable",
        "ingredients": ["Lechuga", "Pollo", "Queso parmesano", "Pan tostado", "Aderezo César"],
        "steps": ["Cortar la lechuga", "Cocinar pollo", "Mezclar todo con aderezo"],
        "images": ["/static/ensalada.jpg"],
        "tags": ["ensalada", "pollo"]
    },
    {
        "id": 4,
        "title": "Brownie de Chocolate",
        "description": "Dulce y esponjoso",
        "ingredients": ["Chocolate", "Harina", "Azúcar", "Huevos", "Mantequilla"],
        "steps": ["Derretir chocolate", "Mezclar ingredientes", "Hornear 25 min"],
        "images": ["/static/brownie.jpg"],
        "tags": ["postre", "chocolate"]
    },
    {
        "id": 5,
        "title": "Sopa de Verduras",
        "description": "Calentita y nutritiva",
        "ingredients": ["Zanahoria", "Calabacín", "Cebolla", "Apio", "Caldo"],
        "steps": ["Cortar verduras", "Hervir en caldo", "Servir caliente"],
        "images": ["/static/sopa.jpg"],
        "tags": ["sopa", "verduras"]
    },
    {
        "id": 6,
        "title": "Tacos Mexicanos",
        "description": "Picante y delicioso",
        "ingredients": ["Tortillas", "Carne", "Salsa", "Cebolla", "Cilantro"],
        "steps": ["Cocinar carne", "Calentar tortillas", "Armar tacos"],
        "images": ["/static/tacos.jpg"],
        "tags": ["mexicano", "tacos"]
    }
]


@publications_bp.route('/all', methods=['GET'])
def all_publications():
    return jsonify(publications)


@publications_bp.route('/create', methods=['POST'])
def create_publication():
    data = request.json
    pub_id = len(publications) + 1

    # Usuario por defecto si no hay login
    user_name = "Usuario"

    pub = {
        "id": pub_id,
        "title": data.get('title'),
        "description": data.get('description'),
        "user": user_name,  # se añade aquí
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

@publications_bp.route('/view/<int:pub_id>')
def publication_view(pub_id):
    return render_template("recipe_detail.html")

