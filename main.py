from functools import wraps
from flask import Flask, render_template
from flask import redirect, url_for, request
from flask import session, flash
import requests

app = Flask(__name__)

app.secret_key = "QWERTY"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/home')
@login_required
def home():
    return render_template("home.html")


@app.route('/Sport')
def sport():
    return render_template("Sports.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'

        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return render_template('logout.html')


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route('/SportsQuiz')
def sq():
    return render_template("sportsquiz.html")


@app.route('/Geo')
def Geo():
    return render_template("Geo.html")


@app.route('/Geoquiz')
def geog():
    return render_template("geoquiz.html")


@app.route('/GK')
def GK():
    return render_template("gk1.html")


@app.route('/GKQuiz')
def gkq():
    return render_template("gkquiz.html")


@app.route('/AboutUs')
def about():
    return render_template("aboutus.html")





if __name__ == "__main__":
    app.run(debug=True)
