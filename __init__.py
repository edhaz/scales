import sqlite3
import random
from flask import Flask, render_template, g

app = Flask(__name__)

DATABASE = '/scales.db'

scales = ['Ab major', 'B major', 'C major', 'E major', 'G minor', 'B minor', 'C minor']

def get_db():
    db = getattr(g, '_scales', None)
    if db is None:
        db = g._scales = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    scale = random.choice(scales)
    return render_template("scales.html", scale=scale)


if __name__ == "__main__":
    app.run()
