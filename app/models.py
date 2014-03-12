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
    esemplari = db.relationship("Esemplare", backref="position", lazy="dynamic")

    def __unicode__(self):
        return '%s(%s)' % (self.mnemonic, self.description)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    esemplari = db.relationship("Opera", backref="category", lazy="dynamic")
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    children = db.relationship("Category",
                               backref=db.backref("parent", remote_side=[id]),
                               lazy="dynamic")

    def __unicode__(self):
        return '<Category: %s>' % self.name


class Opera(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    title = db.Column(db.String(140))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    authors = db.relationship("Author",
                              secondary="opera_author",
                              backref=db.backref("opere"))
    esemplari = db.relationship("Esemplare", backref="opera", lazy="dynamic")

    __mapper_args__ = {
        'version_id_col': id,
        'version_id_generator': lambda version: uuid4().hex
    }

    def __unicode__(self):
        return '<Opera: %s>' % self.title


class Esemplare(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    opera_id = db.Column(db.Integer, db.ForeignKey('opera.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    __mapper_args__ = {
        'version_id_col': id,
        'version_id_generator': lambda version: uuid4().hex
    }

    def __unicode__(self):
        return '<Esemplare: %s>' % self.opera.title

opera_author = db.Table('opera_author',
                        db.Column('opera_id', db.String(32),
                                  db.ForeignKey('opera.id')),
                        db.Column('author_id', db.Integer,
                                  db.ForeignKey('author.id'))
                        )


#TODO: prestito
