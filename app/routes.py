from app import app, socketio
from flask import flash, render_template, redirect, url_for, request, make_response, jsonify
from flask_socketio import emit
from app.utils.auth import token_required, login_, register_


@app.route('/')
@token_required
def index(user):
    print(user.user_id)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = login_(request)
        if token:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', token)
            return resp
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        resp = register_(request)
        if resp == 1:
            login_(request)
            flash('Registration successful!', 'success')
            flash('You are now logged in!', 'success')
            return redirect(url_for('index'))
        elif resp == -1:
            flash('Invalid credentials!', 'danger')
        else:
            flash('Registration failed!', 'danger')
    return render_template('register.html')
    