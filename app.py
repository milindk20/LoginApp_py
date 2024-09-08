from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

#==================================================ConfigFile==================================================
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('C:\\Users\\Milind\\Desktop\\projects\\LoginApp_py\\config.conf')

# Accessing data from the 'database' section
db_host = config.get('database', 'host')
db_port = config.getint('database', 'port')  # Convert to int
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_dbname = config.get('database', 'databasename')

# Accessing data from the 'Flask' section
Flask_app_session_secretKey = config.get('flask_session', 'key')
#===========================================================================================================

app = Flask(__name__)
app.secret_key = Flask_app_session_secretKey # sessionKey

# Configure MySQL connection
app.config['MYSQL_HOST'] = db_host
app.config['MYSQL_USER'] = db_user
app.config['MYSQL_PASSWORD'] = db_password
app.config['MYSQL_DB'] = db_dbname

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query database to check if the user exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
