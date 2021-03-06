from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user  # this is why user db used UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # gets all the users with this email, .first() since email is unique
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)  # creates a session for the user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # validation
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be  greater than 4 characters', category='error')  # to flash messages to the user
        elif len(first_name) < 2:
            flash('Email must be  greater than 3 characters', category='error')  # to flash messages to the user
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')  # to flash messages to the user
        elif len(password1) < 7:
            flash('Password is too short', category='error')  # to flash messages to the user
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))  # ignore the error
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            login_user(user, remember=True)  # creates a session for the user
            return redirect(url_for('views.home'))

    # data = request.form  # to get everything from the entire form
    # print(data)
    return render_template("sign_up.html", user=current_user)
