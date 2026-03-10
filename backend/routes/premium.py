from flask import Blueprint, jsonify

premium_bp = Blueprint('premium', __name__)

@premium_bp.route('/features', methods=['GET'])
def features():
    return jsonify({
        "weekly_coupon": "10€ supermercado",
        "theme_color": "azul",
        "recipe_of_week": {"id": 101, "title": "Ensalada Premium"}
    })