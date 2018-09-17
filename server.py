"""Water Tracker"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session)
import math
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABCD123456"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""
    # do i want to just login on this page? or a button that you clicked called login that redirects to a login page?

    return render_template("homepage.html")

# @app.route('/new_user')
# def new_user():


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect(f"/users/{new_user.user_id}")











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