"""Water Tracker"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, flash
import math
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Water


app = Flask(__name__)

app.secret_key = "ABCD123456"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    fname = request.form["fname"]
    lname = request.form["fname"]
    weight = int(request.form["weight"])
    age = int(request.form["age"])
    # gender = request.form["gender"]
    email = request.form["email"]
    password = request.form["password"]
    # zipcode = request.form["zipcode"]

    new_user = User(fname=fname, lname=lname, weight=weight, age=age, email=email, password=password) #gender=gender

    db.session.add(new_user)
    db.session.commit()

    ############change the flash to a javascript alert 2nd sprint#########
    flash(f"User {email} added")
    return redirect('/')
    # return redirect(f"/users/{new_user.user_id}")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()


    ############maybe do some AJAX here for sprint 2 so don't have to redirect so much############
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login") 

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")











def calculate_user_intake(weight, age):
    """calculates how much user needs to be drinking""" 
    
    need_to_drink = round(((weight/2.2)*age)/28.3,2)
    num_cups = math.ceil(need_to_drink/8)
        
    return f"You need to drink about {need_to_drink}Oz which is about {num_cups} cups a day"



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