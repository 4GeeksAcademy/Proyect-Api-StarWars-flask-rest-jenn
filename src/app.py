import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

# Cargar variables de entorno
load_dotenv()

# Inicializar la app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#  GENERAL

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

# USERS

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    results = [user.serialize() for user in users]
    return jsonify(results), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    results = [fav.serialize() for fav in favorites]
    return jsonify(results), 200

#  PEOPLE

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    results = [person.serialize() for person in people]
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('birth_year'):
        return jsonify({"error": "Missing required fields"}), 400

    new_person = People(name=data['name'], birth_year=data['birth_year'])
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

#  PLANETS

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    results = [planet.serialize() for planet in planets]
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

#   FAVORITES

@app.route('/favorites/people', methods=['POST'])
def add_favorite_people():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('people_id'):
        return jsonify({"error": "Missing user_id or people_id"}), 400

    new_fav = Favorite(user_id=data['user_id'], people_id=data['people_id'], planet_id=None)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route('/favorites/planet', methods=['POST'])
def add_favorite_planet():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('planet_id'):
        return jsonify({"error": "Missing user_id or planet_id"}), 400

    new_fav = Favorite(user_id=data['user_id'], planet_id=data['planet_id'], people_id=None)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
