from flask import render_template, redirect, url_for

from . import app
from .forms import EmailPasswordForm


@app.route('/', methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():

        print("validated")

        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/dashboard')

def dashboard():
    return render_template('dashboard.html')
