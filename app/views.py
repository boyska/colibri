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


# basic views for common models
def _link_esemplare(es):
    return '<a href="%s">%s</a>' % (escape(url_for('esemplare', id=es.id)),
                                    escape(es.opera.title))


def _link_opera(es):
    return '<a href="%s">%s</a>' % (escape(url_for('opera', id=es.id)),
                                    escape(es.title))


@app.route('/esemplare/<id>')
def esemplare(id):
    es = models.Esemplare.query.get(id)
    return '<pre>%s</pre>%s' % (escape(str(es)), _link_opera(es.opera))


@app.route('/opera/<id>')
def opera(id):
    op = models.Opera.query.get(id)
    return '<pre>%s</pre>%s' % (escape(str(op)),
                                ','.join(_link_esemplare(es)
                                         for es in op.esemplari))
