from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


#Соединяемся с базой данных
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@localhost/Data'
db = SQLAlchemy(app)


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
db.create_all()

#Главная страница
@app.route('/')
def start_page():
    return render_template("start_page.html")

#Выбор таблицы д
@app.route('/create_ride_main', methods=['GET'])
def create_ride():
    return render_template('choose_status.html')

@app.route('/create_ride_main/create_rider', methods=['GET'])
def create_rider():
    return render_template("rider_info.html")
#Создать запись водителя
@app.route('/create_ride_main/create_rider_inf', methods=['POST'])
def create_rider_inf():
    if(request.method == 'POST'):
        point_A = request.form.get("point_A")
        point_B = request.form.get('point_B')
        car = request.form.get("car")
        free_place = request.form.get("free_place")
        children = request.form.get("children")
        pets = request.form.get("pets")
        music = request.form.get("music")
        phone = request.form.get("phone")
        driver = Driver(point_A, point_B, car, free_place, children, pets, music, phone)
        db.session.add(driver)
        db.session.commit()


    return redirect(url_for(".passenger_find", a=point_A, b=point_B, free_place=free_place, children=children, pets=pets))

@app.route('/create_ride_main/create_rider_inf', methods=['GET'])
def passenger_find():
    passenger = []
    a= request.args.get('a')
    b = request.args.get('b')
    pas_quant = request.args.get('free_place')
    chil = request.args.get('children')
    pets = request.args.get('pets')
    kwargs = {"point_A": a, "point_B": b, "pas_quantity": pas_quant, "children": chil, "pets": pets}
    passengers = Passenger.query.filter_by(**kwargs).all()
    '''for row in passengers:
        passenger.append(row.point_A)
        passenger.append(row.point_B)
        passenger.append(row.pas_quantity)
        passenger.append(row.children)
        passenger.append(row.pets)
        passenger.append(row.music)'''

    return render_template("pas_find.html", passenger=passengers)

@app.route('/create_ride_main/create_rider_inf/selected', methods=['GET'])
def selected():
    return
#Создать запись пасажра?
@app.route('/create_ride_main/create_passenger', methods=['GET'])
def create_passenger():
    return render_template("pas_info.html")

@app.route('/create_ride_main/create_passenger_inf', methods=['POST'])
def create_passenger_inf():
    if(request.method == 'POST'):
        point_A = request.form.get("point_A")
        point_B = request.form.get('point_B')
        pas_quantity = request.form.get("pas_quantity")
        children = request.form.get("children")
        pets = request.form.get("pets")
        music = request.form.get("music")
        phone = request.form.get("phone")

        passenger = Passenger(point_A, point_B, pas_quantity, children, pets, music, phone)
        db.session.add(passenger)
        db.session.commit()
    return redirect(url_for(".driver_find", a=point_A, b=point_B, pas_quantity=pas_quantity, children=children, pets=pets))

@app.route('/create_ride_main/create_passenger_inf', methods=['GET'])
def driver_find():
    passenger = []
    a= request.args.get('a')
    b = request.args.get('b')
    free_place = request.args.get('pas_quantity')
    chil = request.args.get('children')
    pets = request.args.get('pets')
    kwargs = {"point_A": a, "point_B": b, "free_place": free_place, "children": chil, "pets": pets}
    driver = Driver.query.filter_by(**kwargs).all()

    return render_template("driver_find.html", driver=driver)

#Поиск по критериям
@app.route('/find_ride', methods=['GET'])
def find_ride():
    return render_template('search.html')

@app.route('/find_ride/search', methods=['POST'])
def search():
    a = request.form.get('point_A')
    b = request.form.get('point_B')
    driver = request.form.get("driver")
    passenger = request.form.get("passenger")
    quantity = request.form.get("quantity")
    children = request.form.get("children")
    pets = request.form.get("pets")
    music = request.form.get("music")

    if driver == 'on':
        kwargs = {"point_A": a, "point_B": b}
        if quantity:
            kwargs['free_place'] = quantity
        if children:
            kwargs['children']=children
        if pets:
            kwargs['pets'] = pets
        if music:
            kwargs['music'] = music
        ride = Driver.query.filter_by(**kwargs).all()
        return render_template('driver_find.html', driver=ride)
    if passenger == 'on':
        kwargs = {"point_A": a, "point_B": b}
        if quantity:
            kwargs['pas_quantity'] = quantity
        if children:
            kwargs['children']=children
        if pets:
            kwargs['pets'] = pets
        if music:
            kwargs['music'] = music
        ride = Passenger.query.filter_by(**kwargs).all()
        return  render_template('pas_find.html', passenger=ride)



#подтвердление выбора
@app.route('/change', methods=['GET']) # возможно объединить с find ride только метод пост
def select_ride():
    return render_template('change.html')

@app.route('/change/search', methods=['POST']) # возможно объединить с find ride только метод пост
def selected_ride():
    phone = request.form.get("phone")
    ride_pas = Passenger.query.filter_by(phone=phone).all()
    ride_driv = Driver.query.filter_by(phone=phone).all()
    print(ride_driv)
    return render_template('change_inf.html', driver=ride_driv, passenger=ride_pas)

@app.route('/change/search', methods=['GET']) # возможно объединить с find ride только метод пост
def change():
    passenger = request.args.get('a')
    driver = request.args.get('b')
    ride_pas = Passenger.query.filter_by(id=passenger).all()
    ride_driv = Driver.query.filter_by(id=driver).all()
    if passenger:
        idd = passenger
    elif driver:
        idd = driver
    return  render_template("editor.html", passenger=ride_pas, driver=ride_driv, id=idd )

@app.route('/change/search/edit', methods=['POST']) # возможно объединить с find ride только метод пост
def changes():
    id = request.form.get('id')
    point_A = request.form.get("point_A")
    point_B = request.form.get('point_B')
    car = request.form.get('car')
    free_place = request.form.get('free_place')
    pas_quantity = request.form.get("pas_quantity")
    children = request.form.get("children")
    pets = request.form.get("pets")
    music = request.form.get("music")
    phone = request.form.get("phone")
    if car:
        kwargs = {"id": id, "point_A": point_A, "point_B": point_B, "car": car, "free_place": free_place, "children": children, "pets": pets, "phone": phone}
        driver = Driver.query.filter_by(id=id).update(kwargs, synchronize_session='evaluate')
    else:
        kwargs = {"id": id, "point_A": point_A, "point_B": point_B, "pas_quantity": pas_quantity, "children": children, "pets": pets, "phone": phone}
        passenger = Passenger.query.filter_by(id=id).update(kwargs, synchronize_session='evaluate')
    db.session.commit()
    return render_template("start_page.html")

#Удалиь запись
@app.route('/change/search/delete', methods=['GET']) # возможно объединить с find ride только метод пост
def delete():
    flag = request.args.get('flag')
    id = request.args.get('delete')
    if flag:
        dele = Driver.query.filter_by(id=id).delete()
    else:
        dele = Passenger.query.filter_by(id=id).delete()
    db.session.commit()
    return render_template("start_page.html")



app.run(debug=True)