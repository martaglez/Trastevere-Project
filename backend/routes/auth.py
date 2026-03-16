from flask import Blueprint, request, jsonify, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        # Añadir una validación simple para probar
        return jsonify({"message": "Login correcto", "user_id": 1, "redirect": "/home/feed"}), 200
    
    # Si entras normal (GET), te muestra el HTML
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        return jsonify({"message": "Usuario creado", "user_id": 1, "redirect": "/auth/login"}), 201
    
    # Si entras normal (GET), te muestra el HTML
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    # Simplemente mostramos la página de despedida
    return render_template('logout.html')