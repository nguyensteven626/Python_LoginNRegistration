
from flask import render_template, redirect, session, request, flash 
from login_registration_app import app, bcrypt 
from login_registration_app.models.user import User 
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#-----displayroutes----#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('success.html', user=User.retrieve_one(data))


#-----actionroutes-----#
@app.route('/register', methods = ['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')

    user_data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.create(user_data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Try again")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Nope. You're a hacker")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 