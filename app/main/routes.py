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


@main.route("/", methods=["GET", "POST"], endpoint="index")
@login_required
def index():
    # print(session["username"])
    form = LoginForm()
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["room"] = form.room.data
        return redirect(url_for(".achat"))
    elif request.method == "GET":
        form.name.data = session.get("name", "")
        form.room.data = session.get("room", "")
    return render_template("index.jade", form=form)


@login_required
@main.route("/achat")
def achat():
    name = session.get("name", "")
    room = session.get("room", "")
    if name == "" or room == "":
        return redirect(url_for(".index"))
    return render_template("chat.html", name=name, room=room)


@main.route("/auth/signin", methods=["GET", "POST"], endpoint="signin")
@login_not_required
def signin():
    if request.method == "GET":
        return render_template("auth/signin.jade")
    if (
        request.form["login>logSender>email"]
        and request.form["login>logSender>password"]
    ):
        if is_used("users", mail=request.form["login>logSender>email"]):
            user_obj = find("users", mail=request.form["login>logSender>email"])
            if check_password_hash(
                user_obj["Password"], request.form["login>logSender>password"]
            ):
                session["username"] = user_obj["Username"]
                session["user_id"] = user_obj["UserID"]
                session["expire"] = int(
                    (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
                )
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


@main.route("/auth/signup", methods=["GET", "POST"], endpoint="signup")
@login_not_required
def signup():
    if request.method == "GET":
        return render_template("auth/signup.jade")
    usr_obj = {
        "username": request.form["register>regSender>username"],
        "email": request.form["register>regSender>email"],
        "password": request.form["register>regSender>password"],
        "repass": request.form["register>regSender>rePassword"],
    }
    if check_auth_data(usr_obj) == True:
        if not is_used("users", mail=request.form["email"]):
            a_key = generate_jwt()
            today = datetime.date.today()
            User = {
                "UserID": int(generate_id()),
                "Username": request.form["username"],
                "Email": request.form["email"],
                "Password": generate_password_hash(request.form["password"]),
                "Confirmed": False,
                "Key": a_key,
                "Souls": 0,
                "Groups": [],
                "Channels": [],
                "Friends": [],
                "GlobalRoles": ["User"],
                "Country": [],
                "Language": [],
                "Interest": [],
                "RefLink": "",
                "isBanned": 0,
                "SignUPDate": today.strftime("%m/%d/%y"),
            }
            insert_db("users", User)
            con_url = request.url[:-6] + f"activate/{a_key}"
            send_confirm(request.form["email"], con_url)
            return redirect(url_for(".signin"))
        else:
            flash("user already exist")
            return redirect(url_for(".signup"))
    else:
        flash(check_auth_data(usr_obj))
        return render_template("auth/signup.jade"), 400


@main.route("/auth/logout", methods=["GET", "POST"], endpoint="logout")
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


@main.route("/activate/<string:akey>", methods=["GET"])
def get_task(akey):
    if is_used("users", cusname="Key", cusdata=str(akey)):
        activ_obj = find("users", cusname="Key", cusdata=str(akey))
        if activ_obj["Key"] == akey:
            jwt_data = jwt.decode(akey, FLASK_SECRET, algorithms=["HS256"])
            if int(datetime.datetime.now().timestamp()) < jwt_data["expire"]:
                activ_obj["Confirmed"] = True
                update_db("users", {"UserID": activ_obj["UserID"]}, activ_obj)
                return redirect(url_for(".index"))
            else:
                flash("Activate token has been expired")
                delete_db("users", {"UserID": session["user_id"]})
                return render_template("auth/signup.jade"), 400
        else:
            return "Invalid key"


@main.route("/auth/reset_password", methods=["GET", "POST"], endpoint="reset_password")
def reset_password():
    if request.method == "GET":
        return render_template("auth/forgotPassword.jade")
    else:
        if request.form.get("rpass>emailSender>email"):
            if is_used("users", mail=request.form["rpass>emailSender>email"]):
                usr_obj = find("users", mail=request.form["rpass>emailSender>email"])
                if usr_obj["Confirmed"]:
                    vcode = generate_code()
                    usr_obj["Key"] = vcode
                    update_db(
                        "users",
                        {"Email": request.form["rpass>emailSender>email"]},
                        usr_obj,
                    )
                    send_code(request.form["rpass>emailSender>email"], vcode)
                    return "Email has been sent"
                else:
                    return "Your account must be confirmed!", 400
            else:
                return "User not found", 404
        elif request.form.get("rpass>codeSender>code"):
            usr_obj = find(
                "users", cusname="Key", cusdata=request.form["rpass>codeSender>code"]
            )
            if usr_obj:
                session["entered_email"] = usr_obj["Email"]
                session["valid_key"] = True
                return "Code valid, enter a new password"
            else:
                return "Invalid code!", 400
        elif request.form.get("rpass>passSender>password"):
            if request.form.get("rpass>passSender>password") == request.form.get(
                "rpass>passSender>rePassword"
            ):
                if len(request.form.get("rpass>passSender>password")) >= 8:
                    if "valid_key" in session and session["valid_key"] == True:
                        usr_obj = find("users", mail=session["entered_email"])
                        usr_obj["Password"] = generate_password_hash(
                            request.form.get("rpass>passSender>password")
                        )
                        update_db("users", {"Email": session["entered_email"]}, usr_obj)
                        session.pop("entered_email")
                        session.pop("valid_key")
                        return redirect(url_for(".signin"))
                    else:
                        return "You entered the wrong code or did not enter it!", 400
                else:
                    return "Len password must be >= 8", 400
            else:
                return "Password don't match", 400


@main.route("/profile", methods=["GET"], endpoint="profile")
@login_required
def profile():
    if request.method == "GET":
        usr_obj = find("users", idc=session["user_id"])
        return render_template("profile.html", user_obj=usr_obj)


@main.route("/settings", methods=["GET", "POST"], endpoint="settings")
@login_required
def settings():
    if request.method == "GET":
        usr_obj = find("users", idc=session["user_id"])
        return render_template("settings.html", usr_obj=usr_obj)
    if request.form.get("rprofile>user>username"):
        usr_obj = find("users", idc=session["user_id"])
        if check_name(request.form.get("rprofile>user>username")):
            usr_obj["Username"] = request.form.get("rprofile>user>username")
            update_db("users", {"UserID": session["user_id"]}, usr_obj)
            return redirect(url_for(".profile"))
        else:
            flash("Invalid name")
            return redirect(url_for(".settings"))


@main.route("/rmail", methods=["GET", "POST"], endpoint="reset_email")
@login_required
def reset_email():
    if request.method == "GET":
        return render_template("rmail.html")
    else:
        if request.form.get("rmail>emailSender>email"):
            if is_used("users", mail=request.form["rmail>emailSender>email"]):
                usr_obj = find("users", mail=request.form["rmail>emailSender>email"])
                if usr_obj["Confirmed"]:
                    vcode = generate_code()
                    usr_obj["Key"] = vcode
                    update_db(
                        "users",
                        {"Email": request.form["rmail>emailSender>email"]},
                        usr_obj,
                    )
                    send_code(request.form["rmail>emailSender>email"], vcode)
                    flash("Email has been sent")
                    return render_template("rmail.html")
                else:
                    flash("Your account must be confirmed!")
                    return render_template("rmail.html"), 400
            else:
                flash("User not found")
                return render_template("rmail.html"), 400
        elif request.form.get("rmail>codeSender>code"):
            usr_obj = find(
                "users", cusname="Key", cusdata=request.form["rmail>codeSender>code"]
            )  # mail=session["entered_email"]
            if usr_obj:
                session["entered_email"] = usr_obj["Email"]
                session["valid_key"] = True
                flash("Code valid, enter a new password")
                return render_template("rmail.html")
            else:
                flash("Invalid code!")
                return render_template("rmail.html"), 400
        elif request.form.get("rmail>emailSender>newEmail"):
            if check_mail(request.form.get("rmail>emailSender>newEmail")):
                if "valid_key" in session and session["valid_key"] == True:
                    usr_obj = find("users", mail=session["entered_email"])
                    a_key = generate_jwt()
                    usr_obj["Email"] = request.form.get("rmail>emailSender>newEmail")
                    usr_obj["Key"] = a_key
                    usr_obj["Confirmed"] = False
                    update_db("users", {"Email": session["entered_email"]}, usr_obj)
                    con_url = request.url[:-5] + f"activate/{a_key}"
                    send_confirm(usr_obj["Email"], con_url)
                    session.pop("entered_email")
                    session.pop("valid_key")
                    return redirect(url_for(".logout"))
                else:
                    flash("You entered the wrong code or did not enter it!")
                    return render_template("rmail.html"), 400
            else:
                flash("Invalid email")
                return render_template("rmail.html"), 400
