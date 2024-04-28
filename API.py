import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request
from getpass import getpass

app = Flask(__name__)
try:  # Surrounding the connection in a try-except block to catch all connection errors
    password = getpass("Enter your password for MySQL: ")
    conn = mysql.connector.connect(user="root", password=password,
                                   host='127.0.0.1', database="WarehouseSystem")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  # If the username or password is wrong, it's caught here
        print("Error: your username or password are incorrect")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:  # If the database is incorrectly entered, it's caught here
        print("Error: the database you entered is either misspelled or does not exist")
    else:
        print(err)  # If the hostname is entered incorrectly, it's caught here

print(conn)  # Printing the successful connection


@app.route("/employee/get_all", method=['GET'])
def get_all():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return jsonify({'message': "There are no tasks for all users."})
    else:
        return jsonify(data), 200


@app.route("/employee/create_user", method=['POST'])
def create_user():
    cursor = conn.cursor()
    data = request.json
    new_first = data.get('firstName')
    new_middle = data.get('middleName')
    new_last = data.get('lastName')
    job_title = data.get('jobTitle')
    new_username = data.get('username')
    new_password = data.get('password')
    if new_first is None:
        return jsonify({'message': 'First Name is a required field!'}), 400
    elif new_last is None:
        return jsonify({'message': 'Last Name is a required field!'}), 400
    elif new_username is None or new_password is None:
        return jsonify({'message': 'Missing Username or Password; Both are required before proceeding'}), 400
    try:

        insert_query_employee = "INSERT INTO Employee (firstName, middleName, lastName, jobTitle) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query_employee, (new_first, new_middle, new_last, job_title))
        conn.commit()
        cursor.execute("SELECT employeeID FROM Employee ORDER BY employeeID DESC LIMIT 1")
        last_employee_id = cursor.fetchone()[0]
        insert_query_login = "INSERT INTO Login (username, hashedPassword, employeeId) VALUES (%s, %s, %s)"
        cursor.execute(new_username, new_password, last_employee_id)
        return jsonify({"message": f"New employee data is added successfully for {last_employee_id} - {new_first} {new_last}"}), 201
    except Exception as e:
        return jsonify({"message": f"Failed to create a new user for {new_first} {new_last}", "error": str(e)}), 500


# URL Template: "/<table_name>/<function>/<item_or_order_number> (if needed)
