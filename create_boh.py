import app

m = app.models
db = app.db

da = m.Author('Dante Alighieri')
v = m.Author('Virgilio')
dc = m.Book('Divina commedia', [da, v])
db.session.add(dc)
db.session.commit()
