import csv
import logging
from os import path

from flask_login import current_user

from . import db
from .models import User
from .schemas import Scale
from .settings import BASE_PATH


def reset_completed_status():
    count = 0
    for user in db.session.query(User).filter(User.completed.is_(True)):
        user.completed = False
        count += 1
    db.session.commit()

    logging.info(f"Updated {count} users")


def get_user_by_name(name):
    return db.session.query(User).filter(User.username == name).first()


def get_user_by_email(email):
    return db.session.query(User).filter(User.email == email).first()


def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def update_current_user_selection(instrument, grade):
    current_user.last_instrument = instrument
    current_user.last_grade = grade
    db.session.commit()


def user_completed(completed):
    current_user.completed = completed
    db.session.commit()


def get_scales_from_csv(instrument, grade):
    filename = path.join(BASE_PATH, "scales.csv")

    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        filtered_csv = filter(lambda r: instrument == r[0] and grade == r[1], csvreader)
        rows = [row for row in filtered_csv]

    return [Scale(instrument, grade, row[2], row[3], row[4] == "T") for row in rows]
