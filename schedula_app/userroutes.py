import os, random, string
from flask import render_template, redirect, request, jsonify, session, flash, url_for
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from schedula_app import starter, db
from schedula_app.model import User, Contact, Task
from forms import UserRegForm, LoginForm, ContactForm, PhoneForm



from schedula_app import starter
csrf = CSRFProtect(starter)


#       --  H A N D Y   F U N C T I O N S  --

def generate_name():
    global filename
    filename = random.sample(string.ascii_lowercase,10)
    return "".join(filename) 


def validatePhone(a):
    if not (a.isnumeric() or (a.startswith('+') and a[1:].isnumeric())):
        flash("Please enter a valid phone number", "danger")
        return False
    else:
        return True


def validatePasswordMatch(x, y):
    if x == y:
            flash("The passwords must match!", "danger")
            return True
    else:
        return False

#       --  E R R O R   H A N D L E R S  --

@starter.errorhandler(404)
def page_not_found(e):
    return render_template("user/error404.html"), 404

@starter.errorhandler(500)
def internal_server_error(e):
    return render_template("user/error500.html"), 500

@starter.errorhandler(405)
def method_not_allowed(e):
    if request.path.startswith("/api/"):
        return jsonify(message="Method Not Allowed"), 405
    else:
        return render_template("user/error405.html"), 405   
    

#        --  R O U T E S --

