from flask import Flask, render_template, request, redirect, url_for, session
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from werkzeug.utils import secure_filename
from test import fetch_data
UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

  
app = Flask(__name__)
  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form_log_sig', methods =['POST'])
def form_log_sig():

	mesage = ''
	if request.method == 'POST' and 'email_log' in request.form and 'password_log' in request.form:
		email = request.form['email_log']
		password = request.form['password_log']

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
		user = cursor.fetchone()
		print(user)
		if user:
			session['loggedin'] = True
			session['name'] = user['name']
			session['email'] = user['email']
			mesage = 'Logged in successfully !'
			# print('done')
			# print(session)
			# uploaded_df = pd.read_csv('static\\uploads\\data.csv',encoding='unicode_escape')
			# uploaded_df_html = uploaded_df.to_html()
			return redirect('/tables')
		else:
			print('error')
			mesage = 'Please enter correct email / password !'
			return render_template('index.html')


	elif request.method == 'POST' and 'name_sup' in request.form and 'password_sup' in request.form and 'email_sup' in request.form :
		userName = request.form['name_sup']
		password = request.form['password_sup']
		email = request.form['email_sup']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			mesage = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			mesage = 'Invalid email address !'
		elif not userName or not password or not email:
			mesage = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user VALUES (% s, % s, % s)', (userName, email, password, ))
			mysql.connection.commit()
			mesage = 'You have successfully registered !'
			return render_template('index.html')


  
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
  
@app.route('/tables')
def tables():
	li=fetch_data()
	return render_template('tables.html',li=li)
	

if __name__ == "__main__":
    app.run(debug = True)