from uuid import uuid4

from flask.ext.security import UserMixin, RoleMixin
import flask.ext.whooshalchemy

import app
db = app.db

ROLE_USER = 0
ROLE_ADMIN = 1


# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return '<Role: %s>' % (self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __unicode__(self):
        return '<Role: %s>' % (self.email)


class Author(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))

    def __unicode__(self):
        return self.name


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mnemonic = db.Column(db.String(16))
    description = db.Column(db.String(256))
    esemplari = db.relationship("Esemplare", backref="position",
                                lazy="dynamic")

    def __unicode__(self):
        return '%s(%s)' % (self.mnemonic, self.description)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    opere = db.relationship("Opera", backref="category", lazy="dynamic")
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    children = db.relationship("Category",
                               backref=db.backref("parent", remote_side=[id]),
                               lazy="dynamic")

    def __unicode__(self):
        return '<Category: %s>' % self.name


class UUIDMixin(object):
    id = db.Column(db.String(32), primary_key=True, unique=True,
                   default=lambda: uuid4().hex)


# TODO: i18n-ize as Work
class Opera(UUIDMixin, db.Model):
    ''' According to FRBR, this is Work + Expression '''
    __tablename__ = 'work'
    __searchable__ = ['title']
    title = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    authors = db.relationship("Author",
                              secondary="opera_author",
                              backref=db.backref("opere"))
    esemplari = db.relationship("Esemplare", backref="opera", lazy="dynamic")

    def __unicode__(self):
        return '<Opera: %s>' % self.title


# TODO: i18n-ize as Physical
class Esemplare(UUIDMixin, db.Model):
    ''' According to FRBR, this is Item + Manifestation '''
    __tablename__ = 'physical'
    opera_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    def __unicode__(self):
        return '<Esemplare: %s>' % self.opera.title

opera_author = db.Table('opera_author',
                        db.Column('opera_id', db.String(32),
                                  db.ForeignKey('work.id')),
                        db.Column('author_id', db.Integer,
                                  db.ForeignKey('author.id'))
                        )


#TODO: prestito
