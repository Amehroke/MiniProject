from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from datetime import timedelta
import os
from dotenv import load_dotenv


load_dotenv()

print(os.getenv('DATABASE_URL')) # this line will print the database url from the .env file, for testing

app = Flask(__name__) # this line will create the flask object
app.app_context().push() # this line will create the application context, which is needed for the db object because it is not created with the app object in this file
app.config['SECRET_KEY'] = 'b1b4b3b1b4b3b1b4b3b1b4b3b1b4b3' # this line will set the secret key for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # this line will set the database uri to the students.db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this line will set the track modifications to False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
admin = Admin(app, name='Admin', template_mode='bootstrap3')
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # this line will set the login view to the login function
login_manager.login_message_category = 'info' # this line will set the login message category to info
login_manager.remember_cookie_duration = timedelta(seconds=3600) # this line will set the remember me cookie to expire after 1 hour
login_manager.login_message = (u'Please log in to access this page.') # this line will set the login message to the message in the brackets
login_manager.init_app(app)

# we import routes after the app object is created because the routes module needs to import the app object
from app import routes