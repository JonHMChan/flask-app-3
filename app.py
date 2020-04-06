# Do not change anything in this file for this exercise
import os
import api 
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.register_blueprint(api.pokemon, url_prefix="/api")
app.register_blueprint(api.teams, url_prefix="/api")

# Take all data from database.json and turn it into a Python dictionary to store in DATABASE
with open('data/database.json') as f:
  DATABASE = json.load(f)

# Home page route that serves index.html
@app.route('/')
def index():
    return render_template('index.html')

# Detail page route that serves detail.html
# For example /1 will give you the detail page for Bulbasaur
@app.route('/pokemon/<int:id>')
def detail_id(id):
    return render_template('pokemon/detail.html')

# Teams detail page route that serves teams/detail.html
# For example /1 will give you the detail page for Ash's Team
@app.route('/teams/<int:id>')
def teams_id(id):
    return render_template('teams/detail.html')

# Teams edit page route that serves teams/edit.html
# For example /1 will let you edit Ash's Team
@app.route('/teams/<int:id>/edit')
def teams_id_edit(id):
    return render_template('teams/edit.html')

@app.route('/teams/create')
def teams_create():
    return render_template('teams/create.html', pokemon=DATABASE.get("pokemon", []))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()

    # Split tokens
    tokens = query.split(" ")

    # Rankings
    results = []

    for item in DATABASE.get("pokemon", []):
        append = False
        result = {
            "id": item.get("id", -1),
            "type": "pokemon",
            "name": item.get("name", ""),
            "description": item.get("description", ""),
            "ranking": 0
        }
        for token in tokens:
            for prop in [["name", 4], ["description", 2]]:
                if token in item.get(prop[0], "").lower():
                    append = True
                    result["ranking"] = result.get("ranking", 0) + prop[1]
            for pokeType in item.get("types", []):
                if token in pokeType.lower():
                    append = True
                    result["ranking"] = result.get("ranking", 0) + 1
        if append:
            results.append(result)
    
    for item in DATABASE.get("teams", []):
        append = False
        result = {
            "id": item.get("id", -1),
            "type": "team",
            "name": item.get("name", ""),
            "description": item.get("description", ""),
            "ranking": 0
        }
        for token in tokens:
            for prop in [["name", 4], ["description", 2]]:
                if token in item.get(prop[0], "").lower():
                    append = True
                    result["ranking"] = result.get("ranking", 0) + prop[1]
        if append:
            results.append(result)

    results = sorted(results, key=lambda x: x.get("ranking", 0), reverse=True)
    
    return render_template('search.html', results=results, query=query)
            

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)