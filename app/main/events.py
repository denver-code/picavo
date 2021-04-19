from flask import session, redirect, url_for
from flask_socketio import emit, join_room, leave_room, rooms
from .. import socketio
from functools import wraps

# def login_required(f):
#     if "username" in session:
#         return f()
#     else:
#         return redirect(url_for('.signin'))

def login_required(func):
    def secure_function():
        if "username" not in session:
            return redirect(url_for(".signin"))
        return func()

    return secure_function

@socketio.on('joined', namespace='/achat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':' joined.', 'user':session.get('name')}, room=room)


@socketio.on('text', namespace='/achat')
def text(message):
    room = session.get('room')
    # print(rooms())
    if message['msg'] != "":
        emit('message', {'msg':message['msg'], 'user':session.get('name')}, room=room)


@socketio.on('left', namespace='/achat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': ' left.', "user":session.get('name')}, room=room)