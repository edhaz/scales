import random
from flask import redirect, render_template, request, session, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import select_scales, app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.completed:
        return render_template('finished.html')
    grades = ['4', '5']
    return render_template("index.html", grades=grades)


@app.route('/', methods=['GET', 'POST'])
@app.route('/about', methods=['GET', 'POST'])
def about():
    if current_user.is_authenticated:
        return redirect('index')
    return render_template("about.html")


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
    flash("Successfully logged out.")
    return redirect(url_for('about'))


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


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


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

    session['scales'] = select_scales.get_scales(session['instrument'], session['grade'])

    return redirect(url_for('practice'))


@app.route("/practice/done", methods=['GET', 'POST'])
def done():
    a = request.args.get('a', 'Saved', type=int)
    print(a)
    current_user.completed = True
    db.session.commit()
    return "Saved!"


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
        flash('Progress reset.')
        return redirect(url_for('user', username=current_user.username))
    else:
        return redirect(url_for('index'))
