from flask import render_template, request, redirect, url_for, flash
from app import app, db
import models
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
# from forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # error = ""

    # This handles when logged in user visiting the login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "GET":
        return render_template('login.html')

    email = request.form['inputEmail']
    pas = request.form['inputPassword']

    user = models.User.query.filter_by(email=email).first()
    if user is None or not user.check_password(pas):
        print(user is None)
        flash('Invalid username or password')
        return redirect(url_for('login'))
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)


@app.route('/signup', methods=['POST', "GET"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')

    name = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    user = models.User(username=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
