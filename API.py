import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request
from getpass import getpass


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

app = Flask(__name__)

@app.route("/employee/get_all", methods=['GET'])
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return jsonify({'message': "There are no information on employees. Please make sure the data is added."})
    else:
        return jsonify(data), 200


@app.route("/employee/create_user", methods=['POST'])
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


@app.route("/login/update_username/<string:curr_user>", method=['POST'])
def update_username(curr_user):
    cursor = conn.cursor()
    data = request.json
    new_username = data.get('new_username')
    if new_username is None:
        return jsonify({'message': 'New Username is a required field!'}), 400
    try:
        cursor.execute("UPDATE Login SET username = %s WHERE username = %s", (new_username, curr_user))
        conn.commit()
        return jsonify({"message": f"Username is changed successfully to {new_username}"}), 201
    except Exception as e:
        return jsonify(
            {"message": f"Failed to change the username to {new_username}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/login/update_password/<string:curr_user>", method=['POST'])
def update_username(curr_user):
    cursor = conn.cursor()
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if old_password is None:
        return jsonify({'message': 'Old password is a required field!'}), 400
    elif new_password is None:
        return jsonify({'message': 'New password is a required field!'}), 400
    try:
        cursor.execute("UPDATE Login SET hashedPassword = %s WHERE username = %s and hashedPassword = %s",
                       (new_password, curr_user, old_password))
        conn.commit()
        return jsonify({"message": f"Username is changed successfully to {new_password}"}), 201
    except Exception as e:
        return jsonify(
            {"message": f"Failed to change the username to {new_password}", "error": str(e)}), 500
    finally:
        cursor.close()

@app.route("/warehouse/get_warehouses", methods=['GET'])
def get_warehouses():
    cursor = conn.cursor()
    cursor.execute("SELECT w.warehouseID, w.capacity, a.addressNum, a.street, a.city, a.zipcode "
                   "FROM warehouse w "
                   "INNER JOIN addresses a "
                   "ON w.warehouseAddressID = a.addressID")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return jsonify({'message': "There are no warehouses in the system."})
    else:
        return jsonify(data), 200


@app.route('/warehouse/update_warehouse', methods=['PUT'])
def update_warehouse():
    data = request.json
    warehouseID = data[0]
    warehouseAddressID = data[1]
    capacity = data[2]
    addressNum = data[3]
    street = data[4]
    city = data[5]
    zipCode = data[6]

    if warehouseID is None or warehouseAddressID is None or capacity is None or addressNum is None\
            or capacity is None or street is None or city is None or zipCode is None:
        return jsonify({'message': 'To update the warehouse, you must provide the current warehouseID and '
                                   'warehouseAddressID, then provide the updated addressID, capacity,'
                                   'addressNum, street, city, and zipCode'}), 400

    try:
        cursor = conn.cursor()
        # Update data in warehouse
        update_query = "UPDATE Warehouse SET capacity = %s WHERE warehouseID = %s"
        cursor.execute(update_query, (capacity, warehouseID))
        conn.commit()

        # Update related address data
        update_query = ("UPDATE Addresses SET addressNum = %s, street = %s, city = %s, zipCode = %s "
                          "WHERE addressID = %s")
        cursor.execute(update_query, (addressNum, street, city, zipCode, warehouseAddressID))
        conn.commit()
        return jsonify({'message': 'Data updated successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to update data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route("/orders/get_orders", methods=['GET'])
def get_orders():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no orders in the system."})
    else:
        cursor.execute("SELECT * FROM ItemsOrdered ORDER BY orderID")
        data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


@app.route('/orders/delete_order', methods=['DELETE'])
def delete_order():
    data = request.json
    orderID = data[0]

    if orderID is None:
        return jsonify({'message': 'orderID is a required field'}), 400

    try:
        cursor = conn.cursor()
        delete_query = "DELETE from ItemsOrdered Where orderID = %s"
        cursor.execute(delete_query, (orderID,))

        delete_query = "Delete from Orders Where orderID = %s"
        cursor.execute(delete_query, (orderID,))
        conn.commit()
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route("/item/get_items", methods=['GET'])
def get_items():
    cursor = conn.cursor()
    cursor.execute("SELECT i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity, w.warehouseID "
                   "FROM Item i INNER JOIN ItemInWarehouse w ON i.itemID = w.itemID")
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items in the system."})
    else:
        # The following command will get all ordered items and display the total amount of those items that are
        # on order status across all orders
        cursor.execute("SELECT i.itemName, SUM(o.itemQuantity) AS totalQuantity "
                       "FROM Item i INNER JOIN ItemsOrdered o "
                       "ON i.itemID = o.itemID "
                       "GROUP BY itemName")
        data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)

# URL Template: "/<table_name>/<function>/<item_or_order_number> (if needed)
