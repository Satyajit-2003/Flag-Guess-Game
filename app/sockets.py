from app import socketio
from app.utils.game import Game
from app.utils.auth import get_user
from flask import request
from time import sleep

# dictionary of games currently active
games = {} # {user_id: Game}

# socketio events\
# connect: when a client connects to the server
# Updates the client with the user's highscore and current score
# Updates the client with the current country's flag
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
    print(games[user.user_id].get_country().name, 'connected')

# answer: when a client answers a question
# Checks if the answer is correct and sends the result to the client
# Updates the client with the user's highscore and current score
# wait 5 seconds and update the client with the new country's flag
@socketio.on('answer')
def answer(data):
    user = get_user(request.cookies['token'])
    print('Client answered', user.user_id)
    res = games[user.user_id].check_answer(data['answer'])
    socketio.emit('result', {'result': res[0], 'answer': res[1]})
    socketio.emit('update', {'user': user.user_id ,'highscore': str(user.high_score),
                              'score': str(games[user.user_id].get_score())})
    sleep(5)
    games[user.user_id].refresh_country()
    socketio.emit('update_country', {'flag': games[user.user_id].get_country().flag})

# end: when a client disconnects from the server
# Deletes the game object from the games dictionary
@socketio.on('end')
def end():
    user = get_user(request.cookies['token'])
    print('Client disconnected', user.user_id)
    games[user.user_id].__del__()
    del games[user.user_id]