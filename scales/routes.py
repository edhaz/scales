import random
import json
from flask import redirect, render_template, request, session, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from scales import select_scales, app, db
from scales.forms import LoginForm, RegistrationForm
from scales.models import User


@app.before_first_request
def setup():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.completed:
            return render_template('finished.html')
        grades = ['4', '5']
        return render_template("index.html", grades=grades)
    return render_template("about.html")


@app.route('/sign_in', methods=['GET', 'POST'])
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


@app.route('/sign_out')
def logout():
    logout_user()
    flash("Successfully logged out.")
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


@app.route('/profile')
@login_required
def profile():
    username = request.args.get('user')
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@app.route("/redirecter", methods=['POST'])
@login_required
def redirecter():
    """Get list of scales"""

    session['instrument'] = request.form.get('instrument')
    session['grade'] = request.form.get('grade')
    current_user.last_instrument = session['instrument']
    current_user.last_grade = session['grade']
    db.session.commit()

    if not session['instrument']:
        flash('You need to select an instrument.')
        return redirect(url_for('index'))
    if not session['grade']:
        flash('You need to select a grade.')
        return redirect(url_for('index'))

    session['scales'] = [json.dumps(scale.__dict__) for scale in select_scales.get_scales(
        session['instrument'], session['grade'])]

    return redirect(url_for('practice'))


@app.route("/practice/save", methods=['GET', 'POST'])
def done():
    current_user.completed = True
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/practice", methods=['GET', 'POST'])
@login_required
def practice():
    """ Shows the scales to practice """
    if current_user.completed:
        return render_template('finished.html')
    instrument = session['instrument'].capitalize()
    grade = session['grade']
    scales = session['scales']
    random.shuffle(scales)
    return render_template('scales.html', scales=scales, instrument=instrument, grade=grade)


@app.route("/reset_progress", methods=['GET', 'POST'])
@login_required
def reset_progress():
    if current_user.completed:
        current_user.completed = False
        db.session.commit()
        flash('Progress reset')
        return redirect(url_for('profile', user=current_user.username))
    else:
        return redirect(url_for('index'))
