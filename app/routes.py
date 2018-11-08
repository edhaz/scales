import random
from flask import redirect, render_template, request, session, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import select_scales, app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    grades = ['4', '5']
    return render_template("index.html", grades=grades)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/redirecter", methods=['POST'])
@login_required
def redirecter():
    """Get list of scales"""

    session['instrument'] = request.form.get('instrument')
    session['grade'] = request.form.get('grade')

    if not session['instrument']:
        return redirect(url_for('scales'))
    elif not session['grade']:
        return redirect(url_for('scales'))

    session['scales'] = select_scales.get_scales(session['instrument'], session['grade'])

    return redirect(url_for('practice'))


@app.route("/practice", methods=['GET', 'POST'])
@login_required
def practice():
    """ Shows the scales to practice """
    instrument = session['instrument'].capitalize()
    grade = session['grade']
    try:
        scales = session['scales']
        random.shuffle(scales)
        return render_template('/scales.html', scales=scales, instrument=instrument, grade=grade)
    except IndexError:
        return render_template('/finished.html', instrument=instrument, grade=grade)

