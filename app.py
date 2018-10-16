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


"""-------Scales-------"""


@app.route("/", methods=['GET', 'POST'])
def scales():
    """Scales web app"""
    grades = ['4']
    return render_template("/scalesindex.html", grades=grades)


@app.route("/redirecter", methods=['POST'])
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
def practice():
    """ Shows the scales to practice """
    instrument = session['instrument'].capitalize()
    grade = session['grade']
    try:
        scales = session['scales']
        # TODO shuffle scales list
        scale = random.choice(session['scales'])
        return render_template('/scales.html', scale=scale, scales=scales, instrument=instrument, grade=grade)
    except IndexError:
        return render_template('/finished.html', instrument=instrument, grade=grade)


app.secret_key = 'test'

if __name__ == "__main__":
    app.run()
