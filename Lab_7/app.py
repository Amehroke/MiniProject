from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes


# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"name": self.name, "grade": self.grade}


# Sample data for demonstration
students = {
    "Alice": 85,
    "Bob": 90,
    "Charlie": 75
}

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/grades', methods=['GET'])
def get_grades():
    students = Student.query.all()
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

if __name__ == '__main__':
    with app.app_context():
        # Create the database and tables
        db.create_all()
    app.run(debug=True)