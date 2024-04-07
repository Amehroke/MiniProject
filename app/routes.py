import requests
from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('index.html')