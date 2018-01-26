from flask import render_template

from . import app


@app.route('/')
def index():
    return "Hallo Welt"
