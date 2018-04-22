import sqlite3
import random
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, g, url_for, jsonify, escape
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

#DATABASE = '/scales.db'

#def get_db():
#    db = getattr(g, '_scales', None)
#    if db is None:
#        db = g._scales = sqlite3.connect(DATABASE)
#    return db

scales = []


@app.route("/", methods=['GET', 'POST'])
def index():
    """Scales web app"""
    
    grades = ['1','2','3','4','5','6','7','8']

    return render_template("index.html", grades=grades)

@app.route("/redirecter", methods=['POST'])
def redirecter():
    """Get list of scales"""
    
    session['instrument'] = request.form.get('instrument')
    session['grade'] = request.form.get('grade')

    if not session['instrument']:
        return redirect('/')
    elif not session['grade']:
        return redirect('/')

    if session['instrument'] == 'violin':
        if session['grade'] == '4':
            session['scales'] = ['Ab major', 'B major', 'C major', 'E major', 'G minor', 'B minor', 'C minor']
        elif session['grade'] == '5':
            session['scales'] = ['Db major', 'Eb major', 'F major', 'B minor', 'C# minor', 'E minor']

    return redirect(url_for('scales'))

@app.route("/scales", methods=['GET', 'POST'])
def scales():
    """ Shows the scales to practice """
    instrument = session['instrument'].capitalize()
    grade = session['grade']
    try:
        session['scales_tmp'] = session['scales']
        scale = random.choice(session['scales_tmp'])
        session['scales_tmp'].remove(scale)
        return render_template('scales.html', scale=scale, instrument=instrument, grade=grade)
    except IndexError:
        return render_template('finished.html', instrument=instrument, grade=grade)


app.secret_key = 'test'
app.run(debug=True)

if __name__ == "__main__":
    app.run()