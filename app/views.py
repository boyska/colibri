from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.security import login_required
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Ciao sei nella index"

@app.route('/sec')
@login_required
def sec():
    return "E' un messaggio privatissimoooo"
