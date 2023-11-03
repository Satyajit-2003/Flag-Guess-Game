from functools import wraps
from flask import jsonify, request, flash, redirect, url_for
import jwt
from app import app
from app.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


def token_required(f):

  @wraps(f)
  def decorated(*args, **kwargs):
    token = None

    if 'token' in request.cookies:
      token = request.cookies['token']

    if not token:
      flash('Token is missing!', 'danger')
      return redirect(url_for('login'))

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
      current_user = User.query.filter_by(user_id=data['user_id']).first()
    except:
      flash('Session Expired!', 'danger')
      return redirect(url_for('login'))

    return f(current_user, *args, **kwargs)

  return decorated


def login_(request):
  user = request.form.get('user-id')
  password = request.form.get('password')

  if not user or not password:
    return None

  user = User.query.filter_by(user_id=user).first()

  if not user:
    return None

  if check_password_hash(user.password, password):
    token = jwt.encode(
        {
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256")
    print(token)
    return token

  return None


def register_(request):
  user_id = request.form.get('user-id')
  password = request.form.get('password')
  confirm_password = request.form.get('confirm-password')
  if not user_id or not password or password != confirm_password:
    return -1
  try:
    user = User(user_id=user_id,
                password=generate_password_hash(password,
                                                method='pbkdf2:sha256'))
    db.session.add(user)
    db.session.commit()
    return 1
  except:
    return 0


def get_user(token):
  if not token:
    return None
  try:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    current_user = User.query.filter_by(user_id=data['user_id']).first()
    return current_user
  except:
    return None
