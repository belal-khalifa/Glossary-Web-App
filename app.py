from flask import Flask, flash, g, render_template, redirect, request, session, url_for
import os, sqlite3

app = Flask(__name__)
app.secret_key = "staticfornow"
DATABASE = os.path.join(os.getcwd(),'glossary.db')

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
    app.run(debug=True)

if not os.path.exists(DATABASE):
    with app.app_context():
        init_db()

@app.route("/")
def view_terms():
    search = request.args.get("search", "").strip()
    db = get_cursor()
    terms = db.execute("SELECT * FROM terms WHERE term LIKE ? ORDER BY term ASC", (f"%{search}%",)).fetchall()
    return render_template('viewer.html', terms=terms)

@app.route("/entry", methods=["GET", "POST"])
def add_term():
    if request.method=='GET':
        return render_template('entry.html')
    newterm = request.form.get('term', '')
    category = request.form.get('category', '')
    definition = request.form.get('definition', '')
    example = request.form.get('example', '')
    if not all(field.strip() for field in [newterm, category, definition]):
        flash("Term, Definition and Category are required")
        return render_template('entry.html', term={'term':newterm,'category':category,'definition':definition,'example':example})
    else:
        db = get_cursor()
        db.execute("INSERT INTO terms (term, definition, category, example) VALUES (?, ?, ?, ?)", (newterm, definition, category, example))
        get_db().commit()
        flash(f'Term "{newterm}" added successfully!')
        return redirect(url_for('add_term'))

@app.route("/edit/<int:term_id>", methods=["GET", "POST"])
def edit_term(term_id):
    if request.method=="GET":
        term = get_cursor().execute("SELECT * FROM terms WHERE id = ?",(term_id,)).fetchone()
        if not term:
            flash("Term not found")
            return redirect(url_for('view_terms'))
        return render_template('edit.html', term=term)
    term = request.form.get('newterm', '').strip()
    category = request.form.get('category', '').strip()
    definition = request.form.get('definition', '').strip()
    example = request.form.get('example', '').strip()
    for k,v in {'term':term, 'category':category, 'definition':definition, 'example':example}.items():
        if v:
            get_cursor().execute(f"UPDATE terms SET {k} = ? WHERE id = ?",(v, term_id))
    get_db().commit()
    flash(f"Term {term} updated successfully!")
    return redirect(url_for('view_terms'))

@app.route("/delete/<int:term_id>", methods=["POST"])
def delete_term(term_id):
    term = get_cursor().execute("SELECT term FROM terms WHERE id = ?",(term_id,)).fetchone()
    get_cursor().execute("DELETE FROM terms WHERE id = ?",(term_id,))
    flash(f"Term {term['term']} deleted successfully!")
    get_db().commit()
    return redirect(url_for('view_terms'))

