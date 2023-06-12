import json
import random

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from . import app, store
from .forms import LoginForm, RegistrationForm
from .models import User


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        if current_user.completed:
            return render_template("finished.html")
        grades = ["4", "5"]
        return render_template("index.html", grades=grades)
    return render_template("about.html")


@app.route("/sign_in", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = store.get_user_by_name(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/sign_out")
def logout():
    logout_user()
    flash("Successfully logged out.")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        store.create_user(form.username.data, form.email.data, form.password.data)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/profile")
@login_required
def profile():
    username = request.args.get("user")
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", user=user)


@app.route("/redirecter", methods=["POST"])
@login_required
def redirecter():
    """Get list of scales"""
    instrument = request.form.get("instrument")
    grade = request.form.get("grade")

    if not instrument or not grade:
        flash("You need to select an instrument and a grade.")
        return redirect(url_for("index"))

    store.update_current_user_selection(instrument, grade)
    session["scales"] = [json.dumps(scale.__dict__) for scale in store.get_scales_from_csv(instrument, grade)]

    return redirect(url_for("practice"))


@app.route("/practice/save", methods=["GET", "POST"])
def done():
    store.user_completed(True)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    """Shows the scales to practice"""
    if current_user.completed:
        return render_template("finished.html")
    instrument = current_user.last_instrument.capitalize()
    grade = current_user.last_grade
    scales = session["scales"]
    random.shuffle(scales)
    return render_template("scales.html", scales=scales, instrument=instrument, grade=grade)


@app.route("/reset_progress", methods=["GET", "POST"])
@login_required
def reset_progress():
    if current_user.completed:
        store.user_completed(False)
        flash("Progress reset")
        return redirect(url_for("profile", user=current_user.username))
    else:
        return redirect(url_for("index"))
