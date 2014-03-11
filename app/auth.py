from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security.utils import encrypt_password

from app import app, db, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


#TODO: rimuovi e fai gestione degli utenti da linea di comando

@app.route('/crea')
def create_user():
    db.create_all()
    if models.Position.query.count() == 0:
        m = models.Position()
        m.mnemonic = 'mensolone'
        m.description = 'quello grosso, dai!'
        m2 = models.Position()
        m2.mnemonic = 'scaffaluccio'
        m2.description = "piccino piccio'"

        aut_k = models.Author()
        aut_k.name = 'Kernighan'
        aut_r = models.Author()
        aut_r.name = 'Ritchie'
        op = models.Opera()
        op.title = 'Linguaggio C'
        op.authors = [aut_k, aut_r]
        es = models.Esemplare()
        es.opera = op
        es.position = m
        db.session.add(es)
        es = models.Esemplare()
        es.opera = op
        es.position = m2
        db.session.add(es)

        op = models.Opera()
        op.title = 'The UNIX programming environment'
        op.authors = [aut_k]
        es = models.Esemplare()
        es.opera = op
        es.position = m
        db.session.add(es)
        db.session.commit()
    if models.Role.query.count() == 0:
        supa = user_datastore.create_role(name='super',
                                          description='Will do ANYTHING')
        user_datastore.create_role(name='librarian',
                                   description='Can manage books')
        db.session.commit()
    if models.User.query.count() == 0:
        adm = user_datastore.create_user(email='admin@test',
                                         password=encrypt_password('password'))
        user_datastore.add_role_to_user(adm, supa)
        db.session.commit()
        return 'created'
    else:
        return "C'hai provato, furbettino!"
