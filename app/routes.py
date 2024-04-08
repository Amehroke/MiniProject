import requests
from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db, bcrypt, login_manager
from app.models import User, Class
from app.forms import RegisterationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import current_app as app, jsonify
from .models import User, Class, Enrollment
import pandas as pd
from . import db






@app.route('/courses')
def show_courses():
    if current_user.status == 'teacher':
        courses = Class.query.join(User).filter(Class.teacher_id == current_user.id).all()
        return render_template('teacher.html', courses=courses)
    elif current_user.status == 'student':
        courses = Class.query.join(Enrollment, Class.id == Enrollment.class_id)\
                             .filter(Enrollment.student_id == current_user.id).all()
        return render_template('student.html', courses=courses)
    elif current_user.status == 'admin':
        return render_template('admin/index.html')

@app.route('/')
def home():
    if current_user.is_authenticated:
        return show_courses()
    else:
        return render_template('home.html')
    
@app.route('/edit-grades', methods=['GET'])
@login_required
def edit_grades():
    course_id = request.args.get('courseId')
    if course_id:
        course = Class.query.get(course_id)
        if course and current_user.id == course.teacher_id:
            enrollments = Enrollment.query.filter_by(class_id=course_id).all()
            return render_template('edit-grades.html', enrollments=enrollments, course=course)
    flash('Unauthorized access or invalid course.')
    return redirect(url_for('show_courses'))

@app.route('/update-grades', methods=['POST'])
@login_required
def update_grades():
    # Assuming `courseId` is the name attribute in your HTML form
    course_id = request.form.get('courseId')
    
    if not course_id:
        flash('No course specified.')
        return redirect(url_for('show_courses'))
    
    course = Class.query.get(course_id)
    
    # Check if the course exists and the current user is the teacher of the course
    if not course or current_user.id != course.teacher_id:
        flash('Unauthorized or course not found.')
        return redirect(url_for('show_courses'))

    # Process grades only if the current user is the teacher of the course
    for key in request.form:
        if key.startswith('grade-'):
            student_id = key.split('-')[1]  # Extract the student ID from the form field name
            try:
                student_id = int(student_id)
                grade = request.form[key]
                enrollment = Enrollment.query.filter_by(class_id=course_id, student_id=student_id).first()
                if enrollment:
                    enrollment.grade = grade
                    db.session.commit()
            except ValueError:
                # Handle the case where the student ID is not an integer
                continue

    flash('Grades updated successfully.')
    return redirect(url_for('edit_grades', courseId=course_id))


# @app.route('/grade/<string:name>', methods=['PUT'])
# def update_grade(name):
#     data = request.json
#     # Find the student by name
#     student = Student.query.filter_by(name=name).first()

#     # If the student exists, update their grade
#     if student:
#         student.grade = data['grade']
#         db.session.commit()  # Commit changes to the database
#         return jsonify({"message": "Grade updated successfully"})
#     else:
#         # If the student was not found, return an error
#         return jsonify({"error": "Student not found"}), 404

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
            return show_courses()
          
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