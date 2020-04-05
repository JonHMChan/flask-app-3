from flask import Blueprint, jsonify, request
import json

# A Flask blueprint that allows you to separate different parts of the app into different files
teams = Blueprint('teams', 'teams')

# Take team data from database.json and turn it into a Python dictionary to store in DATABASE
with open('data/database.json') as f:
  raw = json.load(f)
DATABASE = raw.get("teams", [])

# Track the ID that will be used for new teams when they are added to DATABASE
current_id = len(DATABASE) + 1

# REST
# One of the ways to design your web application is to create an internal API so your front end can get data.
# There are lots of different ways different applications do this, but one of the most common ways is to
# create an API using the REST model. This makes it easy to understand what each URL (or endpoint) of your
# application will do to a piece of data, depending on which HTTP method you use (GET, POST, PUT, PATCH, DELETE).
# This file contains the API definition for the teams API, which should do the following:

# Method    URL             Description
# -------------------------------------------------------------------------------------------
# GET       /teams          Gets all teams
# GET       /teams/:id      Gets a single team with the ID :id
# POST      /teams          Creates a new team using request body JSON
# PUT       /teams/:id      Replaces the team with ID :id with request body JSON
# PATCH     /teams/:id      Partially updates the team with ID :id with the request body JSON
# DELETE    /teams/:id      Deletes the team with the ID :id

# Some of these API endpoints are incomplete according to what the REST pattern dictates. It's your job to fix them.

# API route that returns all teams from DATABASE
@teams.route('/teams', methods=['GET'])
def api_teams_get():
    return jsonify(DATABASE), 200

# API route that returns a single teams from DATABASE according to the ID in the URL
# For example /api/teams/1 will give you Ash's Team
@teams.route('/teams/<int:id>', methods=['GET'])
def api_teams_id_get(id):
    for teams in DATABASE:
        if teams.get("id") == id:
            return jsonify(teams), 200
    return jsonify({}), 404

# API route that creates a new team using the request body JSON and inserts it at the end of DATABASE
@teams.route('/teams', methods=['POST'])
def api_teams_id_post():
    # Declare current_id as a global so it can be used correctly in this function
    global current_id

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json()

    # Validating the request body before inserting it into DATABASE
    keys = ["name", "description", "pokemon"]
    for key in keys:
        # Make sure all the required keys in the keys list is in the response json
        if key not in json:
            return jsonify({
                "error": ("You are missing the '" + key  + "' in your request body")
            }), 400
        # Make sure the values at the types and evolutions keys are lists
        if key in ["pokemon"] and not isinstance(json[key],list):
            return jsonify({
                "error": ("Your value at '" + key  + "' must be a list, not a '" + type(json[key]).__name__ + "'")
            }), 400

    # Create a dictionary that contains all of the request json information and a new ID
    teams = {
        "id": current_id,
        "name": json["name"],
        "description": json["description"],
        "pokemon": []
    }
    # Add the new teams entry to the end of the global DATABASE list
    DATABASE.append(teams)

    # Increment the current_id by 1 so it will be unique for the next inserted teams
    current_id = current_id + 1

    # Return the newly inserted teams as a response
    return jsonify(teams)

# API route that does a full update by replacing the entire teams dictionary at the specified ID with the request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would replace the Bulbasaur dictionary with the object { "name": "Foobar" }
@teams.route('/teams/<int:id>', methods=['PUT'])
def api_teams_id_put(id):

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json(id)

    # Iterate through the teams DATABASE, making sure the index is available by using enumerate()
    for index, teams in enumerate(DATABASE):

        # If the ID matches, replace the entire teams dictionary with the request body JSON at the same index
        if teams.get("id") == id:
            DATABASE[index] = json
            return jsonify(json), 200
    
    # If no teams with the ID in the URL can be found in DATABASE, return nothing
    return jsonify({}), 404

# API route that does a partial update by changing the values of the teams dictionary at the specified ID with the values in request body JSON
# For example sending { "name": "Foobar" } to /api/teams/1 would only change Bulbasaur's name to "Foobar" - nothing else would change
@teams.route('/teams/<int:id>', methods=['PATCH'])
def api_teams_id_patch(id):

    # Get the JSON from the request body and turn it into a Python dictionary
    json = request.get_json()

    # Iterate through all of the teams DATABASE
    for teams in DATABASE:
        # Find a matching teams with the ID specified in the URL
        if teams.get("id") == id:
            # Go through every key in the teams dictionary
            for key in teams:
                # Get the value of the key, or if it has no value, False
                jsonValue = json.get(key, False)
                # Make sure there is a value and make it's the same type as the existing value
                if jsonValue and type(jsonValue) == type(teams[key]):
                    # Replace the value of the key
                    teams[key] = jsonValue
            
            # Return the modified teams dictionary as a response
            return jsonify(teams), 200

    # If no teams with the ID in the URL can be found in DATABASE, return nothing
    return jsonify({}), 404

# API route that deletes a single teams from DATABASE
# For example /api/teams/1 will delete Bulbasaur
@teams.route('/teams/<int:id>', methods=['DELETE'])
def api_teams_id_delete(id):
    # Declare DATABASE as a global so it can be used correctly in this function
    global DATABASE

    # Filter the list so any teams dictionaries with the ID specified in the URL are removed from DATABASE
    DATABASE = list(filter(lambda x: x.get("id") != id, DATABASE))

    # Return an empty object
    return jsonify({}), 200