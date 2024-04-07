import requests
from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db, bcrypt, login_manager
from app.models import Great, User
from app.forms import RegisterationForm, LoginForm, SearchForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET'])
def login():
    return 'Login page'

# @app.route('/classes', methods=['GET'])
# def get_classes():
#     classes = Classes.query.all()
#     return jsonify({class.name: class

@app.route('/grades', methods=['GET'])
def get_grades():
    students = Student.query.all()
    print(students)
    return jsonify({student.name: student.grade for student in students})



@app.route('/grade/<string:name>', methods=['GET'])
def get_grade(name):
    if name in students:
        return jsonify({name: students[name]})
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/grade', methods=['POST'])
def add_or_update_grade():
    data = request.json
    if 'name' in data and 'grade' in data:
        student = Student.query.filter_by(name=data['name']).first()
        if student is None:
            student = Student(name=data['name'], grade=data['grade'])
            db.session.add(student)
        else:
            student.grade = data['grade']
        db.session.commit()
        return jsonify({"message": "Grade added successfully"})
    else:
        return jsonify({"error": "Invalid data"}), 400


@app.route('/grade/<string:name>', methods=['PUT'])
def update_grade(name):
    data = request.json
    # Find the student by name
    student = Student.query.filter_by(name=name).first()

    # If the student exists, update their grade
    if student:
        student.grade = data['grade']
        db.session.commit()  # Commit changes to the database
        return jsonify({"message": "Grade updated successfully"})
    else:
        # If the student was not found, return an error
        return jsonify({"error": "Student not found"}), 404


@app.route('/grade/<string:name>', methods=['DELETE'])
def delete_grade(name):
    student = Student.query.filter_by(name=name).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Grade deleted successfully"})
    else:
        return jsonify({"error": "Student not found"}), 404

