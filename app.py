from flask import Flask, g, render_template, redirect, request, session
import os, sqlite3

app = Flask(__name__)

DATABASE = 'glossary.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS terms (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, term TEXT NOT NULL, definition TEXT NOT NULL, category TEXT, example TEXT)")
    db.commit()

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
