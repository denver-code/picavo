from flask import session, redirect, url_for, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import main
from .forms import LoginForm
from .db import *
from .validate import *
from .events import login_required, login_not_required
from .generate import generate_id, generate_code, generate_jwt
from .smtp import *
import datetime
import jwt 
from config import FLASK_SECRET

@main.route('/', methods=['GET', 'POST'], endpoint='index')
@login_required
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
    return render_template('index.jade', form=form)

@login_required
@main.route('/achat')
def achat():
    name = session.get("name", "")
    room = session.get("room", "")
    if name == "" or room == "":
        return redirect(url_for(".index"))
    return render_template("chat.html", name=name, room=room)


@main.route("/signin", methods=["GET", "POST"], endpoint="signin")
@login_not_required
def signin():
    if request.method == "GET":
        return render_template("signin.jade")
    if request.form["email"] and request.form["password"]:
        if is_used("users", mail = request.form["email"]):
           user_obj = find("users", mail=request.form["email"])
           if check_password_hash(user_obj["Password"], request.form["password"]):
               session["username"] = user_obj["Username"]
               session["user_id"] = user_obj["UserID"]
               session["expire"] = int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp())
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


@main.route("/signup", methods=["GET", "POST"], endpoint="signup")
@login_not_required
def signup():
    if request.method == "GET":
        return render_template("signup.jade")
    usr_obj = {
        "username":request.form["username"],
        "email":request.form["email"],
        "password": request.form["password"],
        "repass": request.form["repass"],
    }
    if check_auth_data(usr_obj) == True:
        if not is_used("users", mail=request.form["email"]):
            a_key = generate_jwt()
            today = datetime.date.today()
            User = {
                'UserID': int(generate_id()),
                'Username': request.form["username"],
                'Email': request.form["email"],
                'Password': generate_password_hash(request.form["password"]),
                "Coinfirmed": False,
                "Key":a_key,

                'Groups': [],
                'Channels': [],
                'Friends': [],
                'GlobalRoles': ["User"],
                'Country': [],
                'Language': [],
                'Interest': [],

                'RefLink': "",
                'isBanned': 0,
                'SignUPDate': today.strftime("%m/%d/%y")
            }
            insert_db("users",User)
            con_url = request.url[:-6] + f"activate/{a_key}"
            send_confirm(request.form["email"], con_url)
            return redirect(url_for(".signin"))
        else:
            flash("user already exist")
            return redirect(url_for(".signup"))
    else:
        flash(check_auth_data(usr_obj))
        return render_template("signup.jade"), 400
    
@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    tdl = ["username", "expire", "user_id"]
    for i in tdl:
        session.pop(i)
    return redirect(url_for(".signin"))


@main.route("/protect", endpoint="protect")
@login_required
def protect():
    return render_template("test.html")

@main.route('/activate/<string:akey>', methods=['GET'])
def get_task(akey):
    if is_used("users", idc=session["user_id"]):
        activ_obj = find("users", cusname="Key", cusdata=str(akey))
        if activ_obj["Key"] == akey:
            jwt_data = jwt.decode(akey, FLASK_SECRET, algorithms=['HS256'])
            if int(datetime.datetime.now().timestamp()) < jwt_data["expire"]:
                activ_obj["Coinfirmed"] = True
                update_db("users", {"UserID":session["user_id"]}, activ_obj)
                return redirect(url_for(".index"))
            else:
                flash("Activate token has been expired")
                delete_db("users", {"UserID":session["user_id"]})
                return render_template("signup.jade"), 400
        else:
            return "Invalid key"