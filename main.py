import MySQLdb
from flask import Flask, render_template, redirect, session, url_for, request, flash
from flask_mysqldb import MySQL
from werkzeug.routing import ValidationError
"""
 these are the  pythonmodules if you dont have installed these modules on your computer, install them before running the code
 """

# informations  from database to pass html file
headings = ('Name', 'Password ', 'Email')
data = []
# fill the below accordingly
import MySQLdb
hostnameDB= ""
usernameDB= ""
passwordDB= ""
dbname = "login"
db = MySQLdb.connect(host=hostnameDB,  # your host, usually localhost
                     user=usernameDB,  # your username
                     passwd=passwordDB,  # your password
                     db=dbname)  # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT name,password,email FROM logininfo")


counter = 0;

app = Flask(__name__)
app.secret_key = "1111"
app.config["MYSQL_HOST"] = hostnameDB
app.config["MYSQL_USER"] = usernameDB
app.config["MYSQL_PASSWORD"] = passwordDB
app.config["MYSQL_DB"] = dbname

db = MySQL(app)

# this is the method for login
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form :
            username = request.form['username']
            # print("see")
            password = request.form['password']
            if(username!= "" and password!=""):
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM logininfo WHERE email=%s  AND password=%s", (username, password))
                info = cursor.fetchone()

                if info is not None:
                    if info['email'] == username and info['password'] == password:
                        session['loginsuccess'] = True
                        return redirect(url_for('profile'))
                else:
                    flash('Your password or username is wrong try again!!!')
                    request.form['password'] != 'secret'
                    error = 'Invalid credentials'

                    return redirect(url_for('index'))
            else:
                flash('You have not typed anything.Fill the necessary blanks to login!!!')
                request.form['password'] != 'secret'
                error = 'Invalid credentials'

                return redirect(url_for('index'))


    return render_template("login.html", error=error)




#this is the function to register
@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            username = request.form['one']
            email = request.form['two']
            password = request.form['three']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            flag = False
            if (username != "" and email != "" and password != ""):
                cur.execute("INSERT INTO logininfo (name,password,email) VALUES(%s, %s, %s)",
                            (username, password, email))
                tuple_ = (username, password, email)
                data.append(tuple_)
                db.connection.commit()
                flag = True
            if (flag == True):
                flash("you are successfuly registered now go back to login ")
            else:
                flash("please fill all the blanks correctly!")
            return redirect(url_for('new_user'))


    return render_template("register.html")

# this is the function to check if login is succesfull
@app.route('/new/profile')
def profile():
    if session['loginsuccess']:
        return render_template("profile.html", headings=headings, data=data)


if __name__ == '__main__':
    for row in cur.fetchall():
        data.append(row)
    app.run(debug=True)

    db.close()
