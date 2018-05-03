import sqlite3
import random
from flask import Flask, redirect, render_template, request, session, g, url_for, jsonify
from flask_session import Session

app = Flask(__name__)

#DATABASE = '/scales.db'

#def get_db():
#    db = getattr(g, '_scales', None)
#    if db is None:
#        db = g._scales = sqlite3.connect(DATABASE)
#    return db

scales = []

@app.route("/")
def index():
    """Scales web app"""
    
    grades = ['4','5']

    return render_template("scalesindex.html", grades=grades)

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
            session['scales'] = ['Ab major, 2 octaves', 'B major, 2 octaves', 'C major, 2 octaves', 'E major, 2 octaves', 'G minor, 2 octaves', 'B minor, 2 octaves', 'C minor, 2 octaves']
        elif session['grade'] == '5':
            session['scales'] = ['Db major', 'Eb major', 'F major', 'B minor', 'C# minor', 'E minor']
    elif session['instrument'] == 'piano':
        if session['grade'] == '4':
            session['scales'] = ['test1', 'test2']
        elif session['grade'] == '5':
            session['scales'] = ['test1', 'test2']

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