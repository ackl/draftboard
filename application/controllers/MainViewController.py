from flask import Flask, render_template, request, url_for, Blueprint

from application import get_app

app = get_app()

@app.route('/')
def indexView():
    return render_template("index.html")

@app.route('/matches')
def gamesView():
    return render_template("matches.html")

