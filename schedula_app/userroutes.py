import os, random, string
from flask import render_template, redirect, request, jsonify, session, flash, url_for
from sqlalchemy import *
from sqlalchemy.sql import text
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from schedula_app import starter, db
from schedula_app.model import User, Contact, Task
from forms import UserRegForm, LoginForm, ContactForm, PhoneForm



from schedula_app import starter
csrf = CSRFProtect(starter)

mysql = MySQL(starter)
starter.config["MYSQL_HOST"] = "localhost"
starter.config["MYSQL_USER"] = "root"
starter.config["MYSQL_PASSWORD"] = ""
starter.config["MYSQL_DB"] = "scheduladb"
starter.config["MYSQL_CURSORCLASS"] = "DictCursor"


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
        req = request.form
        name = req.get("contact_name")
        mail = req.get("mail")
        phone = req.get("phone")
        message = req.get("message")
        if name != "" and mail != "" and phone != "" and message != "":
            if validatePhone(phone):
                flash("You must fill the form correctly to register", "danger")
                return redirect("/#support")
            newContact = Contact(contact_name = name, contact_mail = mail, contact_phone = phone, contact_message = message)
            db.session.add(newContact)
            db.session.commit()
            flash(f"Thank you for reaching out to us, {name} We will get in touch with you shortly. ", "success")
            return redirect(request.referrer)
        else:
            flash(f"Please fill the form correctly ", "danger")
            return redirect(request.referrer)
    else:
        return render_template("user/index.html", form = form)


@starter.route("/register", methods = ["POST", "GET"], strict_slashes = False)
def userReg():
    form = UserRegForm()
    if request.method == "POST":
        req = request.form
        fname = req.get("fname")
        lname = req.get("lname")
        phone = req.get("phone")
        password = req.get("password")
        c_password = req.get("c_password")
        hashedpwd = generate_password_hash(password)        
        if fname !="" and lname != "" and phone != "" and password !="":
            if (validatePhone(phone) and validatePasswordMatch(password, c_password)):
                return redirect(request.referrer)
            new_user = User(user_fname = fname, user_lname = lname, user_phone = phone, user_password= hashedpwd)
            db.session.add(new_user)
            db.session.commit()
            userid=new_user.user_id
            session['user'] = userid
            flash(f"Account created for you, {fname}! Please proceed to LOGIN ", "success")
            return redirect(url_for("userLogin"))
        else:
            flash("You must fill the form correctly to register", "danger")
            return redirect(request.url)
    else:
        return render_template("user/register.html", form = form, title="Register - Schedula")
    

@starter.route("/login", methods = ["POST", "GET"], strict_slashes = False)
def userLogin():
    form = LoginForm()
    if request.method == "POST":
        req = request.form
        phone = req.get("phone")
        password = req.get("password")
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
                return redirect(request.referrer)
        else:
            flash("You will need to create an account first", "danger")
            return redirect(url_for("userReg"))
    else:
        return render_template("user/login.html", form = form, title = "Login - Schedula")
    
@starter.route("/logout", strict_slashes = False)
def userLogout():
    if session.get("user") != None:
        session.pop("user", None)
    return redirect(url_for("home"))

@starter.route("/start", strict_slashes = False)
def start():
    id = session.get("user")
    if id:
        return redirect(url_for("app", id = id))
    else:
        return redirect(url_for("userLogin"))

@starter.route("/app/<int:id>", strict_slashes = False)
def app(id):
    user = session.get("user")
    info = User.query.get_or_404(id)
    if user:
        t = Task.query.filter_by(task_user = info.user_id, task_priority = 1).all() or []
        tp = Task.query.filter_by(task_user = info.user_id, task_priority = 1).limit(3).all()
        m = Task.query.filter_by(task_user = info.user_id, task_priority = 2).all() or []
        md = Task.query.filter_by(task_user = info.user_id, task_priority = 2).limit(3).all()
        l = Task.query.filter_by(task_user = info.user_id, task_priority = 3).all() or []
        lt = Task.query.filter_by(task_user = info.user_id, task_priority = 3).limit(3).all()
        top = len(t) 
        mid = len(m) 
        least = len(l)
        total = len(t) + len(m) + len(l)
        return render_template("user/app.html", info = info, top = top, mid = mid, least = least, total= total, t=tp, m=md, l=lt)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/addnew/<int:id>", methods = ["POST", "GET"], strict_slashes = False)
