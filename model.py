from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import localtime
import pytz
import math

db = SQLAlchemy()


def calculate_user_intake(weight, age):
    """calculates how much user needs to be drinking""" 
    
    need_to_drink = round(((weight/2.2)*age)/28.3,2)
    # num_cups = math.ceil(need_to_drink/8)
     
    return need_to_drink #, num_cups
        
    # return f"You need to drink about {need_to_drink}Oz which is about {num_cups} cups a day"


# Model definitions

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

    def __repr__(self):

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} weight={self.weight} age={self.age} email={self.email} password={self.password}>"

class Water(db.Model):
    """Water intake of water intake website"""

    __tablename__= "water_consumption"

    water_intake_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_updated = db.Column(db.DateTime, default=datetime.now())
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