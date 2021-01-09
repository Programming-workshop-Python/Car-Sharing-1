from flask import render_template, request, redirect, url_for, Blueprint
from DataBase.database import Passenger, Driver
from DataBase.AddData import add_data
from settings import app, db, logger
db.create_all()
posts_controller = Blueprint(name='posts_controller', import_name=__name__)

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
        try:
            add_data(driver)
        except Exception as exc:
            logger.warning('create action failed with errors: {exc}', exc_info=True)

    return redirect(url_for(".passenger_find", a=point_A, b=point_B, free_place=free_place, children=children, pets=pets))

@app.route('/create_ride_main/create_rider_inf', methods=['GET'])
def passenger_find():
    passenger = []
    a= request.args.get('a')
    b = request.args.get('b')
    pas_quant = request.args.get('free_place')
    chil = request.args.get('children')
    pets = request.args.get('pets')
    if pets == 'on':
        pets = 1
    else:
        pets = 0
    try:
        kwargs = {"point_A": a, "point_B": b, "pas_quantity": pas_quant, "children": chil, "pets": pets}
        print(pets)
        passengers = Passenger.query.filter_by(**kwargs).all()
    except Exception as exc:
        logger.warning('postgre_request exeption: {exc}', exc_info=True)
    return render_template("pas_find.html", passenger=passengers)

@app.route('/create_ride_main/create_rider_inf/selected', methods=['GET'])
def selected():
    return
#Создать запись пасажра?
@app.route('/create_ride_main/create_passenger', methods=['GET'])
def create_passenger():
    return render_template("pas_info.html")
passenger_find
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
        if pets == 'on':
            pets = 1
        else:
            pets = 0
        passenger = Passenger(point_A, point_B, pas_quantity, children, pets, music, phone)
        try:
            add_data(passenger)
        except Exception as exc:
            logger.warning('create action failed with errors: {exc}', exc_info=True)
    return redirect(url_for(".driver_find", a=point_A, b=point_B, pas_quantity=pas_quantity, children=children, pets=pets))

@app.route('/create_ride_main/create_passenger_inf', methods=['GET'])
def driver_find():
    passenger = []
    a= request.args.get('a')
    b = request.args.get('b')
    free_place = request.args.get('pas_quantity')
    chil = request.args.get('children')
    pets = request.args.get('pets')
    try:
        kwargs = {"point_A": a, "point_B": b, "free_place": free_place, "children": chil, "pets": pets}
        driver = Driver.query.filter_by(**kwargs).all()
    except Exception as exc:
        logger.warning('postgre_request exeption: {exc}', exc_info=True)
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
        try:
            ride = Passenger.query.filter_by(**kwargs).all()
        except Exception as exc:
            logger.warning('postgre_request exeption: {exc}', exc_info=True)
        return  render_template('pas_find.html', passenger=ride)



#подтвердление выбора
@app.route('/change', methods=['GET']) # возможно объединить с find ride только метод пост
def select_ride():
    return render_template('change.html')

@app.route('/change/search', methods=['POST']) # возможно объединить с find ride только метод пост
def selected_ride():
    phone = request.form.get("phone")
    try:
        ride_pas = Passenger.query.filter_by(phone=phone).all()
        ride_driv = Driver.query.filter_by(phone=phone).all()
    except Exception as exc:
        logger.warning('postgre_request exeption: {exc}', exc_info=True)
    return render_template('change_inf.html', driver=ride_driv, passenger=ride_pas)

@app.route('/change/search', methods=['GET']) # возможно объединить с find ride только метод пост
def change():
    passenger = request.args.get('a')
    driver = request.args.get('b')
    try:
        ride_pas = Passenger.query.filter_by(id=passenger).all()
        ride_driv = Driver.query.filter_by(id=driver).all()
    except Exception as exc:
        logger.warning('postgre_request exeption: {exc}', exc_info=True)
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
        try:
            kwargs = {"id": id, "point_A": point_A, "point_B": point_B, "car": car, "free_place": free_place, "children": children, "pets": pets, "phone": phone}
            driver = Driver.query.filter_by(id=id).update(kwargs, synchronize_session='evaluate')
        except Exception as exc:
            logger.warning('postgre_update exeption: {exc}', exc_info=True)
    else:
        try:
            kwargs = {"id": id, "point_A": point_A, "point_B": point_B, "pas_quantity": pas_quantity, "children": children, "pets": pets, "phone": phone}
            passenger = Passenger.query.filter_by(id=id).update(kwargs, synchronize_session='evaluate')
        except Exception as exc:
            logger.warning('postgre_update exeption: {exc}', exc_info=True)
    db.session.commit()
    return render_template("start_page.html")

#Удалиь запись
@app.route('/change/search/delete', methods=['GET']) # возможно объединить с find ride только метод пост
def delete():
    flag = request.args.get('flag')
    id = request.args.get('delete')
    if flag:
        try:
            dele = Driver.query.filter_by(id=id).delete()
        except Exception as exc:
            logger.warning('postgre_del exeption: {exc}', exc_info=True)
    else:
        try:
            dele = Passenger.query.filter_by(id=id).delete()
        except Exception as exc:
            logger.warning('postgre_del exeption: {exc}', exc_info=True)
    db.session.commit()
    return render_template("start_page.html")