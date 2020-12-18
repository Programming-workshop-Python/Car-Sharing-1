from settings import db

def add_data(data):
    db.session.add(data)
    db.session.commit()