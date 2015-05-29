from flask import Flask, render_template, request, url_for, Blueprint

from application import get_app
from application.models.Match import Match

app = get_app()

@app.route('/')
def indexView():
    return render_template("index.html")

@app.route('/matches')
def gamesView():
    return render_template("matches.html")

@app.route('/matches/<match_id>')
def gamesViewById(match_id):
    if match_id == 'new':
        return render_template("new_match.html")
    return render_template("match.html", match=Match.query({'_id': match_id}).generate_json())

