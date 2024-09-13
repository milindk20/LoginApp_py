import time
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

#======================================Custom Functions=======================================================
def session_check():
    if session['logged_in'] == True:
        check=1
        print(check)
    else:
        check=0
    return check
#===========================================================================================================



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
        print(session)
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# create_user route
@app.route('/create_user', methods=['GET', 'POST'])
def redirect_to_create_user():
    if session_check()==1:
        return render_template('create_user.html')
    elif session_check() !=1:
            return redirect(url_for('login'))


# create_new_user route
@app.route('/create_new_user', methods=['GET', 'POST'])
def create_new_user():
    if session_check()==1:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            #Checkes if username or email exists already
            #if  (cursor.execute('SELECT count(1) FROM users WHERE username = %s', (username)) >=1):
             #   flash(f'Username {username} already exists!! please try a different one!!')
           # if  (cursor.execute('SELECT count(1) FROM users WHERE email = %s', (email)) >=1):
            #    flash(f'email {email} already exists!! please try a different one!!')
            # Query database to insert the new user exists
#            else:    
            cursor.execute('INSERT INTO users (username,email, password) VALUES (%s,%s, %s);', (username,email, password))
            cursor.execute('commit')
            flash(f'User "{username}" ha been created successfully!!','success')
        return render_template('create_user.html')
    
    elif session_check() !=1:
            return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))



# StartApp
if __name__ == '__main__':
    app.run(debug=True)
