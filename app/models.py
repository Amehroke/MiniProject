from app import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader # this is a decorator, it will allow us to access the function as an attribute
def load_user(user_id): # this function will load the user
    return User.query.get(int(user_id)) # this line will return the user

class User(db.Model, UserMixin): # UserMixin will give us the default implementations of the functions that we need to have in the User class for flask_login to work
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    @property # this is a decorator, it will allow us to access the function as an attribute
    def password(self): # this function will return the password
        return self.password
    
    @password.setter # this is a decorator, it will allow us to set the password
    def password(self, plain_text_password): # this function will set the password
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') # this line will hash the password and decode it to utf-8 so that it can be stored in the database (as a string)
    
    def check_password_correction(self, attempted_password): # this function will check if the password is correct
        return bcrypt.check_password_hash(self.password_hash, attempted_password) # this line will check if the password is correct, it will return True if it is correct and False if it is not correct

class Great(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    origin = db.Column(db.String(80), unique=False, nullable=True)
    birth = db.Column(db.String(80), unique=False, nullable=True)
    death = db.Column(db.String(80), unique=False, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=True)
    url = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<Great %r>' % self.name