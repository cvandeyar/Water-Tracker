"""Water Tracker"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session)
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCD123456"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""
    # do i want to just login on this page? or a button that you clicked called login that redirects to a login page?

    return render_template("homepage.html")

@app.route('/user-profile', methods=['POST'])
def user_profile():
    """Shows user profile after they login. Includes previous stats, shows goal for the day, how much they have left to drink to meet their goal"""

    return render_template("user-profile.html")

@app.route('/login')
def login():
    """Login page
        user gets sent here to login into their profile
    """

@app.route('/new-user')
def new_user():
    """new user creates profile"""






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