import os
from flask import Flask
from flask_socketio import SocketIO
from config import Config

app = Flask(__name__) # Initialize Flask app
socketio = SocketIO(app, ssl_context='adhoc') # Initialize Flask-SocketIO app (with SSL) 
                        # 'adhoc' is for self-signed certificates

app.config.from_object(Config) # Load config from config.py

# Create database file if it doesn't exist
with open(app.config['SQLALCHEMY_DATABASE_URI'].split('sqlite:///')[1], 'a') as f:
    f.close()

from app import routes
from app import sockets
