from flask import Blueprint, jsonify
from .publications import publications

home_bp = Blueprint('home', __name__)

@home_bp.route('/feed', methods=['GET'])
def get_feed():
    feed = [
        {
            "id": pub["id"],
            "title": pub["title"],
            "description": pub.get("description", ""),
            "tags": pub.get("tags", []),
            "image": pub.get("images", ["/static/default_recipe.jpg"])[0]
        }
        for pub in publications
    ]
    return jsonify(feed)