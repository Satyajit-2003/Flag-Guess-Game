from app import app
from flask import flash, render_template, redirect, url_for, request, make_response
from app.utils.auth import token_required, login_, register_

# Check if user is not logged in and redirect to login page if logged in
# else redirect to index page
@app.route('/')
@token_required
def index(user):
    print(user.user_id)
    return render_template('index.html')

# login page with login form 
# if user is logged in redirect to index page
# set cookie with token
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

# register page with register form
# authenticate user and redirect to index page
# set cookie with token
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        resp = register_(request)
        if resp == 1:
            token = login_(request)
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', token)
            flash('Registration successful!', 'success')
            flash('You are now logged in!', 'success')
            return resp
        elif resp == -1:
            flash('Invalid credentials!', 'danger')
        else:
            flash('Registration failed!', 'danger')
    return render_template('register.html')

# logout user and redirect to login page
# delete cookie
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('token', '', expires=0)
    return resp
