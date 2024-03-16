from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Create a connection to SQLite database
conn = sqlite3.connect('your.db', check_same_thread=False)
c = conn.cursor()

# Create a table to store user data
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT,
              name TEXT,
              email TEXT,
              age INTEGER,
              dob DATE)''')
conn.commit()

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database to check if the username and password are valid
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()

        if user:
            session['username'] = username  # Store the username in the session
            flash('Login successful!', 'success')
            return redirect(url_for('users'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

# Secure route that requires authentication
@app.route('/users')
def users():
    if 'username' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    c.execute("SELECT * FROM users")
    users = c.fetchall()
    return render_template('users.html', users=users)

# Home route
@app.route('/')
def home():
    return render_template('home.html')


# Create user route
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        is_edit = bool(int(request.form.get('edit_mode', 0)))
        if is_edit:
            # This is an edit request, handle updating user details
            user_id = request.form['user_id']
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']
            dob = request.form['dob']

            # Update user data in the database
            try:
                c.execute("""
                    UPDATE users 
                    SET username = ?, password = ?, name = ?, email = ?, age = ?, dob = ?
                    WHERE id = ?
                """, (username, password, name, email, age, dob, user_id))
                conn.commit()
                flash('User details updated successfully!', 'success')
                return redirect(url_for('users'))  # Redirect to users list after successful update
            except sqlite3.Error as e:
                flash(f'Error updating user details: {e}', 'error')
                return redirect(url_for('create_user'))

        else:
            # This is a new user creation request
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']
            dob = request.form['dob']

            # Insert user data into the database
            try:
                c.execute("""
                    INSERT INTO users (username, password, name, email, age, dob)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (username, password, name, email, age, dob))
                conn.commit()
                flash('User created successfully!', 'success')

                # Determine the source page and redirect accordingly
                if request.referrer.endswith('/login'):
                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('users'))  # Redirect to users list after successful user creation

            except sqlite3.IntegrityError:
                flash('Username already exists, please choose another one', 'error')
                return redirect(url_for('create_user'))

    else:
        # Check if it's an edit request and get the user details
        if 'edit_mode' in request.args:
            user_id = request.args.get('id')
            c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = c.fetchone()
            if user:
                return render_template('createuser.html', user=user, edit_mode=True)
            else:
                flash("User not found.", "error")
                return redirect(url_for('users'))
        else:
            return render_template('createuser.html')


# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Logic for initiating password reset
        # Redirect to login page after initiating password reset
        return redirect(url_for('login'))  # Use the correct endpoint name 'login' or 'forgot_password' if available
    else:
        return render_template('forgotpassword.html')

# Index route
@app.route('/')
def index():
    return render_template('home.html')

# Edit user route
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        # Form submission code...
        pass
    else:
        c.execute("SELECT * FROM users WHERE id = ?", (id,))
        user = c.fetchone()
        if user:
            return render_template('createuser.html', user=user)
        else:
            flash("User not found.", "error")
            return redirect(url_for('users'))

# Delete user route
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)