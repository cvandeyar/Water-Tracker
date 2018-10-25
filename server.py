"""Water Tracker"""

from sqlalchemy import func
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, flash, jsonify
import math
from datetime import datetime
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
        return render_template("homepage.html")


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

    ############change the flash to a javascript alert 2nd sprint#########
    flash(f"User {email} added")
    return redirect('/')
    # return redirect(f"/users/{new_user.user_fname}")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()


    ############maybe do some AJAX here for sprint 2 so don't have to redirect so much############
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
    # print(session['user_id'])


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

    # total = db.session.query(func.sum(Water.ounces)).filter_by(user_id=user_id).scalar() #how much they've drank in general
    
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


    # if total_water_today > user_goal_oz:
    # flash("yay you're met your daily goal!")

    # bar_chart = db.session.query(func.date(Water.time_updated),func.sum(Water.ounces)).group_by(func.date(Water.time_updated)).order_by(func.date(Water.time_updated)).filter(Water.user_id==user_id, Water.time_updated==current_date).all()

    # bar_chart = db.session.query(func.date_trunc('month', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('month', Water.time_updated)).order_by(func.date_trunc('month', Water.time_updated)).filter(Water.user_id==user_id).all()

    # bar_chart = db.session.query(func.date_trunc('week', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('week', Water.time_updated)).order_by(func.date_trunc('week', Water.time_updated)).filter(Water.user_id==user_id).all()

    # bar_chart = db.session.query(func.date_trunc('day', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('day', Water.time_updated)).order_by(func.date_trunc('day', Water.time_updated)).filter(Water.user_id==user_id).all()


    # time_parameter = []  
    # qty = []
    # for item in bar_chart:
    #     time_parameter.append(item[0].strftime('%a-%D'))
    #     qty.append(item[1])

    time_parameter = ['Today']
    qty = [total_water_today]


    IP_token = config.token

    return render_template("app_page.html", current_date=current_date, total_water_today=total_water_today, total_cups_today=total_cups_today, fname=fname, user_goal_oz=user_goal_oz, user_goal_cups=user_goal_cups, time_zone=time_zone, time_parameter=time_parameter, qty=qty, IP_token=IP_token)


# bar_chart = db.session.query(func.date(Water.time_updated),func.sum(Water.ounces)).group_by(func.date(Water.time_updated)).filter(Water.user_id==session["user_id"]).all()

# fmt = "%a-%D"




# this is for chart.js
# >>> test = db.session.query(func.date(Water.time_updated),func.sum(Water.ounces)).group_by(func.date(Water.time_updated))
# >>> test.all()
# [(datetime.date(2018, 9, 4), 4), (datetime.date(2018, 9, 1), 22), (datetime.date(2018, 9, 30), 164), (datetime.date(2018, 9, 2), 26), (datetime.date(2018, 9, 3), 18)]
# >>> test.filter(Water.user_id==1).all()
# [(datetime.date(2018, 9, 1), 4), (datetime.date(2018, 9, 30), 20), (datetime.date(2018, 9, 2), 4), (datetime.date(2018, 9, 3), 6)]

# >>> user1[3][0].strftime('%a-%D')
# 'Mon-09/03/18'






@app.route('/add-water', methods=['POST'])
def add_water():
    """Adds water to daily total"""

    user_id = session['user_id']
    drink = int(request.form.get('drink'))
    time_updated = datetime.now()
    new_drink = Water(ounces=drink, user_id=user_id, time_updated=time_updated)

    db.session.add(new_drink)
    db.session.commit()
 
    time_zone = session["user_timezone"]

    # total = db.session.query(func.sum(Water.ounces)).filter_by(user_id=user_id).scalar() #how much they've drank in general
    
    current_time = datetime.now().astimezone(pytz.timezone(time_zone))

    current_date = current_time.date()

    total_water_today = db.session.query(func.sum(Water.ounces)).filter(Water.user_id==user_id, Water.time_updated >= current_date).scalar()

    if total_water_today != None:
        total_cups_today = round((total_water_today/8),2)
    else:
        total_water_today = 0
        total_cups_today = 0



    # return redirect('/app_page')
    return f'Current Water Count: {total_water_today} Oz ( {total_cups_today} Cups)'


#############################################

def month_query(user_id):
    """organizes data by month"""

    line_chart = db.session.query(func.date_trunc('month', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('month', Water.time_updated)).order_by(func.date_trunc('month', Water.time_updated)).filter(Water.user_id==user_id).all()

    time_parameter = []  
    qty = []
    for item in line_chart:
        time_parameter.append(item[0].strftime('%b %Y'))
        qty.append(item[1])

    return time_parameter, qty

def week_query(user_id):
    """organizes data by week"""

    line_chart = db.session.query(func.date_trunc('week', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('week', Water.time_updated)).order_by(func.date_trunc('week', Water.time_updated)).filter(Water.user_id==user_id).all()

    time_parameter = []  
    qty = []
    for item in line_chart:
        time_parameter.append(item[0].strftime('%D'))
        qty.append(item[1])

    return time_parameter, qty

def day_query(user_id):
    """organizes data by day"""

    line_chart = db.session.query(func.date_trunc('day', Water.time_updated),func.sum(Water.ounces)).group_by(func.date_trunc('day', Water.time_updated)).order_by(func.date_trunc('day', Water.time_updated)).filter(Water.user_id==user_id).all()

    time_parameter = []  
    qty = []
    for item in line_chart:
        time_parameter.append(item[0].strftime('%D'))
        qty.append(item[1])

    return time_parameter, qty


# def current_day_query(user_id):
#     """shows current day drink amount"""


#     line_chart = db.session.query(func.date(Water.time_updated),func.sum(Water.ounces)).group_by(func.date(Water.time_updated)).order_by(func.date(Water.time_updated)).filter(Water.user_id==user_id).all()

#     time_parameter = []  
#     qty = []
#     for item in line_chart:
#         time_parameter.append(item[0].strftime('%D'))
#         qty.append(item[1])

#     return time_parameter, qty


# @app.route('/scatter_chart.json')
# def scatter_chart():
#     """makes scatter chart of consumption"""

#     user_id = session["user_id"]

#     if they chose month:
#         month_query(user_id)
#     elif they chose week:
#         week_query(user_id)
#     elif they chose week:
#         day_query(user_id)
#     else:
#         current_day_query(user_id)

#     return jsonify(scatter_chart_data)

# @app.route('/pie_chart.json')
# def pie_chart():
#     """makes pie chart of location"""

#     user_id = session["user_id"]

#     return jsonify(pie_chart_data)


#############################################
@app.route('/stat_page.json')
def stats():
    """Summary of intake in graphs"""

    user_id = session["user_id"]
    filter_name = request.args.get('filter_name')
    print("filter name is", filter_name)

    user = User.query.filter_by(user_id=user_id).first()
    user_goal_oz = User.calculate_user_intake(user.weight, user.age)

    # if filter_name == 'today':

    #     time_parameter, qty = current_day_query(user_id)

    if filter_name == 'days':

        time_parameter, qty = day_query(user_id)

    elif filter_name == 'weeks':
    
        time_parameter, qty = week_query(user_id)

    elif filter_name == 'months':
    
        time_parameter, qty = month_query(user_id)

    # return render_template("stat_page.html", user_goal_oz=user_goal_oz, time_parameter=time_parameter, qty=qty)

    return jsonify(user_goal_oz=user_goal_oz, time_parameter=time_parameter, qty=qty)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')