from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
pokemon = Blueprint('pokemon', 'pokemon')

# Take pokemon data from database.json and turn it into a Python dictionary to store in DATABASE
with open('data/database.json') as f:
  raw = json.load(f)
DATABASE = raw.get("pokemon", [])

# Track the ID that will be used for new pokemon when they are added to DATABASE
current_id = len(DATABASE) + 1

# API route that returns all pokemon from DATABASE
@pokemon.route('/pokemon', methods=['GET'])
def api_pokemon_get():
    return jsonify(DATABASE), 200

# API route that returns a single pokemon from DATABASE according to the ID in the URL
# For example /api/pokemon/1 will give you Bulbasaur
@pokemon.route('/pokemon/<int:id>', methods=['GET'])
def api_pokemon_id_get(id):
    for pokemon in DATABASE:
        if pokemon.get("id") == id:
            return jsonify(pokemon), 200
    return jsonify({}), 404