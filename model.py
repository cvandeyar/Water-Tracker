from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import localtime
import pytz
import math

db = SQLAlchemy()

class User(db.Model):
    """User of water intake website"""

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    time_zone = db.Column(db.String(100), nullable=False)

    @classmethod
    def calculate_user_intake(cls, weight, age):
        """calculates how much user needs to be drinking in ounces""" 

        a = weight/2.2

        if age < 30:
            b = a * 40
        elif age >=30 and age < 55:
            b = a * 35
        elif age >= 55: 
            b = a * 30

        c = b/28.3

        need_to_drink = round(c, 2)

        return need_to_drink


    def __repr__(self):

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} weight={self.weight} age={self.age} email={self.email} password={self.password} time_zone={self.time_zone}>"

class Water(db.Model):
    """Water intake of water intake website"""

    __tablename__= "water_consumption"

    water_intake_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_updated = db.Column(db.DateTime, nullable=False)
    # change ounces to qty!!!!!!!!
    ounces = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # def time_entered(self):
    #     return time_updated.astimezone(pytz.timezone('US/Pacific'))

    user = db.relationship('User', backref='water')

    # def convert_timezone(self):
    #     time_updated = self.time_updated.astimezone(pytz.timezone('US/Pacific')).ctime()
    #     return time_updated

    def __repr__(self):

        return f"""<Water_intake 
        water_intake_id={self.water_intake_id} 
        time_updated={self.time_updated} 
        ounces={self.ounces} 
        user_id={self.user_id}>"""

# class Bathroom(db.Model):
#     """Bathroom use of water intake website"""

#     __tablename__= "bathroom_use"

#     bathroom_use_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     time = db.Column(db.DateTime, default=datetime.now())
#     color = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

#     user = db.relationship('User', backref='bathroom')

#     def __repr__(self):

#         return f"<Bathroom_use bathroom_use_id={self.bathroom_use_id} time={self.time} color={self.color} user_id={self.user_id}>"


#################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///water'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print("Connected to DB.")