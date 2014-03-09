from uuid import uuid4

from flask.ext.security import UserMixin, RoleMixin

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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Book(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    title = db.Column(db.String(140))
    authors = db.relationship("Author",
                              secondary="book_author",
                              backref=db.backref("books", lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #FIXME: non funziona boh
    #position = db.relationship("Position", uselist=False, backref="books", lazy="dynamic")
    #category = db.relationship("Category", uselist=False, backref="books", lazy="dynamic")

    __mapper_args__ = {
        'version_id_col': id,
        'version_id_generator': lambda version: uuid4().hex
    }

    def __init__(self, title, authors):
        self.title = title
        self.authors = authors

    def __repr__(self):
        return '<Book %r>' % self.id

book_author = db.Table('book_author',
                       db.Column('book_id', db.String(32),
                                 db.ForeignKey('book.id')),
                       db.Column('author_id', db.Integer,
                                 db.ForeignKey('author.id'))
                       )


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))

    def __init__(self, name):
        self.name = name


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mnemonic = db.Column(db.String(16))
    description = db.Column(db.String(256))


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    #children = db.relationship("Category", backref="parent", lazy="dynamic")

#TODO: prestito
