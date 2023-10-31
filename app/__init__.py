from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app)

app.config.from_object(Config)

from app import routes
