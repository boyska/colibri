import flask
from flask import url_for
from flask.ext.admin import Admin
from flask.ext.wtf import Form
from wtforms import TextField
# from flask.ext.admin.form import rules
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form.fields import Select2TagsField
from flask.ext.admin.form.rules import Markup
from flask.ext.security import current_user
# from wtforms.fields import PasswordField

from app import app, models, db

admin = Admin(app, name="Colibri'")


class UserView(ModelView):
    column_exclude_list = ('password', 'confirmed_at')
    form_excluded_columns = ('confirmed_at', 'password')
    #column_display_all_relations = True
    #TODO: allow change password; need to encrypt it, later
    #form_extra_fields = {
    #    'password': PasswordField('Password')
    #}

    def is_accessible(self):
        return current_user.is_authenticated()


class OperaForm(Form):
    title = TextField("")
    authors = Select2TagsField(default="",)


class OperaView(ModelView):
    form_excluded_columns = ('esemplari', )
    #form_overrides = dict(authors=Select2TagsField)

    def is_accessible(self):
        return current_user.is_authenticated()


def linked_formatter(view, context, model, name):
    field = getattr(model, name)
    if not field:
        return 'N/A'
    nice = unicode(field)
    return Markup(
        '<a href="%s">Clicche%s</a>' % (
            url_for('%sview.edit_view' % name, id=field.id),
            nice
        )
    )


class BookView(ModelView):
    #form_create_rules = (rules.FieldSet(('title', 'authors'), header='Opera'),
    #                     rules.FieldSet(('position',), 'Organizzazione')
    #                     )
    #inline_models = [(models.Position, dict(form_columns=['position']))]
    column_display_all_relations = True
    column_formatters = {
        'position': linked_formatter,
        'opera': linked_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated()


class AuthorView(ModelView):
    form_excluded_columns = ('books', )
    column_display_all_relations = True

    def is_accessible(self):
        return current_user.is_authenticated()


class CategoryView(ModelView):
    form_excluded_columns = ('books', )

    def is_accessible(self):
        return current_user.is_authenticated()

admin.add_view(UserView(models.User, db.session, category='SuperAdmin'))
admin.add_view(UserView(models.Role, db.session, category='SuperAdmin'))
admin.add_view(OperaView(models.Opera, db.session))
admin.add_view(BookView(models.Esemplare, db.session))
admin.add_view(AuthorView(models.Author, db.session))

admin.add_view(CategoryView(models.Position, db.session, category='Meta'))
admin.add_view(CategoryView(models.Category, db.session, category='Meta'))
