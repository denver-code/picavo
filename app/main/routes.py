from flask import session, redirect, url_for, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import main
from .forms import LoginForm
from .db import *
from .validate import *
from .events import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    # print(session["username"])
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.achat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)

@main.route('/achat')
def achat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)

@main.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("login.html")
    if request.form["email"] and request.form["password"]:
        if is_used("users", mail = request.form["email"]):
           user_obj = find("users", mail=request.form["email"])
           if check_password_hash(user_obj["password"], request.form["password"]):
               session["username"] = user_obj["username"]
               return redirect(url_for(".index"))
           else:
               flash("Invalid password")
               return redirect(url_for(".signin"))
        else:
            flash("User not found")
            return redirect(url_for(".signin"))    
    else:
        flash("Data is invalid")
        return redirect(url_for(".signin"))          
    

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("reg.html")
    if check_mail(request.form["email"]) and request.form["password"] == request.form["repass"] and check_name(request.form["username"]):
        if not is_used("users", mail=request.form["email"]):
            insert_db("users",{
                "username":request.form["username"],
                "email":request.form["email"],
                "password":generate_password_hash(request.form["password"])})
            return redirect(url_for(".signin"))
        else:
            flash("user already exist")
            return redirect(url_for(".signup"))
    else:
        flash("Some data is invalid")
        return redirect(url_for(".signup"))
    
@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop("username")
    return redirect(url_for(".signin"))

@main.route("/protect", endpoint='protect')
@login_required
def protect():
    return render_template("test.html")