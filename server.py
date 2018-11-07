"""Water Tracker"""

from sqlalchemy import func
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, flash, jsonify
import math
from datetime import datetime, timedelta
from time import localtime
import pytz
from model import connect_to_db, db, User, Water
import config



app = Flask(__name__)

app.secret_key = config.app_secret_key

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    if session.get('user_id') != None:
        return redirect('/app_page')
    else:
        return render_template("index.html")


@app.route('/register')
def register_form():
    """Show form for user signup."""

    TIMEZONES = pytz.all_timezones

    return render_template("register_form.html", timezones=TIMEZONES)


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    fname = request.form["fname"]
    lname = request.form["lname"]
    weight = int(request.form["weight"])
    age = int(request.form["age"])
    email = request.form["email"]
    password = request.form["password"]
    time_zone = request.form["timezone"]

    email_exist = db.session.query(User.email).filter(User.email==email).one_or_none() 

    if email_exist and email == email_exist[0]:
            flash("ACCOUNT ALREADY EXIST!")
            return redirect("/register")
    else:
        new_user = User(fname=fname, lname=lname, weight=weight, age=age, email=email, password=password, time_zone=time_zone)

        db.session.add(new_user)
        db.session.commit()

    flash(f"User {email} added")
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User does not exist. Please create account")
        return redirect("/register")

    if user.password != password:
        flash("Password does not match our records")
        return redirect("/") 

    session["user_id"] = user.user_id
    session["user_fname"] = user.fname
    session["user_timezone"] = user.time_zone

    flash("Login Successful")
    return redirect("/app_page")

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    del session["user_fname"]
    del session["user_timezone"]
    return redirect("/")


@app.route('/app_page')
def app_page():
    """this is the app"""

    user_id = session["user_id"]
    fname = session["user_fname"]
    time_zone = session["user_timezone"]
    
    current_time = datetime.now().astimezone(pytz.timezone(time_zone))

    current_date = current_time.date()

    total_water_today = db.session.query(func.sum(Water.ounces)).filter(Water.user_id==user_id, Water.time_updated >= current_date).scalar()

    if total_water_today != None:
        total_cups_today = round((total_water_today/8),2)
    else:
        total_water_today = 0
        total_cups_today = 0

    user = User.query.filter_by(user_id=user_id).first()

    user_goal_oz = User.calculate_user_intake(user.weight, user.age)

    user_goal_cups = round((user_goal_oz/8), 2)

    IP_token = config.token

    return render_template("app_page.html", current_date=current_date, total_water_today=total_water_today, total_cups_today=total_cups_today, fname=fname, user_goal_oz=user_goal_oz, user_goal_cups=user_goal_cups, time_zone=time_zone, IP_token=IP_token)


@app.route('/add-water', methods=['POST'])
def add_water():
    """Adds water to daily total"""

    user_id = session['user_id']
    drink = request.form.get('drink')
    postal = request.form.get('postal')
    time_updated = datetime.now()
    new_drink = Water(ounces=drink, user_id=user_id, time_updated=time_updated, postal=postal)

    db.session.add(new_drink)
    db.session.commit()
 
    time_zone = session["user_timezone"]
    
    current_time = datetime.now().astimezone(pytz.timezone(time_zone))

    current_date = current_time.date()

    total_water_today = db.session.query(func.sum(Water.ounces)).filter(Water.user_id==user_id, Water.time_updated >= current_date).scalar()

    if int(total_water_today) != None or int(total_water_today) != 0:
        total_cups_today = round((total_water_today/8),2)
    else:
        total_water_today = 0
        total_cups_today = 0

    print('user id', user_id)
    print('current date', current_date)
    return f'Current Water Count: {total_water_today} Oz ({total_cups_today} Cups)'
    
#############################################

def chart_query(user_id, filter_name):
    """charts filter"""

    filter_dict = {
        'months': ('month', '%b %Y'),
        'weeks': ('week', '%D'),
        'days': ('day', '%D'),
    }
    trunc_type, time_format = filter_dict[filter_name]

    line_chart = (
        db.session.query(
            func.date_trunc(trunc_type, Water.time_updated),
            func.sum(Water.ounces)
        )
        .group_by(func.date_trunc(trunc_type, Water.time_updated))
        .order_by(func.date_trunc(trunc_type, Water.time_updated))
        .filter(Water.user_id==user_id)
        .all()
    )

    prev_date_time = None
    time_parameter = []  
    qty = []

    for item in line_chart:

        if prev_date_time!=None:
            cur_date = next_date(prev_date_time, trunc_type)

            while cur_date<item[0]:
                time_parameter.append(cur_date.strftime(time_format))
                qty.append(0)
                cur_date=next_date(cur_date, trunc_type)
        time_parameter.append(item[0].strftime(time_format))
        qty.append(item[1])
        prev_date_time = item[0]


    return time_parameter, qty

def next_date(date_time_input, interval):
    """updates goals total by filter"""

    if interval=='day':
        return date_time_input+timedelta(days=1)

    elif interval=='week':
        return date_time_input+timedelta(days=7)

    elif interval=='month':
        
        a = date_time_input+timedelta(days=31)
        next_month = a.replace(day=1)
        return next_month

#############################################
@app.route('/line_chart.json')
def line_chart():
    """Summary of intake in graphs"""

    user_id = session["user_id"]
    filter_name = request.args.get('filter_name')
    print("filter name is", filter_name)

    user = User.query.filter_by(user_id=user_id).one()
    user_goal_oz = User.calculate_user_intake(user.weight, user.age)

    goal_multiplier = {
        'months': 30,
        'weeks': 7,
        'days': 1,
    }

    user_goal_oz = user_goal_oz*goal_multiplier[filter_name]

    time_parameter, qty = chart_query(user_id, filter_name)
    print(chart_query)

    return jsonify(user_goal_oz=user_goal_oz, time_parameter=time_parameter, qty=qty)

@app.route('/pie-chart.json')
def pie_chart_data():
    """pie chart for postal data"""

    user_id = session["user_id"]

    pie_chart_query = db.session.query(Water.postal, func.count(Water.postal)).filter(Water.user_id==user_id).group_by(Water.postal).all()

    print('pie_chart_query, ', pie_chart_query)
    postal = []  
    qty = []
    for item1, item2 in pie_chart_query:

        if item1 is not None:
            postal.append(item1)
        if item2 is not 0:
            qty.append(item2)

    print('Postal: ', postal)
    print('Qty: ', qty)    

    return jsonify(postal=postal, qty=qty)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')