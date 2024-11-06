from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS medications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    dosage TEXT,
                    time TEXT,
                    date TEXT,
                    taken BOOLEAN DEFAULT 0
                )''')
    conn.commit()
    conn.close()

init_db()

# Route to view and add medications
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        time = request.form['time']
        date = datetime.now().strftime('%Y-%m-%d')  # Current date

        # Save medication data
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO medications (name, dosage, time, date) VALUES (?, ?, ?, ?)",
                  (name, dosage, time, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    # Display upcoming doses
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM medications WHERE date >= ? ORDER BY date, time", (datetime.now().strftime('%Y-%m-%d'),))
    medications = c.fetchall()
    conn.close()

    return render_template('index.html', medications=medications)

# Route to mark medication as taken
@app.route('/take/<int:id>', methods=['POST'])
def take_medication(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE medications SET taken = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route for medication history
@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM medications WHERE taken = 1 ORDER BY date DESC, time DESC")
    medications = c.fetchall()
    conn.close()
    return render_template('history.html', medications=medications)

if __name__ == '__main__':
    app.run(debug=True)
