from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from schedula_app import db

class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    user_fname = db.Column(db.String(100),nullable = True)
    user_lname = db.Column(db.String(100),nullable = True)
    user_phone = db.Column(db.String(100),nullable = False, unique=True)
    user_password = db.Column(db.String(200),nullable = True)
    user_img = db.Column(db.String(200),nullable = True)
    user_regdate = db.Column(db.DateTime(), default = datetime.utcnow)



class Task(db.Model):
    task_id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    task_item = db.Column(db.String(200),nullable = True)
    task_img = db.Column(db.String(200),nullable = True)
    task_priority = db.Column(db.Integer, db.ForeignKey('priority.priority_id'), nullable=True)
    task_status = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=True)
    task_date = db.Column(db.DateTime(), default = datetime.utcnow)
    task_user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)

    #Relationship
    taskdeets = db.relationship("User", backref = "userdeets")

class Priority(db.Model):
    priority_id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    priority_item = db.Column(db.String(200), nullable = True)

class Status(db.Model):
    status_id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    status_item = db.Column(db.String(200), nullable = True)

class Contact(db.Model):
    contact_id=db.Column(db.Integer, autoincrement=True,primary_key=True) 
    contact_name=db.Column(db.String(150),nullable=False)   
    contact_phone=db.Column(db.String(40),nullable=False)
    contact_mail=db.Column(db.String(100),nullable=False)
    contact_message=db.Column(db.Text(),nullable=False)
    contact_date = db.Column(db.DateTime(), default=datetime.utcnow)

