import sqlite3
import random
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, g, url_for, jsonify
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)


#DATABASE = '/scales.db'

#def get_db():
#    db = getattr(g, '_scales', None)
#    if db is None:
#        db = g._scales = sqlite3.connect(DATABASE)
#    return db

#scales = ['Ab major', 'B major', 'C major', 'E major', 'G minor', 'B minor', 'C minor']

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index_test.html')

"""@app.route("/", methods=["GET", "POST"])
def index():
    """ """Scales web app""" """

    grades = ['1','2','3','4','5','6','7','8']

    if request.method == "POST":
        if not request.form.get("instrument"):
            return render_template("index.html", grades=grades)
        elif not request.form.get("grade"):
            return render_template("index.html", grades=grades)
        
        instrument = request.form.get("instrument")
        grade = request.form.get("grade")

        if instrument == 'violin':
            if grade == '4':
                scales = ['Ab major', 'B major', 'C major', 'E major', 'G minor', 'B minor', 'C minor']

        #while scales:
        #    scale = random.choice(scales)
        #    scales.remove(scale)

        return render_template("scales.html", instrument=instrument, grade=grade, scales=scales)

 
    else:
        return render_template("index.html", grades=grades)
"""

#if __name__ == "__main__":
#    app.run()