"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Favourites, FavouritesType, People, Planets, Species, db, Users
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

tables = {
    "species": Species,
    "planets": Planets,
    "people": People
}

@app.route('/users', methods=['GET'])
def get_users():
    user_list = Users.query.all()
    return jsonify(user_list), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    return jsonify(user) if user else (jsonify({"error": "User not found"}), 400)

@app.route('/users/<int:user_id>/favourites', methods=['GET', 'POST', 'DELETE'])
def handle_favourites(user_id):
    if request.method == 'GET':
        favourites = Favourites.query.filter_by(user_id=user_id).all()
        return jsonify(favourites), 200
    
    data = request.get_json()

    if request.method == 'POST':
        required_fields = ["external_id", "type", "name"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        if not (data["type"] in FavouritesType.__members__):
            return jsonify({"error": "Type no valid"}), 400
        if Favourites.query.filter_by(external_id=data["external_id"], user_id=user_id, type=data["type"]).first():
            return jsonify({"error": "Resource already favourited"}), 400
        if not tables[data["type"].lower()].query.filter_by(id=data["external_id"]).first():
            return jsonify({"error": "Resource not found"}), 400

        new_favourite = Favourites(
            user_id=user_id,
            external_id=data["external_id"],
            type=data["type"],
            name=data["name"]
        )

        db.session.add(new_favourite)
        db.session.commit()

        return jsonify({
            "message": "Favorite added successfully",
            "favorite": new_favourite
        }), 201
    
    if request.method == 'DELETE':
        required_fields = ["id"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        favourite = Favourites.query.filter_by(id=data["id"], user_id=user_id).first()

        if not favourite:
            return jsonify({"error": "Favourite not found"}), 404

        db.session.delete(favourite)
        db.session.commit()

        return jsonify({"message": "Favourite deleted successfully"}), 200

@app.route('/species', methods=['GET'])
def get_species():
    species = Species.query.all()
    return jsonify(species), 200

@app.route('/species/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    specie = Species.query.get(specie_id)
    return jsonify(specie) if specie else (jsonify({"error": "Specie not found"}), 400)

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Species.query.get(planet_id)
    return jsonify(planet) if planet else (jsonify({"error": "Planet not found"}), 400)

@app.route('/people', methods=['GET'])
def get_characters():
    characters = People.query.all()
    return jsonify(characters), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    result = (
        db.session.query(People, Planets)
        .join(Planets, People.homeworld == Planets.uid)
        .filter(People.uid == people_id)
        .first()
    )
    character, home_world = result
    character.home_world = home_world
    return jsonify(character) if character else (jsonify({"error": "Character not found"}), 404)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
