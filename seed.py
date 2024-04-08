from app import db
from app.models import User, Class, Enrollment
import random

def add_users_and_classes():
    # Create teachers
    alice = User(username='alice', first_name='Alice', last_name='Brown', email='alice@example.com', password='password123', status='teacher')
    bob = User(username='bob', first_name='Bob', last_name='White', email='bob@example.com', password='password456', status='teacher')
    charlie = User(username='charlie', first_name='Charlie', last_name='Green', email='charlie@example.com', password='password789', status='teacher')
    
   
  # Create students
    students = [
        User(username='ricky', first_name='Ricky', last_name='Blue', email='random@gmail.com', password='password123', status='student'),
        User(username='martin', first_name='Martin', last_name='Red', email='something@gmail.com', password='password123', status='student'),
        User(username='john', first_name='John', last_name='Yellow', email='howdy@gmail.com', password='password123', status='student'),
        User(username='joseph', first_name='Joseph', last_name='Black', email='schish@gmail.com', password='password123', status='student'),
        User(username='jacob', first_name='Jacob', last_name='Purple', email='schishdsfsdf@gmail.com', password='password123', status='student'),
        User(username='jackson', first_name='Jackson', last_name='Orange', email='schishwer@gmail.com', password='password123', status='student')
    ]

    db.session.add(alice)
    db.session.add(bob)
    db.session.add(charlie)
    db.session.add_all(students)
    db.session.commit()  # Commit users to ensure they have ids assigned

    
    # Create classes with teacher_ids set
    classes = [
        Class(name='Mathematics 101', time='08:00 - 09:30', capacity=25, teacher=alice),
        Class(name='English Literature 201', time='10:00 - 11:30', capacity=20, teacher=bob),
        Class(name='Physics 301', time='12:00 - 01:30', capacity=30, teacher=bob),
        Class(name='Chemistry 101', time='02:00 - 03:30', capacity=25, teacher=alice),
        Class(name='Biology 102', time='08:00 - 09:30', capacity=20, teacher=alice),
        Class(name='World History 203', time='10:00 - 11:30', capacity=30, teacher=bob),
        Class(name='Art and Design 101', time='12:00 - 01:30', capacity=15, teacher=bob),
        Class(name='Computer Science 101', time='02:00 - 03:30', capacity=20, teacher=charlie),
        Class(name='Business Management 202', time='08:00 - 09:30', capacity=25, teacher=charlie),
        Class(name='Philosophy 303', time='10:00 - 11:30', capacity=30, teacher=charlie)
    ]
 
    db.session.add_all(classes)
    db.session.commit()
    
     # Randomly enroll each student in a subset of classes
    for student in students:
        enrolled_classes = random.sample(classes, k=random.randint(1, len(classes)))  # Random number of classes, at least 1
        for class_ in enrolled_classes:
            enrollment = Enrollment(student=student, class_=class_, grade=random.randint(50, 100))
            db.session.add(enrollment)

    db.session.commit()

if __name__ == '__main__':
    db.drop_all()  # Drop all tables
    db.create_all()  # Create tables based on models
    add_users_and_classes()
