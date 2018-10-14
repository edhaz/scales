import random

from flask import Flask, redirect, render_template, request, session, url_for

import select_scales

app = Flask(__name__)

"""
DATABASE = '/scales.db'

def get_db():
    db = getattr(g, 'scales', None)
    if db is None:
        db = g.scales = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

with app.app_context():
    for scale in query_db('select * from scales'):
        print(scale['name'], 'has', scale['octaves'], 'octaves')

#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_scales', None)
#    if db is not None:
#        db.close()
"""

scales = []


@app.route("/")
def index():
    """Scales web app"""

    grades = ['4', '5']

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

    session['scales'] = select_scales.get_scales(session['instrument'], session['grade'])

    return redirect(url_for('scales'))


@app.route("/", methods=['GET', 'POST'])
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
