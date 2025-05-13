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

def get_cursor():
    return get_db().cursor()

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)

@app.route("/view")
def view_terms():
    search = request.args.get("search", "").strip()
    db = get_cursor()
    terms = db.execute("SELECT * FROM terms WHERE term LIKE ? ORDER BY term ASC", (f"%{search}%",)).fetchall()
    return render_template('viewer.html', terms=terms)

@app.route("/entry", methods=["GET", "POST"])
def add_term():
    return ("Page under construction")

@app.route("/edit", methods=["GET", "POST"])
def edit_term():
    return ("Page under construction")

@app.route("/delete", methods=["GET", "POST"])
def delete_term():
    return ("Page under construction")

@app.route("/login", methods=["GET", "POST"])
def login():
    return ("Page under construction")