from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='templates')

# Create a connection to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user data
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT,
              age INTEGER,
              dob DATE)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    dob = request.form['dob']

    # Validate age
    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        return "Age must be a positive integer."

    # Validate email
    if '@' not in email:
        return "Invalid email format."

    # Insert data into the database
    c.execute("INSERT INTO users (name, email, age, dob) VALUES (?, ?, ?, ?)",
              (name, email, age, dob))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/users')
def users():
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
