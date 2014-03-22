'''
Get a CSV (tab-delimited) where columns are:
1) # of items
2) Authors, comma delimited
3) Title
4) Publisher
'''
import sys
import os
import csv
projdir = os.path.realpath('../../')
sys.path.append(projdir)
from app import models, db


def get_author(authorname):
    aut = models.Author.query.filter_by(name=authorname).first()
    if aut is None:
        aut = models.Author()
        aut.name = authorname
    else:
        print 'anvedi, ripescato', authorname, aut.id
    return aut


def get_location(locname):
    loc = models.Position.query.filter_by(mnemonic=locname).first()
    if loc is None:
        loc = models.Position()
        loc.mnemonic = locname
        loc.description = locname
    return loc


def make_opera(authorlist, title):
    o = models.Opera()
    o.title = title
    o.authors = [get_author(a) for a in authorlist]
    db.session.add(o)
    return o


def make_esemplare(opera, location):
    e = models.Esemplare()
    e.opera = opera
    e.position = get_location(location)
    db.session.add(e)

if __name__ == '__main__':
    csvpath = sys.argv[1]
    csv = csv.reader(open(csvpath, 'rb'), delimiter='\t', quotechar='"')
    db.create_all()
    for line in csv:
        count, loc, authors, title, publisher = line[:5]
        print line
        op = make_opera(authors.decode('utf-8').split(','),
                        title.decode('utf-8'))
        for _ in xrange(int(count)):
            make_esemplare(op, loc.upper())
        db.session.commit()


# vim: set ts=4 sw=4 et:
