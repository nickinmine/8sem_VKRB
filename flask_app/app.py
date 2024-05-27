from flask import Flask, render_template, redirect, request, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import func, cast, Numeric
from waitress import serve
from config.config import Config, db
from model.FuelPriceLimit import FuelPriceLimit
from model.FuelPrice import FuelPrice
from model.Admin import Admin
from model.Azs import Azs
from datetime import datetime, timedelta
import numpy
import random
import hashlib
import uuid
import geojson

app = Flask(__name__, static_folder='static')
login_manager = LoginManager(app)


def create_app(config):
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    return app


@login_manager.user_loader
def load_user(user_uuid):
    user = Admin.query.filter_by(user_uuid=user_uuid).first()
    return user


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/map", methods=['GET'])
def map_page():
    return render_template('map.html')


@app.route("/statistics", methods=['GET'])
def statistics():
    date1 = datetime.utcnow() + timedelta(-29.875)
    date2 = datetime.utcnow() + timedelta(0.125)
    avg_prices_today = (
        FuelPrice.query.with_entities(func.round(cast(func.avg(FuelPrice.ai_92), Numeric()), 2).label('avg_ai_92'),
                                      func.round(cast(func.avg(FuelPrice.ai_95), Numeric()), 2).label('avg_ai_95'),
                                      func.round(cast(func.avg(FuelPrice.ai_98), Numeric()), 2).label('avg_ai_98'),
                                      func.round(cast(func.avg(FuelPrice.ai_100), Numeric()), 2).label('avg_ai_100'),
                                      func.round(cast(func.avg(FuelPrice.dt), Numeric()), 2).label('avg_dt'),
                                      func.round(cast(func.avg(FuelPrice.gas), Numeric()), 2).label('avg_gas'))
        .filter_by(date=date2.date()).first())
    avg_prices_month = (
        FuelPrice.query.with_entities(func.round(cast(func.avg(FuelPrice.ai_92), Numeric()), 2).label('avg_ai_92'),
                                      func.round(cast(func.avg(FuelPrice.ai_95), Numeric()), 2).label('avg_ai_95'),
                                      func.round(cast(func.avg(FuelPrice.ai_98), Numeric()), 2).label('avg_ai_98'),
                                      func.round(cast(func.avg(FuelPrice.ai_100), Numeric()), 2).label('avg_ai_100'),
                                      func.round(cast(func.avg(FuelPrice.dt), Numeric()), 2).label('avg_dt'),
                                      func.round(cast(func.avg(FuelPrice.gas), Numeric()), 2).label('avg_gas'))
        .filter(FuelPrice.date.between(date1.date(), date2.date())).first())
    min_prices = (
        FuelPrice.query.with_entities(func.min(FuelPrice.ai_92).label('min_ai_92'),
                                      func.min(FuelPrice.ai_95).label('min_ai_95'),
                                      func.min(FuelPrice.ai_98).label('min_ai_98'),
                                      func.min(FuelPrice.ai_100).label('min_ai_100'),
                                      func.min(FuelPrice.dt).label('min_dt'),
                                      func.min(FuelPrice.gas).label('min_gas'))
        .filter(FuelPrice.date.between(date1.date(), date2.date())).first())
    max_prices = (
        FuelPrice.query.with_entities(func.max(FuelPrice.ai_92).label('max_ai_92'),
                                      func.max(FuelPrice.ai_95).label('max_ai_95'),
                                      func.max(FuelPrice.ai_98).label('max_ai_98'),
                                      func.max(FuelPrice.ai_100).label('max_ai_100'),
                                      func.max(FuelPrice.dt).label('max_dt'),
                                      func.max(FuelPrice.gas).label('max_gas'))
        .filter(FuelPrice.date.between(date1.date(), date2.date())).first())
    return render_template('statistics.html', avg_prices_month=avg_prices_month, avg_prices_today=avg_prices_today,
                           min_prices=min_prices, max_prices=max_prices, date_now=date2.date())


@app.route("/stations", methods=['GET'])
def azs():
    stations = Azs.query.order_by(Azs.brand_name).all()
    date = datetime.utcnow() + timedelta(0.125)
    date = date.date()
    for station in stations:
        price = FuelPrice.query.filter_by(azs_id=station.azs_id, date=date).first()
        if price:
            station.ai_92 = price.ai_92
            station.ai_95 = price.ai_95
            station.ai_98 = price.ai_98
            station.ai_100 = price.ai_100
            station.dt = price.dt
            station.gas = price.gas
    return render_template('stations.html', stations=stations, date=date)


@app.route("/users", methods=['GET'])
@login_required
def users():
    user_list = Admin.query.all()
    return render_template('users.html', user_list=user_list)


@app.route("/users/new", methods=['POST'])
@login_required
def add_new_user():
    user_password = hashlib.md5(request.form['user_password'].encode())
    user = Admin(user_uuid=uuid.uuid4(), user_login=request.form['user_login'],
                 user_password=user_password.hexdigest(), user_name=request.form['user_name'])
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route("/users/delete", methods=['POST'])
@login_required
def delete_user():
    user = Admin.query.filter_by(user_uuid=request.form['user_uuid']).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/users')


@app.route("/prices", methods=['GET', 'POST'])
@login_required
def prices():
    fuelPriceLimits = FuelPriceLimit.query.first()
    if request.method == 'POST':
        if fuelPriceLimits:
            fuelPriceLimits.ai_92_min = request.form['ai_92_min']
            fuelPriceLimits.ai_92_max = request.form['ai_92_max']
            fuelPriceLimits.ai_95_min = request.form['ai_95_min']
            fuelPriceLimits.ai_95_max = request.form['ai_95_max']
            fuelPriceLimits.ai_98_min = request.form['ai_98_min']
            fuelPriceLimits.ai_98_max = request.form['ai_98_max']
            fuelPriceLimits.ai_100_min = request.form['ai_100_min']
            fuelPriceLimits.ai_100_max = request.form['ai_100_max']
            fuelPriceLimits.dt_min = request.form['dt_min']
            fuelPriceLimits.dt_max = request.form['dt_max']
            fuelPriceLimits.gas_min = request.form['gas_min']
            fuelPriceLimits.gas_max = request.form['gas_max']
            fuelPriceLimits.limits_updating_date = datetime.utcnow() + timedelta(0.125)
            db.session.commit()
        return redirect('/prices')
    return render_template('prices.html', fuelPriceLimits=fuelPriceLimits)


@app.route("/prices/update", methods=['POST'])
@login_required
def prices_update():
    fuelPriceLimits = FuelPriceLimit.query.first()
    azs_count = Azs.query.count()
    date = datetime.utcnow() + timedelta(0.125)
    fuelPriceLimits.prices_updating_date = date
    db.session.commit()
    if fuelPriceLimits:
        #for j in range(21, 35):
        #    date1 = date + timedelta(j)
        for i in range(azs_count):
            ai_92 = numpy.round(random.uniform(fuelPriceLimits.ai_92_min, fuelPriceLimits.ai_92_max), 2)
            ai_95 = numpy.round(random.uniform(fuelPriceLimits.ai_95_min, fuelPriceLimits.ai_95_max), 2)
            ai_98 = numpy.round(random.uniform(fuelPriceLimits.ai_98_min, fuelPriceLimits.ai_98_max), 2)
            ai_100 = numpy.round(random.uniform(fuelPriceLimits.ai_100_min, fuelPriceLimits.ai_100_max), 2)
            dt = numpy.round(random.uniform(fuelPriceLimits.dt_min, fuelPriceLimits.dt_max), 2)
            gas = numpy.round(random.uniform(fuelPriceLimits.gas_min, fuelPriceLimits.gas_max), 2)
            fuelPrice = FuelPrice(azs_id=i + 2, date=date.date(), ai_92=ai_92, ai_95=ai_95,
                                  ai_98=ai_98, ai_100=ai_100, dt=dt, gas=gas)
            db.session.add(fuelPrice)
            db.session.commit()
    return redirect('/prices')


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if 'active_user_uuid' in session:
        return redirect("/prices")
    if request.method == 'POST':
        login = request.form['login']
        password = hashlib.md5(request.form['password'].encode())
        if login and password:
            user = Admin.query.filter_by(user_login=login, user_password=password.hexdigest()).first()
            if user:
                session['active_user_uuid'] = user.user_uuid
                login_user(user)
                return redirect("/prices")
    return render_template('auth.html')


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/")


@app.route("/api/v1/prices", methods=['GET'])
def api_prices():
    stations = Azs.query.order_by(Azs.brand_name).all()
    date = datetime.utcnow() + timedelta(0.125)
    features = []
    for station in stations:
        price = FuelPrice.query.filter_by(azs_id=station.azs_id, date=date.date()).first()
        feature = geojson.Feature(
            geometry=geojson.Point((float(station.longitude), float(station.latitude))),
            properties={"brand": station.brand_name, "address": station.address, "ai_92": price.ai_92,
                        "ai_95": price.ai_95, "ai_98": price.ai_98, "ai_100": price.ai_100,
                        "dt": price.dt, "gas": price.gas}
        )
        features.append(feature)
    feature_collection = geojson.FeatureCollection(features)
    return jsonify(geojson.loads(geojson.dumps(feature_collection)))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/auth')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html', error=error), 404


app = create_app(Config)
serve(app, host='0.0.0.0', port=5000)
