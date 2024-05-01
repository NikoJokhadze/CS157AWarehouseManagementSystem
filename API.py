import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request
from getpass import getpass


try:  # Surrounding the connection in a try-except block to catch all connection errors
    #password = getpass("Enter your password for MySQL: ")
    conn = mysql.connector.connect(user="root", password="NikoMySQL_13",
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
    cursor.execute("SELECT e.employeeID as EmployeeID, CONCAT_WS(" ", e.firstName, e.middleName, e.lastName) as Name, e.jobTitle as JobTitle,"
                   "l.username as Username FROM Employee e LEFT JOIN Login l ON e.employeeID = l.employeeID")
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
        cursor.execute(insert_query_login, (new_username, new_password, last_employee_id))
        return jsonify({"message": f"New employee data is added successfully for {last_employee_id} - {new_first} {new_last}"}), 201
    except Exception as e:
        return jsonify({"message": f"Failed to create a new user for {new_first} {new_last}", "error": str(e)}), 500


@app.route("/login/update_username/<string:curr_user>", method=['PUT'])
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


@app.route("/login/update_password/<string:curr_user>", method=['PUT'])
def update_password(curr_user):
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
            {"message": f"Failed to change the password to {new_password}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/employee/update_title/<string:curr_user>", method=['PUT'])
def update_title(curr_user):
    cursor = conn.cursor()
    data = request.json
    new_title = data.get("new_title")
    if new_title is None:
        return jsonify({'message': 'New job title is a required field!'}), 400
    try:
        cursor.execute("SELECT employeeID FROM Login WHERE username=%s", curr_user)
        title_employee_id = cursor.fetchone()[0]
        cursor.execute("UPDATE Employee SET jobTitle = %s WHERE employeeID = %s",
                   (new_title, title_employee_id))
    except Exception as e:
        return jsonify(
            {"message": f"Failed to change the job title to {new_title}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route('/employee/delete_employee/<string:username>', method=['DELETE'])
def delete_user(username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT employeeID from Login WHERE username=%s", username)
        id_res = cursor.fetchone()
        delete_id = id_res[0]
        cursor.execute("DELETE FROM Login WHERE username=%s", username)
        cursor.execute("DELETE FROM Employee WHERE employeeID=%s", delete_id)
        conn.commit()
        return jsonify({"message": 'User deleted successfully!'})
    except Exception as err:
        return jsonify({"message": f"Failed to delete user {username}", "error": str(err)}), 500
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
        cursor.execute("SELECT i.itemName, SUM(o.itemQuantity) AS totalCountOrdered"
                       "FROM Item i INNER JOIN ItemsOrdered o "
                       "ON i.itemID = o.itemID "
                       "GROUP BY itemName")
        data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


@app.route('/item/create_item', methods=['POST'])
def insert_item():
    data = request.json
    itemName = data[0]
    itemWeight = data[1]
    itemPrice = data[2]

    if itemName is None or itemWeight is None or itemPrice is None:
        return jsonify({'message': 'To insert a new item, you must provide the itemID, itemWeight, and itemPrice'}), 400

    try:
        cursor = conn.cursor()

        insert_query = "Insert into Item (itemName, itemWeight, itemPrice) values (%s, %s, %s)"
        cursor.execute(insert_query, (itemName, itemWeight, itemPrice))
        conn.commit()
        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route('/warehouse/add_items', methods=['POST'])
def insert_items_in_warehouse():
    data = request.json
    warehouseID = data[0]
    itemID = data[1]
    arrivalTime = data[2]
    itemStatus = data[3]
    itemLocation = data[4]
    itemQuantity = data[5]

    if warehouseID is None or itemID is None or arrivalTime is None or itemStatus is None\
            or itemLocation is None or itemQuantity is None:
        return jsonify({'message': 'To insert an item in a warehouse, you must provide the itemID, the arrival time, '
                                   'the item status, the location in the warehouse, and the total quantity to place'
                                   'in the warehouse.'}), 400

    try:
        cursor = conn.cursor()

        # The following few lines checks to see if the itemID exists in the Item table
        cursor.execute("SELECT * FROM Item WHERE itemID = %s", (itemID,))
        item = cursor.fetchone()
        if item is None:
            return jsonify({'message': f'Item with ID {itemID} does not exist in the Item table.'}), 404

        insert_query = ("Insert into ItemInWarehouse (warehouseID, itemID, arrivalTime, itemStatus, itemLocation, "
                        "itemQuantity) values (%s, %s, %s, %s, %s, %s)")
        cursor.execute(insert_query, (warehouseID, itemID, arrivalTime, itemStatus, itemLocation, itemQuantity))
        conn.commit()
        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route("/item/get_items_by_warehouse", methods=['GET'])
def get_items_by_warehouse():
    data = request.json
    warehouseID = data[0]

    if warehouseID is None:
        return jsonify({'message': 'Must enter warehouse ID to search by warehouse.'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT w.warehouseID, i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity "
                   "FROM Item i INNER JOIN ItemInWarehouse w ON i.itemID = w.itemID "
                   "WHERE warehouseID = %s", (warehouseID,))
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items in this warehouse."})
    else:
        # The following command will get all ordered items and display the total amount of those items that are
        # on order status across all orders
        cursor.execute("SELECT i.itemName, w.warehouseID, SUM(o.itemQuantity) as totalCountOrdered "
                       "FROM Item i INNER JOIN ItemsOrdered o ON i.itemID = o.itemID "
                       "INNER JOIN ItemInWarehouse w ON w.itemID = o.itemID "
                       "WHERE warehouseID = %s "
                       "GROUP BY itemName", (warehouseID,))
        data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


@app.route("/item/get_items_by_name", methods=['GET'])
def get_items_by_name():
    data = request.json
    itemName = data[0]

    if itemName is None:
        return jsonify({'message': 'Must enter item name to search by item.'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity, w.warehouseID "
                   "FROM Item i INNER JOIN ItemInWarehouse w ON i.itemID = w.itemID "
                   "WHERE itemName = %s", (itemName,))
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items by this name."})
    else:
        # The following command will get all ordered items and display the total amount of those items that are
        # on order status across all orders
        cursor.execute("SELECT i.itemName, SUM(o.itemQuantity) AS totalCountOrdered"
                       "FROM Item i INNER JOIN ItemsOrdered o "
                       "ON i.itemID = o.itemID "
                       "WHERE itemName = %s "
                       "GROUP BY itemName", (itemName,))
        data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)

# URL Template: "/<table_name>/<function>/<item_or_order_number> (if needed)
