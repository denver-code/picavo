from flask import session, redirect, url_for
from flask_socketio import emit, join_room, leave_room, rooms
from .. import socketio
from functools import wraps
import datetime
from .db import *


def login_required(func):
    def secure_function():
        if "user_id" not in session:
            return redirect(url_for(".signin"))
        else:
            usr_obj = find("users", idc=session["user_id"])
            if usr_obj:
                if usr_obj["Coinfirmed"] == True:
                    if int(datetime.datetime.now().timestamp()) < session["expire"]:
                        return func()
                    else:
                        return redirect(url_for(".signin"))
                else:
                    return "Please confirm your account, activation link has been sended to your email"
            else:
                return redirect(url_for(".signin"))
    return secure_function

def login_not_required(func):
    def secure_function():
        if "user_id" in session:
            return redirect(url_for(".index"))
        else:
            return func()
    return secure_function

@socketio.on("joined", namespace="/achat")
def joined(message):
    room = session.get("room")
    join_room(room)
    emit("status", {"msg": " joined.", "user": session.get("name")}, room=room)


@socketio.on("text", namespace="/achat")
def text(message):
    room = session.get("room")
    # print(rooms())
    if message["msg"] != "":
        emit("message", {"msg": message["msg"], "user": session.get("name")}, room=room)


@socketio.on("left", namespace="/achat")
def left(message):
    room = session.get("room")
    leave_room(room)
    emit("status", {"msg": " left.", "user": session.get("name")}, room=room)
