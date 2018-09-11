"""Models and database functions for Water Tracker project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# Model definitions

class User(db.Model):
    """User of water intake website"""

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} weight={self.weight} age={self.age} gender={self.gender} email={self.email} password={self.password}>"

class Water_intake(db.Model):
    """Water intake of water intake website"""

    __tablename__= "water_intakes"

    water_intake_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    amount_drank = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):

        return f"<Water_intake water_intake_id={self.water_intake_id} time={self.time} amount_drank={self.amount_drank} user_id={self.user_id}>"  


class Bathroom_use(db.Model):
    """Bathroom use of water intake website"""

    __tablename__= "bathroom_use"

    bathroom_use_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):

        return f"<Bathroom_use bathroom_use_id={self.bathroom_use_id} time={self.time} color={self.color} user_id={self.user_id}>"


#################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///water'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")