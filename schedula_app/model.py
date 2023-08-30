from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from schedula_app import db

class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    admin_fname = db.Column(db.String(100),nullable = True)
    admin_lname = db.Column(db.String(100),nullable = True)
    admin_username = db.Column(db.String(100),nullable = False, unique=True)
    admin_password = db.Column(db.String(200),nullable = True)
    admin_regdate = db.Column(db.DateTime(), default = datetime.utcnow)


class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    user_fname = db.Column(db.String(100),nullable = True)
    user_lname = db.Column(db.String(100),nullable = True)
    user_phone = db.Column(db.String(100),nullable = False, unique=True)
    user_password = db.Column(db.String(200),nullable = True)
    user_regdate = db.Column(db.DateTime(), default = datetime.utcnow)

    #Relationship
    userdeets = db.relationship("Task", backref = "taskdeets")


class Task(db.Model):
    task_id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    task_item = db.Column(db.String(200),nullable = True)
    task_date = db.Column(db.DateTime(), default = datetime.utcnow)

    #Relationship
    taskdeets = db.relationship("User", backref = "userdeets")
