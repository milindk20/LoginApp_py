from getpass import getuser
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
    if 'logged_in' in session and session['logged_in']:
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
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s;', (username, password))
        user = cursor.fetchone()
        print(session)
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password','danger')
    
    return render_template('login.html')


# create_new_user route
@app.route('/create_new_user', methods=['GET', 'POST'])
def create_new_user():
    if session_check()==1:
        if request.method == 'POST':
            username = str(request.form['username'])
            email = str(request.form['email'])
            role = str(request.form['role'])
            name = str(request.form['name'])
            mobileno = str(request.form['mobileno'])
            password = str(request.form['password'])

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            flag=0
            #Checkes if username exists already
            cursor.execute(f'SELECT count(1) as "countofuser" FROM users WHERE username = "{username}"')
            count=cursor.fetchone()
            if (count['countofuser'] >=1):
                flash(f'Username \"{username}\" already exists!! please try a different one!!','danger')
                flag=1
            #Checkes if email exists already
            cursor.execute(f'SELECT count(1) as "countofuser" FROM users WHERE email = "{email}"')
            count=cursor.fetchone()
            if (count['countofuser'] >=1):
                flash(f'email \"{email}\" already exists!! please try a different one!!','danger')
                flag=1
            # Query database to insert the new user exists
            if flag==0:
                cursor.execute('INSERT INTO users (username,email, password,role,name,mobileno) VALUES (%s,%s, %s,%s,%s,%s);', 
                               (username,email, password,role,name,mobileno))
                cursor.execute('commit')
                flash(f'User "{username}" has been created successfully!!','success')
        return render_template('create_user.html')
    
    elif session_check() !=1:
            return redirect(url_for('login'))


# users_list route
@app.route('/users_list')
def users_list():
    if session_check()==1:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return render_template('users_list.html', users=users)

    elif session_check() !=1:
            return redirect(url_for('login'))
    
@app.route('/profile')
def profile():
    if session_check()==1:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        username=session['username']
        cursor.execute(f'SELECT * FROM users where username=\'{username}\'')
        users = cursor.fetchone()
        return render_template('profile.html', user=users)

    elif session_check() !=1:
            return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Example: Check if the user is logged in
    if session_check():
        if request.method == 'POST':
            # Handle the form submission for profile editing
            username=session['username']
            new_email = request.form.get('email')
            new_name = request.form.get('name')
            new_role = request.form.get('role')
            new_mobileno = request.form.get('mobileno')
            # Update the user in the database logic here...
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                '''
                UPDATE users 
                SET email = %s, role = %s, name = %s, mobileno = %s 
                WHERE username = %s
                ''', 
                (new_email, new_role, new_name, str(new_mobileno), username)
            )
            cursor.execute('commit')
            flash(f'User "{username}" has been created successfully!!','success')
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))  # Redirect to the profile page after successful update

        if request.method=="GET":  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            username=session['username']
            cursor.execute(f'SELECT * FROM users where username=\'{username}\'')
            users = cursor.fetchone()
        # Render the edit profile page
        #user = getuser()  # Replace with your user-fetching logic
        return render_template('edit_profile.html', user=users)

    else:
        return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # Example: Check if the user is logged in
    if session_check():
        if request.method == 'POST':
            # Handle the form submission for profile editing
            username=session['username']
            current_password = request.form.get('current-password')
            new_password = request.form.get('new-password')
            confirm_password = request.form.get('confirm-password')
            # Update the user in the database logic here...
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f'SELECT password FROM users where username=\'{username}\'')
            old_password=cursor.fetchone()['password']
            print(old_password)
            if old_password==current_password:
                if new_password==confirm_password:
                    cursor.execute(
                        '''
                        UPDATE users 
                        SET password=%s
                        WHERE password=%s and username = %s
                        ''', 
                        (confirm_password,current_password, username)
                    )
                    cursor.execute('commit')
                    flash('Password changed successfully','success')
                else:
                    flash('new password did not matched with the confirm password, please try again !!','danger')
            else:
                flash("Current password didnot match, please try again!!",'danger')

            return redirect(url_for('profile'))  # Redirect to the profile page after successful update

        if request.method=="GET":  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            username=session['username']
            cursor.execute(f'SELECT * FROM users where username=\'{username}\'')
            users = cursor.fetchone()
        # Render the edit profile page
        #user = getuser()  # Replace with your user-fetching logic
        return render_template('change_password.html', user=users)

    else:
        return redirect(url_for('login'))


# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))



# StartApp
if __name__ == '__main__':
    app.run(debug=True)
