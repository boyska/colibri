import flask
from flask import url_for, escape
from flask.ext.admin import Admin, BaseView, expose
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


class CustomView(ModelView):
    '''
    A simple collection of typical configuration. Not very semantic, one day
    this will be refactored.
    '''
    form_excluded_columns = ('confirmed_at', 'password')

    def linked_formatter(self, context, model, name):
        def link_one(field, name):
            if not field:
                return 'N/A'
            nice = unicode(field)
            html = '<a href="%s">%s</a>' % (
                url_for('%sview.edit_view' % name, id=field.id),
                flask.escape(nice)
            )
            return html
        val = getattr(model, name)
        if hasattr(val, '__iter__'):
            html = ','.join((link_one(field, field.__tablename__)
                             for field in val))
            return Markup(html)
        else:
            return Markup(link_one(val, name))


class UserView(CustomView):
    column_exclude_list = ('password', 'confirmed_at')
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


class OperaView(CustomView):
    form_excluded_columns = ('esemplari', )
    #form_overrides = dict(authors=Select2TagsField)

    def is_accessible(self):
        return current_user.is_authenticated()



class BookView(CustomView):
    #form_create_rules = (rules.FieldSet(('title', 'authors'), header='Opera'),
    #                     rules.FieldSet(('position',), 'Organizzazione')
    #                     )
    #inline_models = [(models.Position, dict(form_columns=['position']))]
    column_display_all_relations = True
    column_formatters = {
        'position': CustomView.linked_formatter,
        'opera': CustomView.linked_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated()


class AuthorView(CustomView):
    #form_excluded_columns = ('opere', )
    column_display_all_relations = True
    column_formatters = {
        'opere': CustomView.linked_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated()


class CategoryView(CustomView):
    form_excluded_columns = ('books', )

    def is_accessible(self):
        return current_user.is_authenticated()


class SummaryView(BaseView):
    def esemplari_for_position(self):
        #FIXME: sbagliato
        group = db.session.query(models.Position,
                                 db.func.count(models.Esemplare.id).
                                 label('esemplari')).\
            group_by(models.Esemplare.position_id)
        return '<br/>'.join(escape('%s=%d' % (unicode(p), c))
                            for p, c in group.all())

    def total_esemplari(self):
        tot = models.Esemplare.query.count()
        return '%d Esemplari' % tot

    def total_opere(self):
        tot = models.Opera.query.count()
        return '%d Opere' % tot

    @expose('/')
    def index(self):
        totals = (self.total_esemplari, self.total_opere)
        return self.render('base_report.html',
                           content='<br/>'.join(func() for func in totals))
admin.add_view(UserView(models.User, db.session, category='SuperAdmin'))
admin.add_view(UserView(models.Role, db.session, category='SuperAdmin'))
admin.add_view(OperaView(models.Opera, db.session))
admin.add_view(BookView(models.Esemplare, db.session))
admin.add_view(AuthorView(models.Author, db.session))

admin.add_view(CategoryView(models.Position, db.session, category='Meta'))
admin.add_view(CategoryView(models.Category, db.session, category='Meta'))

admin.add_view(SummaryView(name='Summary', category='Report'))
