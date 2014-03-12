from app.models import Esemplare, Opera

def search(querystr):
    '''
    Generic search function
    '''
    return Esemplare.query.join(Opera).filter(
        Opera.title.like('%%%s%%' % querystr))
