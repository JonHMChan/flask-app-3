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

# Teams create page that serves teams/create.html
@app.route('/teams/create')
def teams_create():
    return render_template('teams/create.html', pokemon=DATABASE.get("pokemon", []))

# Searches for pokemon and teams in DATABASE and displays in search.html using Jinja (no AJAX)
# - Searches should be case insensitive
# - You should not use JavaScript or AJAX in search.html
# - For pokemon, items should be ranked higher if any of the words in the search query are in the name, description, or types
# - For teams, items should be ranked higher if any of the words in the search query are in the name or description
# - Not all properties are treated equally: if there is a match in the name, rank the item higher than other properties

# Extra requirements when you're done:
# - Teams should rank higher if their member pokemon also match
# - Highlight the matching word in the name or description in the search results
# - Implement a filter for search queries (e.g. searching "p type:fire" will only
#   search for pokemon that contain the letter p that are fire type pokemon)
# - Add pagination to your search results page so only 20 pokemon show up at a time,
#   but you can navigate to another page
@app.route('/search')
def search():
    return render_template('search.html')        

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)