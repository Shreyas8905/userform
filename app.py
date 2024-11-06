from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'form'

mysql = MySQL(app)


# Route for displaying the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        address = request.form['address']
        phone_no = request.form['phone_no']
        email = request.form['email']
        closed_one_name = request.form['closed_one_name']
        closed_one_phone = request.form['closed_one_phone']
        closed_one_relation = request.form['closed_one_relation']

        # Check if user already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # User already exists
            return render_template('index.html', user_exists=True, user=existing_user)
        else:
            # Insert new user into the database
            cursor.execute("""
                INSERT INTO users (name, address, phone_no, email, closed_one_name, closed_one_phone, closed_one_relation)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, address, phone_no, email, closed_one_name, closed_one_phone, closed_one_relation))
            mysql.connection.commit()
            cursor.close()

            # Redirect to the URL with user details
            return redirect(url_for('user_details', email=email))

    return render_template('index.html', user_exists=False)


# Route to display user details
@app.route('/user/<email>')
def user_details(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template('user_details.html', user=user)
    else:
        return "User not found", 404


if __name__ == '__main__':
    app.run(debug=False)