@starter.route("/", methods = ["POST", "GET"], strict_slashes = False)
def home():
    form = ContactForm()
    if request.method == "POST":
        name = request.form.get("contact_name")
        mail = request.form.get("mail")
        phone = request.form.get("phone")
        message = request.form.get("message")
        if name != "" and mail != "" and phone != "" and message != "":
            if validatePhone(phone):
                flash("You must fill the form correctly to register", "danger")
                return redirect("/#support")
            newContact = Contact(contact_name = name, contact_mail = mail, contact_phone = phone, contact_message = message)
            db.session.add(newContact)
            db.session.commit()
            flash(f"Thank you for reaching out to us, {name} We will get in touch with you shortly. ", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Please fill the form correctly ", "danger")
            return redirect(url_for("home"))
    else:
        return render_template("user/index.html", form = form)


@starter.route("/register", methods = ["POST", "GET"], strict_slashes = False)
def userReg():
    form = UserRegForm()
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        phone = request.form.get("phone")
        password = request.form.get("password")
        c_password = request.form.get("c_password")
        hashedpwd = generate_password_hash(password)        

        if fname !="" and lname != "" and phone != "" and password !="":
            if (validatePhone(phone) and validatePasswordMatch(password, c_password)):
                return redirect(url_for("userReg"))
               
            new_user = User(user_fname = fname, user_lname = lname, user_phone = phone, user_password= hashedpwd)
            db.session.add(new_user)
            db.session.commit()
            userid=new_user.user_id
            session['user']=userid
            flash(f"Account created for you, {fname}! Please proceed to LOGIN ", "success")
            return redirect(url_for("userLogin"))
        else:
            flash("You must fill the form correctly to register", "danger")
            return redirect(url_for("userReg"))
    else:
        return render_template("user/register.html", form = form, title="Register - Schedula")
    

@starter.route("/login", methods = ["POST", "GET"], strict_slashes = False)
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
                flash(f"Welcome back, {deets.user_fname}", "success")
                return redirect(url_for("app", id= id))
            else:
                flash("Incorrect username or password", "danger")
                return redirect(url_for("userLogin"))
        else:
            flash("You will need to create an account first", "danger")
            return redirect(url_for("userReg"))
    else:
        return render_template("user/login.html", form = form, title = "Login - Schedula")
    
@starter.route("/logout", strict_slashes = False)
def userLogout():
    if session.get("user") != None:
        session.pop("user",None)
    return redirect(url_for("home"))

@starter.route("/app/<int:id>", strict_slashes = False)
def app(id):
    info = User.query.get_or_404(id)
    t = Task.query.filter_by(task_user = info.user_id, task_priority = 1).all()
    tp = Task.query.filter_by(task_user = info.user_id, task_priority = 1).limit(3).all()
    m = Task.query.filter_by(task_user = info.user_id, task_priority = 2).all()
    md = Task.query.filter_by(task_user = info.user_id, task_priority = 2).limit(3).all()
    l = Task.query.filter_by(task_user = info.user_id, task_priority = 3).all()
    lt = Task.query.filter_by(task_user = info.user_id, task_priority = 3).limit(3).all()
    top = len(t)
    mid = len(m)
    least = len(l)
    total = len(t) + len(m) + len(l)
    if id:
        return render_template("user/app.html", info = info, top = top, mid = mid, least = least, total= total, t=tp, m=md, l=lt)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/addnew/<int:id>", methods = ["POST", "GET"], strict_slashes = False)
def addNew(id):
    info = User.query.get_or_404(id)
    if request.method == "POST":
        task = request.form.get("taskName")
        order = request.form.get("priority")
        file = request.files['taskImg']
        filename = file.filename 
        filetype = file.mimetype 
        allowed = [".png", ".jpg", ".jpeg", ".webp", ".aviv"]
        if task != "" and order != "" and filename != "":
            name, ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                img_task = generate_name()+ext
                file.save("schedula_app/static/assets/uploads/"+img_task)
                taskInfo = Task(task_item = task, task_priority = order, task_img = img_task, task_user=id, task_status = 1)
                db.session.add(taskInfo) 
                db.session.commit()
                flash("Item added", "success")
                return redirect(url_for("addNew", id = id))
            else:
                return "Images only!"
        else:
            flash("Please fill all fields")
            return redirect(url_for("addNew", id = id))

    else:
        return render_template("user/addnew.html", info = info)


@starter.route("/must-do-list/<int:id>", strict_slashes = False)
def must(id):
    info = User.query.get_or_404(id)
    todo = Task.query.filter_by(task_user = info.user_id, task_priority = 1).all()
    return render_template("user/must.html", info = info, todo = todo)


@starter.route("/should-do-list/<int:id>", strict_slashes = False)
def should(id):
    info = User.query.get_or_404(id)
    todo = db.session.query(Task).filter_by(task_user = info.user_id, task_priority = 2).all() 
    return render_template("user/should.html", info = info, todo = todo)


@starter.route("/could-do-list/<int:id>", strict_slashes = False)
def could(id):
    info = User.query.get_or_404(id)
    todo = db.session.query(Task).filter_by(task_user = info.user_id, task_priority = 3).all() 
    return render_template("user/could.html", info = info, todo = todo)


@starter.route("/delete/<int:id>", strict_slashes = False)
def deleteTodo(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    # current_url = request.url
    return redirect(request.referrer)

    

@starter.route("/profile/<int:id>", strict_slashes = False)
def userProfile(id):
    info = User.query.get_or_404(id)
    return render_template("user/profile.html", info = info)


@starter.route("/update/phone-number", methods = ["POST", "GET"], strict_slashes = False)
def updatePhone():
    form = PhoneForm()
    if request.method == "GET":
        return render_template("user/update-phone.html", form = form)
    else:
        info = db.session.query(User).get(id)
        phone = request.form.get("phone")
        if phone != "":
            if validatePhone(phone):
                return redirect(url_for("updatePhone"))
            info.user_phone = phone
            db.session.commit()
            flash(f"Your phone number has been updated", "success")
            return redirect(f"/profile/{id}")
        else:
            flash("Please provide your new phone number", "danger")
            return redirect(f"/profile/{id}")
        


        
@starter.route("/update/profile", methods = ["POST", "GET"], strict_slashes = False)
def updateProfile():
    id= session.get("user")
    info = User.query.get_or_404(id)
    if id == None:
        return redirect(url_for("userLogin"))
    else:
        if request.method == "GET":
            return render_template("user/update-profile.html", info = info)
        else:
            file = request.files['pix']
            filename = file.filename 
            filetype = file.mimetype 
            allowed = [".png", ".jpg", ".jpeg", ".webp", ".aviv"]
            if filename != "":
                name, ext = os.path.splitext(filename) 
                if ext.lower() in allowed: 
                    newname = generate_name()+ext
                    file.save("schedula_app/static/assets/uploads/"+newname) 
                    userImg = f"UPDATE user SET user_img = '{newname}' WHERE (user_id = {id})"
                    result = db.session.execute(text(userImg))
                    db.session.commit()
                    flash(f"Your display picture has been updated", "success")
                    return redirect(f"/profile/{id}")
                else:
                    return "Images only!"
            else:
                flash("Please choose a File")
                return redirect(url_for("updateProfile"))


        
    
