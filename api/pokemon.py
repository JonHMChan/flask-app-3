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
# Allows for an option "search" query parameter that shows only pokemon that contain the search query in the name of the pokemon
# For example, going to /pokemon?search=pika will return a list containing one item representing Pikachu
@pokemon.route('/pokemon', methods=['GET'])
def api_pokemon_get():

    return "Fix me!"

# API route that returns a single pokemon from DATABASE according to the ID in the URL
# For example /api/pokemon/1 will give you Bulbasaur
@pokemon.route('/pokemon/<int:id>', methods=['GET'])
def api_pokemon_id_get(id):
    return "Fix me!"