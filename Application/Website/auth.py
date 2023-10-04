# Laras code for authorizing users and information

from flask import Blueprint, Markup, jsonify, render_template, request, flash, redirect, url_for, request, session, current_app
from .models import User
from . import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, jsonify
from werkzeug.utils import secure_filename
import flask
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

auth = Blueprint('auth', __name__)

# Authorising user login by checking their username and password with the database

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.welcome'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


# Logging out the user

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Signing up user through post form and sending the information to database

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.welcome'))

    return render_template("signup.html", user=current_user)

# Open scan when button is clicked
@auth.route('/scan')
def scan():
    return render_template('scan.html', user=current_user)

# Take image file if submit is clicked, open scan2
@auth.route('/scan', methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Extracting uploaded file and passing it to scan2
        uploaded_img = request.files['uploaded-file']
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))

        session['uploaded_img_file_path'] = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)

    img_file_path = session.get('uploaded_img_file_path', None)

    return render_template('scan2.html', user_image=img_file_path, user=current_user)
