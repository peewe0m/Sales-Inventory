from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import yaml

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load MySQL configuration from YAML file
db_config = yaml.safe_load(open('db_config.yaml'))

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=db_config['mysql_host'],
        user=db_config['mysql_user'],
        password=db_config['mysql_password'],
        database=db_config['mysql_db']
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        flash('Login successful!', 'success')
        return redirect(url_for('main', username=username))  # Pass username to main page
    else:
        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('home'))

@app.route('/main')
def main():
    username = request.args.get('username', 'User')
    return render_template('main.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        
        # Insert new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

# @app.route('/main')
# def main():
#     return render_template('main.html')


