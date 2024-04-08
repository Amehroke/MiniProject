import requests
from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db, bcrypt, login_manager
from app.models import User, Class
from app.forms import RegisterationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import current_app as app, jsonify
from .models import User, Class
import pandas as pd
from . import db



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses', methods=['GET'])
def get_courses():
    # Query all courses and join with the User table to get teacher info
    courses = Class.query.join(User).filter(Class.teacher_id == current_user.id).all()

    # Format the output to include course name, time, capacity, and teacher's name
    course_info = [{
        'name': course.name,
        'time': course.time,
        'capacity': course.capacity,
        'teacher': current_user.first_name + ' ' + current_user.last_name
    } for course in courses]

    return jsonify(course_info)


# pass the search form to the template/base.html

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data): # this line will check if we have a user with the username that the user entered and if the password that the user entered is correct
            if form.remember.data:
                login_user(attempted_user, remember=True)
                flash(f'Success! You are logged in as: {attempted_user.first_name}, and will be remembered for 1 hour', category='success')
                return redirect(url_for('home'))
            
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.first_name}', category='success')
            if attempted_user.status == 'teacher':
                return render_template('teacher.html')
            elif attempted_user.status == 'student':
                return render_template('student.html')
            elif(form.status.data == 'admin'):
                return render_template('admin/index.html')
            else:
                return redirect(url_for('home'))
        else:
            flash('Incorrect Username or Password. Please try again.', category='danger')

    return render_template('login.html', form=form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterationForm()
    if form.validate_on_submit(): # if the form is valid/user has submitted the form
        new_user = User(username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=form.password1.data,
                        status=form.status.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('You have successfully created an account!', category='success')
        if(form.status.data == 'teacher'):
            return render_template('teacher.html')
        elif(form.status.data == 'student'):
            return render_template('student.html')
        elif(form.status.data == 'admin'):
            return render_template('admin/index.html')
        else:
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