def addNew(id):
    user = session.get("user")
    info = User.query.get_or_404(id)
    if user:
        if request.method == "POST":
            req = request.form
            task = req.get("taskName")
            order = req.get("priority")
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
                    return redirect(request.referrer)
                else:
                    return "Images only!"
            else:
                flash("Please fill all fields")
                return redirect(request.referrer)

        else:
            return render_template("user/addnew.html", info = info)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/update-progress/<int:id>", strict_slashes = False)
def toDoing(id):
    user = session.get("user")
    if user:
        task_to_update = Task.query.get_or_404(id)
        task_to_update.task_status = 2
        db.session.commit()
        return redirect(request.referrer)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/update-complete/<int:id>", strict_slashes = False)
def toDone(id):
    user = session.get("user")
    if user:
        task_to_update = Task.query.get_or_404(id)
        task_to_update.task_status = 3
        db.session.commit()
        return redirect(request.referrer)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/must-do-list/<int:id>", strict_slashes = False)
def must(id):
    user = session.get("user")
    if user:
        info = User.query.get_or_404(id)
        todo = Task.query.filter_by(task_user = info.user_id, task_priority = 1).all()
        return render_template("user/must.html", info = info, todo = todo)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/should-do-list/<int:id>", strict_slashes = False)
def should(id):
    user = session.get("user")
    if user:
        info = User.query.get_or_404(id)
        todo = db.session.query(Task).filter_by(task_user = info.user_id, task_priority = 2).all() 
        return render_template("user/should.html", info = info, todo = todo)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/could-do-list/<int:id>", strict_slashes = False)
def could(id):
    user = session.get("user")
    if user:
        info = User.query.get_or_404(id)
        todo = db.session.query(Task).filter_by(task_user = info.user_id, task_priority = 3).all() 
        return render_template("user/could.html", info = info, todo = todo)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/delete/<int:id>", strict_slashes = False)
def deleteTodo(id):
    user = session.get("user")
    if user:
        task_to_delete = Task.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        # current_url = request.url
        return redirect(request.referrer)
    return redirect(url_for("userLogin"))

    

@starter.route("/profile/<int:id>", strict_slashes = False)
def userProfile(id):
    user = session.get("user")
    if user:
        info = User.query.get_or_404(id)
        return render_template("user/profile.html", info = info)
    else:
        return redirect(url_for("userLogin"))


@starter.route("/update/phone-number", methods = ["POST", "GET"], strict_slashes = False)
def updatePhone():
    id = session.get("user")
    info = db.session.query(User).get(id)
    form = PhoneForm()
    if request.method == "POST":
        req = request.form
        new_phone = req.get("phone")
        if new_phone != "":
            if validatePhone(new_phone):
                info.user_phone = new_phone
                db.session.commit()
                flash(f"Your phone number has been updated", "success")
                return redirect(request.referrer)
            else:
                return redirect(request.referrer)    
    else:
         return render_template("user/update-phone.html", form = form)


@starter.route("/update/task", methods = ["POST", "GET"], strict_slashes = False)
def updateTask():
    id = session.get("user")
    info = db.session.query(User).get(id)
    todo = db.session.query(Task).filter(Task.task_user==id).first()
    if request.method == "POST":
        req = request.form
        task = req.get("task")
        order = req.get("taskOrder")
        file = request.files['taskDp']
        filename = file.filename 
        filetype = file.mimetype 
        allowed = [".png", ".jpg", ".jpeg", ".webp", ".aviv"]
        if task != "" and order !="" and filename != "":
            name, ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newTaskDp = generate_name()+ext
                file.save("schedula_app/static/assets/uploads/"+newTaskDp)
                todo.task_item = task
                todo.task_priority = order
                todo.task_img = newTaskDp
                todo.task_user = id
                db.session.commit() 
                flash(f"Your task has been updated", "success")
                return redirect(request.referrer)
            else:
                flash("Please fill the fields", "danger")
                return redirect(request.referrer)    
    else:
         return render_template("user/update-task.html", info = info)
        


        
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
                return redirect(request.referrer)


@starter.route("/livesearch", methods = ["POST", "GET"])
def livesearch():
    searchbox = request.form.get("text")
    cursor = mysql.connection.cursor()
    query = "SELECT task_item FROM task WHERE task_item LIKE '{}%' ORDER BY task_item".format(searchbox)
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)      


@starter.route("/searchApp", methods = ['POST', 'GET'], strict_slashes = False)
def searchbox():
    user = session.get("user")
    allTasks = db.session.query(Task).filter(Task.task_user == user).all()
    return redirect(url_for('app', id = user), allTasks=allTasks) 


        
    
