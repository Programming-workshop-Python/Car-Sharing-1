from settings import db

class Driver(db.Model):
    #create a table
    __tablename__ = "driver"
    id = db.Column(db.Integer, primary_key = True)
    point_A  = db.Column(db.String)
    point_B = db.Column(db.String)
    car = db.Column(db.String)
    free_place = db.Column(db.Integer)
    children = db.Column(db.Integer)
    pets = db.Column(db.String)
    music = db.Column(db.String)
    phone = db.Column(db.String)


    def __init__(self, point_A, point_B, car, free_place, children, pets, music, phone):


        self.point_A = point_A
        self.point_B = point_B
        self.car = car
        self.free_place = free_place
        self.children = children
        self.pets = pets
        self.music = music
        self.phone = phone

class Passenger(db.Model):
    #create a table
    __tablename__ = "passenger"
    id = db.Column(db.Integer, primary_key = True)
    point_A  = db.Column(db.String)
    point_B = db.Column(db.String)
    pas_quantity = db.Column(db.Integer)
    children = db.Column(db.Integer)
    pets = db.Column(db.String)
    music = db.Column(db.String)
    phone = db.Column(db.String)


    def __init__(self, point_A, point_B, pas_quantity, children, pets, music, phone):


        self.point_A = point_A
        self.point_B = point_B
        self.pas_quantity = pas_quantity
        self.children = children
        self.pets = pets
        self.music = music
        self.phone = phone
