from app import db, bcrypt, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader # this is a decorator, it will allow us to access the function as an attribute
def load_user(user_id): # this function will load the user
    return User.query.get(int(user_id)) # this line will return the user

class User(db.Model, UserMixin): # UserMixin will give us the default implementations of the functions that we need to have in the User class for flask_login to work
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='student')

    @property # this is a decorator, it will allow us to access the function as an attribute
    def password(self): # this function will return the password
        return self.password
    
    @password.setter # this is a decorator, it will allow us to set the password
    def password(self, plain_text_password): # this function will set the password
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') # this line will hash the password and decode it to utf-8 so that it can be stored in the database (as a string)
    
    def check_password_correction(self, attempted_password): # this function will check if the password is correct
        return bcrypt.check_password_hash(self.password_hash, attempted_password) # this line will check if the password is correct, it will return True if it is correct and False if it is not correct

class Class(db.Model): # this line will create the Class model
    id = db.Column(db.Integer, primary_key=True) # this line will create the id column
    name = db.Column(db.String(100), nullable=False) # this line will create the name column

    def __repr__(self): # this function will return the name of the class
        return f"Class('{self.name}')"

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Class, db.session))
    
# how to delete all data from a table
# >>> python
# >>> from MSapp import models
# >>> from MSapp.models import User, Great
# >>> from MSapp import db

### for all records ###
# >>> db.session.query(User).delete()
# 1
# >>> db.session.

### for specific records ###
# >>> db.session.query(User).filter(User.id == 1).delete()
# >>> db.session.commit()