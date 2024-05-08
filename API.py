from datetime import date

import mysql.connector
from mysql.connector import errorcode
from flask import Flask, jsonify, request
from getpass import getpass


try:  # Surrounding the connection in a try-except block to catch all connection errors
    # password = getpass("Enter your password for MySQL: ")
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
    cursor.execute("""SELECT e.employeeID as EmployeeID, CONCAT_WS(" ", e.firstName, e.middleName, e.lastName) as Name, 
                    e.jobTitle as JobTitle, l.username as Username FROM Employee e LEFT JOIN Login l ON e.employeeID = l.employeeID""")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return jsonify({'message': "There are no information on employees. Please make sure the data is added."})
    else:
        return jsonify(data), 200


@app.route("/login/check_login", methods=['GET'])
def check_login():
    cursor = conn.cursor()
    data = request.json
    input_username = data.get("username")
    input_password = data.get("password")
    if input_username == "" or input_password == "":
        return jsonify({'message': 'Please check that both username and password are inputted!', 'response': False}), 400
    try:
        cursor.execute("""SELECT IF(EXISTS(SELECT * FROM LOGIN WHERE username=%s and hashedPassword=%s), 1, 0)""",
                       (input_username, input_password))
        check_res = cursor.fetchone()[0]
        if check_res:
            return jsonify({"response": True})
        else:
            return jsonify({"response": False})
    except Exception as e:
        return jsonify({"message": f"Unable to check inputted username and password", "error": str(e), 'response': False}), 500


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
    if new_first == "":
        return jsonify({'message': 'First Name is a required field!'}), 400
    elif new_last == "":
        return jsonify({'message': 'Last Name is a required field!'}), 400
    elif new_username == "" or new_password == "":
        return jsonify({'message': 'Missing Username or Password; Both are required before proceeding'}), 400
    try:

        insert_query_employee = "INSERT INTO Employee (firstName, middleName, lastName, jobTitle) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query_employee, (new_first, new_middle, new_last, job_title))
        cursor.execute("SELECT employeeID FROM Employee ORDER BY employeeID DESC LIMIT 1")
        last_employee_id = cursor.fetchone()[0]
        insert_query_login = "INSERT INTO Login (username, hashedPassword, employeeId) VALUES (%s, %s, %s)"
        cursor.execute(insert_query_login, (new_username, new_password, last_employee_id))
        conn.commit()
        return jsonify({"message": f"New employee data is added successfully for {last_employee_id} - {new_first} {new_last}"}), 201
    except Exception as e:
        return jsonify({"message": f"Failed to create a new user for {new_first} {new_last}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/login/update_username/<string:curr_user>", methods=['PUT'])
def update_username(curr_user):
    cursor = conn.cursor()
    data = request.json
    new_username = data.get('new_username')
    if new_username == "":
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


@app.route("/login/update_password/<string:curr_user>", methods=['PUT'])
def update_password(curr_user):
    cursor = conn.cursor()
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if old_password == "":
        return jsonify({'message': 'Old password is a required field!'}), 400
    elif new_password == "":
        return jsonify({'message': 'New password is a required field!'}), 400
    try:
        cursor.execute("UPDATE Login SET hashedPassword = %s WHERE username = %s and hashedPassword = %s",
                       (new_password, curr_user, old_password))
        conn.commit()
        return jsonify({"message": f"Password is changed successfully to {new_password}"}), 201
    except Exception as e:
        return jsonify(
            {"message": f"Failed to change the password to {new_password}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/employee/update_title/<string:curr_user>", methods=['PUT'])
def update_title(curr_user):
    cursor = conn.cursor()
    data = request.json
    new_title = data.get("new_title")
    if new_title == "":
        return jsonify({'message': 'New job title is a required field!'}), 400
    try:
        cursor.execute("SELECT employeeID FROM Login WHERE username=%s", (curr_user,))
        title_employee_id = cursor.fetchone()[0]
        cursor.execute("UPDATE Employee SET jobTitle = %s WHERE employeeID = %s", (new_title, title_employee_id))
        return jsonify({"message": f"Job title for {curr_user} is changed successfully to {new_title}"}), 201
    except Exception as e:
        return jsonify(
            {"message": f"Failed to change the job title to {new_title}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route('/employee/delete_employee/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT employeeID from Login WHERE username=%s", (username,))
        id_res = cursor.fetchone()
        delete_id = id_res[0]
        cursor.execute("DELETE FROM Login WHERE username=%s", (username,))
        cursor.execute("DELETE FROM Employee WHERE employeeID=%s", (delete_id,))
        conn.commit()
        return jsonify({"message": 'User deleted successfully!'})
    except Exception as e:
        return jsonify({"message": f"Failed to delete user {username}", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route("/item/get_items", methods=['GET'])
def get_items():
    cursor = conn.cursor()
    cursor.execute("""SELECT i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity, w.warehouseID, w.itemLocation
                   FROM Item i LEFT JOIN ItemInWarehouse w ON i.itemID = w.itemID""")
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items in the system."})
    else:
        cursor.close()
        return jsonify(data), 200


@app.route("/item/get_items_by_warehouse", methods=['GET'])
def get_items_by_warehouse():
    data = request.json
    warehouseID = data.get("warehouseID")

    if warehouseID == "":
        return jsonify({'message': 'Must enter warehouse ID to search by warehouse.'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity, w.warehouseID, w.itemLocation "
                   "FROM Item i INNER JOIN ItemInWarehouse w ON i.itemID = w.itemID "
                   "WHERE warehouseID = %s"
                   "ORDER BY i.itemID", (warehouseID,))
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items in this warehouse."})
    else:
        cursor.close()
        return jsonify(data), 200


@app.route("/item/get_items_by_name", methods=['GET'])
def get_items_by_name():
    data = request.json
    itemName = data.get("itemName")

    if itemName == "":
        return jsonify({'message': 'Must enter item name to search by item.'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT i.itemID, i.itemName, i.itemWeight, i.itemPrice, w.itemQuantity, w.warehouseID, w.itemLocation "
                   "FROM Item i INNER JOIN ItemInWarehouse w ON i.itemID = w.itemID "
                   "WHERE itemName = %s", (itemName,))
    data = cursor.fetchall()
    if len(data) == 0:
        return jsonify({'message': "There are no items by this name."})
    else:
        cursor.close()
        return jsonify(data), 200


@app.route('/item/create_item', methods=['POST'])
def insert_item():
    data = request.json
    itemName = data.get("itemName")
    itemWeight = data.get("itemWeight")
    itemPrice = data.get("itemPrice")

    if itemName == "" or itemWeight == "" or itemPrice == "":
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

@app.route('/warehouse/add_items', methods=['POST'])
def insert_items_in_warehouse():
    data = request.json
    warehouseID = data.get("warehouseID")
    itemID = data.get("itemID")
    arrivalTime = date.today()
    itemLocation = data.get("itemLocation")
    itemQuantity = data.get("itemQuantity")

    if warehouseID == "" or itemID == "" or arrivalTime == "" or itemLocation == "" or itemQuantity == "":
        return jsonify({'message': 'One of the required fields is missing'}), 400

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT itemQuantity FROM ItemInWarehouse WHERE warehouseID = %s AND itemID = %s",
                       (warehouseID, itemID))
        existing_quantity = cursor.fetchone()

        if existing_quantity:
            # If the item exists, add the entered number to total ItemQuantity
            new_quantity = int(existing_quantity[0]) + int(itemQuantity)
            update_query = "UPDATE ItemInWarehouse SET itemQuantity = %s WHERE warehouseID = %s AND itemID = %s"
            cursor.execute(update_query, (new_quantity, warehouseID, itemID))
        else:
            cursor.execute("SELECT * FROM Item WHERE itemID = %s", (itemID,))
            item = cursor.fetchone()
            if item == "":
                return jsonify({'message': f'Item with ID {itemID} does not exist in the Item table.'}), 404

            insert_query = ("Insert into ItemInWarehouse (warehouseID, itemID, arrivalTime, itemLocation, "
                            "itemQuantity) values (%s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (warehouseID, itemID, arrivalTime, itemLocation, itemQuantity))
        conn.commit()
        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route('/warehouse/update_warehouse', methods=['PUT'])
def update_warehouse():
    data = request.json
    warehouseID = data.get("warehouseID")
    warehouseAddressID = data.get("warehouseAddressID")
    capacity = data.get("capacity")
    addressNum = data.get("addressNum")
    street = data.get("street")
    city = data.get("city")
    zipCode = data.get("zipCode")

    if warehouseID == "" or warehouseAddressID == "" or capacity == "" or addressNum == ""\
            or capacity == "" or street == "" or city == "" or zipCode == "":
        return jsonify({'message': 'One of the required fields is missing'}), 400

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Addresses WHERE addressID = %s", (warehouseAddressID,))
        address_exists = cursor.fetchone()
        if not address_exists:
            return jsonify({'message': 'Warehouse address with the provided ID does not exist.'}), 404

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
        #cursor.execute("SELECT * FROM ItemsOrdered ORDER BY orderID")
        #data += cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


@app.route("/orders/get_items_in_orders", methods=['GET'])
def get_items_in_orders():
    data = request.json
    orderID = data.get("orderID")
    if orderID == "":
        return jsonify({'message': 'orderID is a required field'}), 400
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT i.itemName, o.itemID, o.itemQuantity FROM Item i INNER JOIN ItemsOrdered o ON i.itemID = o.itemID WHERE orderID = %s", (orderID,))
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data), 200


@app.route("/orders/create_order", methods=['POST'])
def create_order():
    data = request.json
    orderStatus = data.get("orderStatus")
    departureTime = data.get("departureTime")
    deliveryAddressID = data.get("deliveryAddressID")
    handlerID = data.get("handlerID")

    try:
        cursor = conn.cursor()

        insert_query = ("Insert into Orders (orderStatus, departureTime, deliveryAddressID, handlerID) "
                        "values (%s, %s, %s, %s)")
        cursor.execute(insert_query, (orderStatus, departureTime, deliveryAddressID, handlerID))
        conn.commit()
        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route("/orders/add_item_to_order", methods=['POST'])
def add_item_to_order():
    data = request.json
    orderID = data.get("orderID")
    itemID = data.get("itemID")
    warehouseID = data.get("warehouseID")
    itemQuantity = data.get("itemQuantity")

    if orderID == "" or itemID == "" or warehouseID == "" or itemQuantity == "":
        return jsonify({'message': 'Missing a field.'}), 400

    try:
        cursor = conn.cursor()

        # Check if the entered itemQuantity does not exceed the available quantity in the warehouse
        cursor.execute("SELECT itemQuantity FROM ItemInWarehouse WHERE warehouseID = %s AND itemID = %s",
                       (warehouseID, itemID))
        warehouse_quantity = cursor.fetchone()
        if warehouse_quantity is None:
            return jsonify({'message': 'Item not found in the warehouse.'}), 404

        warehouse_quantity = int(warehouse_quantity[0])
        if int(itemQuantity) > warehouse_quantity:
            return jsonify({'message': 'Entered item quantity exceeds available quantity in the warehouse.'}), 400

        # Update the quantity in the warehouse by subtracting the entered itemQuantity
        new_warehouse_quantity = warehouse_quantity - int(itemQuantity)
        update_query = "UPDATE ItemInWarehouse SET itemQuantity = %s WHERE warehouseID = %s AND itemID = %s"
        cursor.execute(update_query, (new_warehouse_quantity, warehouseID, itemID))

        cursor.execute("SELECT itemQuantity FROM ItemsOrdered WHERE orderID = %s AND itemID = %s",
                       (orderID, itemID))
        existing_quantity = cursor.fetchone()

        if existing_quantity:
            # If the item exists, add the entered number to total ItemQuantity
            new_quantity = int(existing_quantity[0]) + int(itemQuantity)
            update_query = "UPDATE ItemsOrdered SET itemQuantity = %s WHERE orderID = %s AND itemID = %s"
            cursor.execute(update_query, (new_quantity, orderID, itemID))
        else:
            # If the item does not exist, insert a new row
            insert_query = "INSERT INTO ItemsOrdered (orderID, itemID, itemQuantity) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (orderID, itemID, itemQuantity))
        conn.commit()
        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
    finally:
        cursor.close()


@app.route('/orders/delete_order', methods=['DELETE'])
def delete_order():
    data = request.json
    orderID = data.get("orderID")

    if orderID == "":
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


@app.route('/orders/delete_item_from_order', methods=['DELETE'])
def delete_item_from_order():
    data = request.json
    orderID = data.get("orderID")
    warehouseID = data.get("warehouseID")
    itemID = data.get("itemID")

    if orderID == "" or itemID == "" or warehouseID == "":
        return jsonify({'message': 'Missing a field.'}), 400

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT itemQuantity FROM ItemInWarehouse WHERE warehouseID = %s AND itemID = %s",
                       (warehouseID, itemID))
        existing_quantity = cursor.fetchone()
        if existing_quantity is None:
            return jsonify({'message': 'Item not found in specified warehouse.'}), 404

        # Retrieve the quantity of the deleted item from the order
        cursor.execute("SELECT itemQuantity FROM ItemsOrdered WHERE orderID = %s AND itemID = %s", (orderID, itemID))
        deleted_item_quantity = cursor.fetchone()

        if deleted_item_quantity:
            deleted_item_quantity = int(deleted_item_quantity[0])
            update_query = "UPDATE ItemInWarehouse SET itemQuantity = itemQuantity + %s WHERE warehouseID = %s AND itemID = %s"
            cursor.execute(update_query, (deleted_item_quantity, warehouseID, itemID))

        delete_query = "DELETE from ItemsOrdered Where itemID = %s"
        cursor.execute(delete_query, (itemID,))
        conn.commit()
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete data', 'error': str(e)}), 500
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)

# URL Template: "/<table_name>/<function>/<item_or_order_number> (if needed)
