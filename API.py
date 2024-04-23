import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request
from getpass import getpass

app = Flask(__name__)
try:  # Surrounding the connection in a try-except block to catch all connection errors
    password = getpass("Enter your password for MySQL: ")
    conn = mysql.connector.connect(user="root", password=password,
                                   host='127.0.0.1', database="warehousesystem")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  # If the username or password is wrong, it's caught here
        print("Error: your username or password are incorrect")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:  # If the database is incorrectly entered, it's caught here
        print("Error: the database you entered is either misspelled or does not exist")
    else:
        print(err)  # If the hostname is entered incorrectly, it's caught here

print(conn)  # Printing the successful connection

# URL Template: "/<table_name>/<function>/<item_or_order_number> (if needed)

app = Flask(__name__)