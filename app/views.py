from flask import render_template, url_for, escape
from flask.ext.security import login_required
from app import app, models


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'base.html',
        content="Welcome to Colibri. Use the searchbar on top to look for " +
        "your favourite books")

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
    es = models.Esemplare.query.get_or_404(id)
    html = '<pre>%s</pre>%s' % (escape(str(es)), _link_opera(es.opera))
    return render_template('base.html', title=es.opera.title, content=html)


@app.route('/opera/<id>')
def opera(id):
    op = models.Opera.query.get_or_404(id)
    html = '<pre>%s</pre>%s' % (escape(str(op)),
                                ','.join(_link_esemplare(es)
                                         for es in op.esemplari))
    return render_template('base.html', title=op.title, content=html)
