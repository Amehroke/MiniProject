import requests
from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db, bcrypt, login_manager
from app.models import User, Class
from app.forms import RegisterationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('home.html')

# pass the search form to the template/base.html

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data): # this line will check if we have a user with the username that the user entered and if the password that the user entered is correct
            if form.remember.data:
                login_user(attempted_user, remember=True)
                flash(f'Success! You are logged in as: {attempted_user.username}, and will be remembered for 1 hour', category='success')
                return redirect(url_for('home'))
            
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Username or Password. Please try again.', category='danger')

    return render_template('login.html', form=form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterationForm()
    if form.validate_on_submit(): # if the form is valid/user has submitted the form
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('You have successfully created an account!', category='success')
        return redirect(url_for('home'))
    if form.errors != {}: # if there are no errors from the validations
        for err_msg in form.errors.values(): # loop through the dictionary of errors
            flash(f'Registeration Error: {err_msg}', category='danger') # print each error message to the screen
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('home'))