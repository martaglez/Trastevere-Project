from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/feed', methods=['GET'])
def get_feed():
    feed = [
        {
            "title": "Pasta Carbonara",
            "description": "Receta clásica italiana",
            "tags": ["pasta", "italiano"]
        },
        {
            "title": "Pizza Margherita",
            "description": "Pizza sencilla y deliciosa",
            "tags": ["pizza", "queso"]
        }
    ]
    return jsonify(feed)