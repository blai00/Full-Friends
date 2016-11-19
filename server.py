from flask import Flask, request, redirect, render_template, session, flash
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friends')
app.secret_key = "very secret"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
@app.route('/' , methods = ['GET'])
def index():
	query = 'SELECT * FROM friends'
	data = {}
	friends = mysql.query_db(query, data)
	return render_template('index.html', friends=friends)

@app.route('/friends' , methods=['POST'])
def create():
	data = request.form
	print data 

	if not request.form['first_name']:
		flash("Please enter a first name")
		return redirect('/')
	elif len(request.form['first_name']) < 2:
		flash('Your name should be longer than 2 characters')
		return redirect('/')
	if not request.form['last_name']:
		flash("Please enter a last name ")
		return redirect('/')
	elif len(request.form['first_name']) < 2:
		flash('Your last name should be longer than 2 characters')
		return redirect('/')
	if not request.form['email']:
		flash("Please enter an email ")
		return redirect('/')
	elif len(request.form['email']) < 2:
		flash('Your email should be longer than 2 characters')
		return redirect('/')
	if not EMAIL_REGEX.match(request.form['email']):	
		flash('Please enter a valid email address')
		return redirect('/')
	else:
		query = "INSERT INTO friends (first_name, last_name, email, created_at) VALUES(:first_name, :last_name, :email, NOW())"

		data = {
					'first_name' :request.form['first_name'],
					'last_name'  :request.form['last_name'],
					'email'		 :request.form['email']	
		}

		mysql.query_db(query,data)
		return redirect('/')

@app.route('/friends/<id>/edit' , methods = ['GET'])
def edit(id):
	query = "SELECT * FROM friends where id =:id"
	data = {
		'id': friend_id
	}

	friend = mysql.query_db(query,data)
	return render_template('edit.html', friend=friend)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	query ="Update friends SET first name = :first_name, last_name = :last_name, email = :email WHERE id = :id"

	data ={
			'first_name' : request.form['first_name'],
			'last_name'  : request.form['last_name'],
			'email'      : request.form['email'],
			'id'         : friend_id  
	}

	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/delete' , methods=['POST'])
def delete(id):
	query = "DELETE FROM friends WHERE id =:id"
	data = {'id : friend_id'}
	mysql.query_db(query,data)
	return redirect('/')


if __name__ == "__main__":
	app.run(debug=True)