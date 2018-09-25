"""Water Tracker"""

from sqlalchemy import func
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, flash
import math

from datetime import datetime
from time import localtime
import pytz
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Water, calculate_user_intake


app = Flask(__name__)

app.secret_key = "ABCD123456"

app.jinja_env.undefined = StrictUndefined



#######################I want to import this function from my model file


# def calculate_user_intake(weight, age):
#     """calculates how much user needs to be drinking""" 
    
#     need_to_drink = round(((weight/2.2)*age)/28.3,2)
#     # num_cups = math.ceil(need_to_drink/8)
     
#     return need_to_drink
###############################


@app.route('/')
def index():
    """Homepage"""

    if session.get('user_id') != None:
        return redirect('/app_page')
    else:
        return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    fname = request.form["fname"]
    lname = request.form["lname"]
    weight = int(request.form["weight"])
    age = int(request.form["age"])
    email = request.form["email"]
    password = request.form["password"]
    # zipcode = request.form["zipcode"]

    email_exist = db.session.query(User.email).filter(User.email==email).one_or_none() 

    # check to see if account already exists
    # if email == db.session.query(User.email).filter(User.email==email).first()[0]:
    #     flash("ACCOUNT ALREADY EXIST!")
    #     return redirect("/register")
    if email_exist and email == email_exist[0]:
            flash("ACCOUNT ALREADY EXIST!")
            return redirect("/register")
    else:
        new_user = User(fname=fname, lname=lname, weight=weight, age=age, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

    ############change the flash to a javascript alert 2nd sprint#########
    flash(f"User {email} added")
    return redirect('/')
    # return redirect(f"/users/{new_user.user_id}")

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


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

    flash("Login Successful")
    return redirect("/app_page")
    # print(session['user_id'])


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    del session["user_fname"]
    return redirect("/")


@app.route('/app_page')
def app_page():
    """this is the app"""

    user_id = session["user_id"]
    fname = session["user_fname"]
    total = db.session.query(func.sum(Water.ounces)).filter_by(user_id=user_id).scalar() #how much they've drank in general
    current_time = datetime.now().astimezone(pytz.timezone('US/Pacific'))
    current_date = current_time.date()

    total_water_today = db.session.query(func.sum(Water.ounces)).filter(Water.user_id==user_id, Water.time_updated >= current_date).scalar()

    if total_water_today != None:
        total_cups_today = round((total_water_today/8),2)
    else:
        total_water_today = 0
        total_cups_today = 0

    user = User.query.filter_by(user_id=user_id).first()
    user_goal_oz = calculate_user_intake(user.weight, user.age)
    user_goal_cups = round((user_goal_oz/8), 2)

    # session["user_goal"] = user_goal_oz
    # user_goal = session["user_goal"]

    if total_water_today > user_goal_oz:
        flash("yay you're met your daily goal!")

    return render_template("app_page.html", current_date=current_date, total_water_today=total_water_today, total_cups_today=total_cups_today, fname=fname, user_goal_oz=user_goal_oz, user_goal_cups=user_goal_cups)

@app.route('/add-water', methods=['POST'])
def add_water():
    "Adds water to daily total"

    user_id = session["user_id"]
    drink = int(request.form['drink'])
    time_updated = datetime.now()
    new_drink = Water(ounces=drink, user_id=user_id, time_updated=time_updated)

    db.session.add(new_drink)
    db.session.commit()

    return redirect('/app_page')


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