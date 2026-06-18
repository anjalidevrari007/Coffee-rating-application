from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('coffee.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS coffees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        votes INTEGER
    )
    ''')

    c.execute("SELECT COUNT(*) FROM coffees")
    if c.fetchone()[0] == 0:
        coffees = [
            ("Espresso", 0),
            ("Latte", 0),
            ("Cappuccino", 0)
        ]
        c.executemany(
            "INSERT INTO coffees(name,votes) VALUES (?,?)",
            coffees
        )

    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('coffee.db')
    c = conn.cursor()

    c.execute("SELECT * FROM coffees")
    coffees = c.fetchall()

    conn.close()

    return render_template('demo1.html', coffees=coffees)

@app.route('/vote/<int:id>')
def vote(id):
    conn = sqlite3.connect('coffee.db')
    c = conn.cursor()

    c.execute(
        "UPDATE coffees SET votes=votes+1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)