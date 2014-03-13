'''
API for colibri
'''

from datetime import datetime

from flask import request, escape, url_for, Response
from werkzeug.contrib.atom import AtomFeed

from app import app, utils, api_manager, models

#TODO: forbid GET_MANY for unauthenticated users
api_manager.create_api(models.Opera)
api_manager.create_api(models.Esemplare)


def results_rss(iterable):
    feed = AtomFeed("OpenSearch results",
                    feed_url=request.url,
                    url=request.url_root)
    for r in iterable:
        feed.add(r.opera.title,
                 'Libro bello eh %s' %
                 (','.join((escape(a.name) for a in r.opera.authors))),
                 updated=datetime.now(),
                 url=url_for('esemplare', id=r.id))
    return feed.get_response()


@app.route('/opensearch/search.xml')
def os_search():
    howmany = 20

    querystr = request.args.get('q', '')
    results = utils.search(querystr).limit(howmany)
    return results_rss(results.all())


@app.route('/opensearch/description.xml')
def os_description():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Colibri Node</ShortName>
  <Description>Search books &amp; resist</Description>
  <Url type="application/rss+xml" template="%s?q={searchTerms}"/>
</OpenSearchDescription>
''' % (request.host_url.rstrip('/') + url_for('os_search'),)
    return Response(xml, mimetype='application/opensearchdescription+xml')
