from sqlalchemy import func
from model import User
from model import Water
# from model import Bathroom

from model import connect_to_db, db
from server import app

def load_users():

    User.query.delete()

    for row in open(user_filename):
        row = row.rstrip()

        user_id, fname, lname, weight, age, gender, email, password = row.split('|')

        user = User(user_id=user_id, fname=fname, lname=lname, weight=weight, age=age, gender=gender, email=email, password=password)

        db.session.add(user)

    db.session.commit()

def load_water():

    Water.query.delete()

    for row in open(water_filename):
        row = row.rstrip()

        water_intake_id, time_updated, ounces, user_id = row.split('|')

        water = Water(water_intake_id=water_intake_id, time_updated=time_updated, ounces=ounces, user_id=user_id)

        db.session.add(water)

    db.session.commit()

# def load_bathroom():

#     Bathroom.query.delete()

#     for row in open('seed_data/u.bathroom'):
#         row = row.rstrip()

#         bathroom_use_id, time, color, user_id = row.split('|')

#         bathroom = Bathroom(bathroom_use_id=bathroom_use_id, time=time, color=color, user_id=user_id)

#         db.session.add(bathroom)

#     db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    user_filename = 'seed_data/u.user'
    water_filename = 'seed_data/u.water'
    load_users()
    load_water()
    set_val_user_id()
    # load_bathroom()