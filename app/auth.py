from flask.ext.security import Security, SQLAlchemyUserDatastore

from app import app, db, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


#TODO: rimuovi e fai gestione degli utenti da linea di comando

@app.route('/crea')
def create_user():
    if models.User.query.count() == 0:
        db.create_all()
        user_datastore.create_user(email='admin@test',
                                   password='password')
        db.session.commit()
        return 'created'
    else:
        return "C'hai provato, furbettino!"
