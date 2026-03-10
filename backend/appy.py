from flask import Flask, render_template
from routes.home import home_bp
# Importa otros blueprints si los tienes
from routes.user import user_bp
from routes.tables import tables_bp
from routes.publications import publications_bp
from routes.premium import premium_bp


# Le decimos a Flask que busque los HTML en la carpeta 'frontend' que está un nivel arriba
app = Flask(__name__, template_folder='../frontend/pages', static_folder='../frontend/static')

# Blueprints
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(tables_bp, url_prefix='/tables')
app.register_blueprint(publications_bp, url_prefix='/publications')
app.register_blueprint(premium_bp, url_prefix='/premium')

# Principal page
@app.route('/')
def home():
    return render_template('home.html')

# Routes HTML 

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)