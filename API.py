import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request

try:  # Surrounding the connection in a try-except block to catch all connection errors
    databaseConnection = mysql.connector.connect(  # Connection happens here
        host="localhost",
        user="root",
        password="NikoMySQL_13",
        database="warehousesystem"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  # If the username or password is wrong, it's caught here
        print("Error: your username or password are incorrect")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:  # If the database is incorrectly entered, it's caught here
        print("Error: the database you entered is either misspelled or does not exist")
    else:
        print(err)  # If the hostname is entered incorrectly, it's caught here

print(databaseConnection)  # Printing the successful connection


app = Flask(__name__)