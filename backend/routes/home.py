from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/feed', methods=['GET'])
def get_feed():
    feed = [
        {
            "id": 1,
            "title": "Pasta Carbonara",
            "description": "Receta clásica italiana",
            "tags": ["pasta", "italiano"],
            "image": "/static/pasta.jpg"
        },
        {
            "id": 2,
            "title": "Pizza Margherita",
            "description": "Pizza sencilla y deliciosa",
            "tags": ["pizza", "queso"],
            "image": "/static/pizza.jpg"
        },
        {
            "id": 3,
            "title": "Ensalada César",
            "description": "Fresca y saludable",
            "tags": ["ensalada", "pollo"],
            "image": "/static/ensalada.jpg"
        },
        {
            "id": 4,
            "title": "Brownie de Chocolate",
            "description": "Dulce y esponjoso",
            "tags": ["postre", "chocolate"],
            "image": "/static/brownie.jpg"
        },
        {
            "id": 5,
            "title": "Sopa de Verduras",
            "description": "Calentita y nutritiva",
            "tags": ["sopa", "verduras"],
            "image": "/static/sopa.jpg"
        },
        {
            "id": 6,
            "title": "Tacos Mexicanos",
            "description": "Picante y delicioso",
            "tags": ["mexicano", "tacos"],
            "image": "/static/tacos.jpg"
        }
    ]
    return jsonify(feed)

