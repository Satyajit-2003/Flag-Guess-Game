import os
from flask import Flask
from flask_socketio import SocketIO
from config import Config

app = Flask(__name__)
socketio = SocketIO(app)

app.config.from_object(Config)

if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]):
    os.makedirs(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])

from app import routes
from app import sockets
