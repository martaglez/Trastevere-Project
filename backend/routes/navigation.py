from flask import Blueprint, jsonify

navigation_bp = Blueprint('navigation', __name__)

@navigation_bp.route('/buttons', methods=['GET'])
def bottom_buttons():
    buttons = {
        "home": "/home/feed",
        "search": "/navigation/search",
        "create": "/publications/create",
        "tables": "/tables/",
        "profile": "/user/profile"
    }
    return jsonify(buttons)

@navigation_bp.route('/search', methods=['GET'])
def search_example():
    sample_tags = ["pasta", "pizza", "queso", "postre", "ensalada"]
    return jsonify({"recommended_tags": sample_tags})

