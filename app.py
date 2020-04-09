import os
import api 
import json
import re
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
# (done) Searches should be case insensitive
# (done) You should not use JavaScript or AJAX in search.html
# (done) For pokemon, items should be ranked higher if any of the words in the search query are in the name, description, or types
# (done) For teams, items should be ranked higher if any of the words in the search query are in the name or description
# (done) Not all properties are treated equally: if there is a match in the name, rank the item higher than other properties

# Extra requirements when you're done:
# (done) Teams should rank higher if their member pokemon also match
# (done) Highlight the matching word in the name or description in the search results
# (part done) Implement a filter for search queries (e.g. searching "p type:fire" will only
#   search for pokemon that contain the letter p that are fire type pokemon)
# - Add pagination to your search results page so only 20 pokemon show up at a time,
#   but you can navigate to another page

# takes a string like "p type:electric" and splits it into p, type, and electric
def search_parser(search_string):
        filters = re.match(r'^(?P<str>.*)\s(?P<mod>.*)[:](?P<fil>.*)(\s|$)', search_string)
        if filters != None:
            return filters
        else:
            return False

# generator function that returns at the first match or yields until it's called again
def search_db(search_string, search_object):
    if search_string in search_object['name'].lower():
        return search_object
    else:
        yield
    if search_string in search_object['description'].lower():
        return search_object
    else:
        yield
    if 'types' in search_object.keys():
        for t in search_object['types']:
            if search_string == t.lower():
                return search_object
        return False
    else:
        for p in search_object['members']:
            if search_string == pokemon[p['pokemon_id']-1]['name'].lower():
                return search_object
        return False

def highlighter(results, search_string, keyArray):
    for i in range(len(results)):
        for j in keyArray:
            caps_string = search_string.capitalize()
            results[i][j] = results[i][j].replace(search_string,f'<span class="highlight">{search_string}</span>')
            results[i][j] = results[i][j].replace(caps_string,f'<span class="highlight">{caps_string}</span>')
    return results


@app.route('/search')
def search():
    search_string_raw = request.args.get('query').lower()
    search_params = search_parser(search_string_raw)
    if search_params:
        search_string = search_params.group('str')
        search_type = search_params.group('fil')
    else:
        search_string = search_string_raw
    results = []
    global teams
    global pokemon
    teams = DATABASE['teams']
    pokemon = DATABASE['pokemon']
    gens = []
    gens_to_remove = []

    for i in range(len(pokemon)):
        gens.append(search_db(search_string, pokemon[i]))
    for i in range(len(teams)):
        gens.append(search_db(search_string, teams[i]))
    
    for h in range(3):
        for j in range(len(gens)):
            try:
                next(gens[j])
            except StopIteration as output:
                if output.value != False and output.value != None:
                    results.append(output.value)
    if search_params:
        new_results = []
        for i in range(len(results)):
            if 'types' in results[i].keys():
                for j in results[i]['types']:
                    if j == search_type.lower():
                        new_results.append(results[i])
        results.clear()
        results = new_results

    results = highlighter(results, search_string, ['name','description'])
    
    return render_template('search.html', results=results, searchstring=search_string)        

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)