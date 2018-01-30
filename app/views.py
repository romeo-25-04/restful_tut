from flask import render_template, redirect, url_for, session, request
from flask_pymongo import PyMongo
import bcrypt

from . import app
from .forms import EmailPasswordForm

mongo = PyMongo(app)


@app.route('/', methods=["GET", "POST"])
def index():
    form = EmailPasswordForm()
    if form.validate_on_submit() and "username" in session:
        message = "You are logged in as " + session["username"]
        return render_template("dashboard.html", message=message)
    return render_template('index.html', form=form)


@app.route('/login')
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        users = mongo.db.users
        form_username = request.form.get('email')
        existing_user = users.find_one({'username': form_username})
        if existing_user:
            form_pass = request.form.get('password')
            match_pass = bcrypt.hashpw(form_pass.encode('utf-8'), existing_user.password.encode('utf-8'))
            if match_pass:
                return redirect('/')

    return 'Combination email/password is invalid'


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = EmailPasswordForm()
    if form.validate_on_submit() and request.method == "POST":
        users = mongo.db.users
        form_username = request.form.get('email')
        form_pass = request.form.get('password')
        existing_user = users.find_one({'username': form_username})
        if existing_user is None:
            password = bcrypt.hashpw(form_pass.encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': form_username, 'password': password})
            session['username'] = form_username
            return redirect(url_for("index"))
        return "Username already exists"

    return render_template("register.html", form=form)
