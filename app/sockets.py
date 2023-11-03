from app import socketio
from app.utils.game import Game
from app.utils.auth import get_user, token_required
from flask import request
from time import sleep

games = {}

@socketio.on('connect')
def connect():
    user = get_user(request.cookies['token'])
    print('Client connected', user.user_id)
    if user.user_id not in games:
        games[user.user_id] = Game(user.user_id)
        games[user.user_id].refresh_country()
    socketio.emit('update', {'user': user.user_id ,'highscore': str(user.high_score),
                              'score': str(games[user.user_id].get_score())})
    socketio.emit('update_country', {'flag': games[user.user_id].get_country().flag})
    print(games[user.user_id].get_country().name)

@socketio.on('answer')
def answer(data):
    user = get_user(request.cookies['token'])
    print('Client answered', user.user_id)
    print(data)
    res = games[user.user_id].check_answer(data['answer'])
    socketio.emit('result', {'result': res[0], 'answer': res[1]})
    socketio.emit('update', {'user': user.user_id ,'highscore': str(user.high_score),
                              'score': str(games[user.user_id].get_score())})
    sleep(5)
    games[user.user_id].refresh_country()
    socketio.emit('update_country', {'flag': games[user.user_id].get_country().flag})

@socketio.on('end')
def end():
    user = get_user(request.cookies['token'])
    print('Client disconnected', user.user_id)
    games[user.user_id].__del__()
    del games[user.user_id]