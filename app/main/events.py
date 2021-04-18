from flask import session
from flask_socketio import emit, join_room, leave_room, rooms
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':' joined.', 'user':session.get('name')}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    # print(rooms())
    if message['msg'] != "":
        emit('message', {'msg':message['msg'], 'user':session.get('name')}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': ' left.', "user":session.get('name')}, room=room)

