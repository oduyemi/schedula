import os, random, string
from flask import render_template, redirect, request, jsonify, session, flash, url_for
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from schedula_app import starter, db
from schedula_app.model import User
from forms import UserRegForm, LoginForm



from schedula_app import starter

def generate_name():
    global filename
    filename = random.sample(string.ascii_lowercase,10)
    return "".join(filename) 


#       --  E R R O R   H A N D L E R S  --

@starter.errorhandler(404)
def page_not_found(e):
    return render_template("user/error404.html"), 404

@starter.errorhandler(500)
def internal_server_error(e):
    return render_template("error500.html"), 500

@starter.errorhandler(405)
def method_not_allowed(e):
    if request.path.startswith("/api/"):
        return jsonify(message="Method Not Allowed"), 405
    else:
        return render_template("error405.html"), 405   
    

#        --  R O U T E S --

@starter.route("/", strict_slashes = False)
def home():
    return render_template("user/index.html")

@starter.route("/app", strict_slashes = False)
def app():
    return render_template("user/app.html")

@starter.route("/register", methods = ["POST", "GET"], strict_slashes = False)
def userReg():
    form = UserRegForm()
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        phone = request.form.get("phone")
        password = request.form.get("password")
        hashedpwd = generate_password_hash(password)

        if fname !="" and lname != "" and phone != "" and password !="":
            new_user=User(user_fname = fname, user_lname = lname, user_phone = phone, password_hash = hashedpwd)
            db.session.add(new_user)
            userid=new_user.user_id
            session["user"] = userid
            flash(f"Account created for you, '{fname}'! Please proceed to LOGIN ", "success")
        else:
            flash("You must fill the form correctly to register", "danger")
    else:
        return render_template("user/register.html", form = form, title="Register - Schedula")
    

@starter.route("/login", strict_slashes = False)
def userLogin():
    form = LoginForm()
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")
        deets = db.session.query(User).filter(User.user_phone == phone).first() 
        if deets != None:
            pwd_indb = deets.user_password
            chk = check_password_hash(pwd_indb, password)
            if chk:
                id = deets.user_id
                session["user"] = id
                return redirect(url_for("app"))
            else:
                flash("Incorrect username or password")
                return redirect(url_for("userLogin"))
    else:
        return render_template("user/login.html", form = form, title = "Login - Schedula")
    
@starter.route("/logout", strict_slashes = False)
def userlogout():
    if session.get("user") != None:
        session.pop("user",None)
    return redirect('/login')



@starter.route("/profile", strict_slashes = False)
def userProfile():
    return render_template("user/profile.html")