import json
import tkinter.ttk
from tkinter import *
from tkinter import scrolledtext, ttk
import requests

import sv_ttk

root = Tk()
root.geometry("900x750")
root.resizable(False, True)

loginFrame = Frame(root)
mainFrame = Frame(root)
ordersFrame = Frame(root)
warehousesFrame = Frame(root)
itemsFrame = Frame(root)
employeesFrame = Frame(root)
updateEmpFrame = Frame(root)
createEmpFrame = Frame(root)
updateWareFrame = Frame(root)
orderItemsFrame = Frame(root)
createItemsFrame = Frame(root)
addItemsFrame = Frame(root)
createOrderFrame = Frame(root)
addressFrame = Frame(root)
addAddressFrame = Frame(root)

sv_ttk.set_theme("dark")
title = ("Arial", 25)
text = ("Arial", 12)
entry = ("Arial", 15)
s = ttk.Style()
s.configure('my.TButton', font=('Arial', 25))

root.grid_columnconfigure(0, weight=1)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def login():
    def test_login():
        user = user_enter.get()
        pas = pass_enter.get()
        request = (requests.get("http://127.0.0.1:105/login/check_login",
                        json={"username": user,
                              "password": pas})).json()
        if request != {} and request["response"]:
            main()
            loginFrame.grid_forget()
            mainFrame.grid()
            clear_frame(loginFrame)
        else:
            login_button.configure(text="Wrong")
            login_button.after(1000, lambda: login_button.configure(text="Enter"))

    label = ttk.Label(loginFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 150))

    login_label = ttk.Label(loginFrame, text="Username", font=text)
    login_label.grid(row=1, column=0)

    user_enter = ttk.Entry(loginFrame, font=("Arial", 30))
    user_enter.grid(row=2, column=0, pady=(0, 100))

    pass_label = ttk.Label(loginFrame, text="Password", font=text)
    pass_label.grid(row=3, column=0)

    pass_enter = ttk.Entry(loginFrame, show="*", font=("Arial", 30))
    pass_enter.grid(row=4, column=0)

    login_button = ttk.Button(loginFrame, text="Enter", command=test_login,
                             style='my.TButton')
    login_button.grid(row=5, column=0, pady=(150, 0))
def main():
    items_button = ttk.Button(mainFrame, text="Items",
                          command=lambda: [itemsFrame.grid(),
                                           mainFrame.grid_forget(),
                                           item()],
                          style='my.TButton')
    items_button.grid(row=0, column=0, pady=(55, 0))

    warehouses_button = ttk.Button(mainFrame, text="Warehouses",
                               command=lambda: [warehousesFrame.grid(),
                                                mainFrame.grid_forget(),
                                                warehouse()],
                               style='my.TButton')
    warehouses_button.grid(row=1, column=0, pady=(55, 0))

    orders_button = ttk.Button(mainFrame, text="Orders",
                           command=lambda: [ordersFrame.grid(),
                                            mainFrame.grid_forget(),
                                            orders()],
                           style='my.TButton')
    orders_button.grid(row=2, column=0, pady=(55, 0))

    employees_button = ttk.Button(mainFrame, text="Employees",
                              command=lambda: [employeesFrame.grid(),
                                               mainFrame.grid_forget(),
                                               employee()],
                              style='my.TButton')
    employees_button.grid(row=3, column=0, pady=(55, 0))

    address_button = ttk.Button(mainFrame, text="Addresses",
                              command=lambda: [addressFrame.grid(),
                                               mainFrame.grid_forget(),
                                               address({'message':""})],
                              style='my.TButton')
    address_button.grid(row=4, column=0, pady=(55, 0))

    log_out_button = ttk.Button(mainFrame, text="Log Out",
                           command=lambda: [loginFrame.grid(),
                                            mainFrame.grid_forget(),
                                            login()],
                           style='my.TButton')
    log_out_button.grid(row=5, column=0, pady=(55, 0))

def address(temp):
    def delete_add():
        response = requests.delete("http://127.0.0.1:105/addresses/delete_address", json={"addressID": user_enter.get()})
        response = json.loads(response.text)
        clear_frame(addressFrame)
        address(response)

    label = Label(addressFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 25))

    box = ttk.Treeview(addressFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(addressFrame, orient="vertical", command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4", "5")
    box['show'] = 'headings'

    box.column("1", width=100)
    box.column("2", width=100)
    box.column("3", width=200)
    box.column("4", width=125)
    box.column("5", width=100)


    box.heading("1", text="Address ID")
    box.heading("2", text="Address Num")
    box.heading("3", text="Street")
    box.heading("4", text="City")
    box.heading("5", text="Zipcode")

    response = requests.get("http://127.0.0.1:105/addresses/get_addresses")
    for i in response.json():
        box.insert("", "end", values=i)


    label = Label(addressFrame, text="Address ID", font=text)
    label.grid(row=2, column=0, pady=(30, 0))

    user_enter = Entry(addressFrame, font=entry)
    user_enter.grid(row=3, column=0, pady=(0, 30))

    temp = temp["message"]

    label_response = Label(addressFrame, text=f"{temp}", font=text)
    label_response.grid(row=4, column=0, pady=(0, 0))

    back_button = ttk.Button(addressFrame, text="Delete",
                         command=lambda: [delete_add()],
                         style='my.TButton')
    back_button.grid(row=5, column=0, pady=(0, 50))

    back_button = ttk.Button(addressFrame, text="Create",
                         command=lambda: [addAddressFrame.grid(),
                                          addressFrame.grid_forget(),
                                          clear_frame(addressFrame),
                                          add_address()],
                         style='my.TButton')
    back_button.grid(row=6, column=0, pady=(0, 50))

    back_button = ttk.Button(addressFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          addressFrame.grid_forget(),
                                          clear_frame(addressFrame)],
                         style='my.TButton')
    back_button.grid(row=7, column=0, pady=(0, 50))

def add_address():
    def create_add():
        response = requests.post("http://127.0.0.1:105/addresses/create_address",
                                   json={"addressNum": add_num_enter.get(),
                                         "street": street_enter.get(),
                                         "city": street_enter.get(),
                                         "zipCode": zip_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])


    label = Label(addAddressFrame, text="Address Num", font=text)
    label.grid(row=3, column=0, pady=(150, 0))
    add_num_enter = Entry(addAddressFrame, font=entry)
    add_num_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(addAddressFrame, text="Street", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    street_enter = Entry(addAddressFrame, font=entry)
    street_enter.grid(row=6, column=0, pady=(0, 25))

    label = Label(addAddressFrame, text="City", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    city_entry = Entry(addAddressFrame, font=entry)
    city_entry.grid(row=8, column=0, pady=(0, 25))

    label = Label(addAddressFrame, text="Zipcode", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    zip_enter = Entry(addAddressFrame, font=entry)
    zip_enter.grid(row=10, column=0, pady=(0, 25))

    label_response = Label(addAddressFrame, text="", font=text)
    label_response.grid(row=15, column=0, pady=(10, 10))

    back_button = ttk.Button(addAddressFrame, text="Create",
                         command=lambda: [create_add()],
                         style='my.TButton')
    back_button.grid(row=19, column=0, pady=(0, 50))

    back_button = ttk.Button(addAddressFrame, text="Back",
                         command=lambda: [addressFrame.grid(),
                                          addAddressFrame.grid_forget(),
                                          clear_frame(addAddressFrame),
                                          address({'message':""})],
                         style='my.TButton')
    back_button.grid(row=20, column=0, pady=(0, 50))
def orders():
    def del_order():
        requests.delete("http://127.0.0.1:105/orders/delete_order", json={"orderID": user_enter.get()})
        clear_frame(ordersFrame)
        orders()

    label = Label(ordersFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 50))

    box = ttk.Treeview(ordersFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(ordersFrame, orient="vertical", command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4", "5")
    box['show'] = 'headings'

    box.column("1", width=100)
    box.column("2", width=100)
    box.column("3", width=300)
    box.column("4", width=125)
    box.column("5", width=100)

    box.heading("1", text="Order ID")
    box.heading("2", text="Status")
    box.heading("3", text="Departure Time")
    box.heading("4", text="Delivery Address ID")
    box.heading("5", text="Handler ID")

    response = requests.get("http://127.0.0.1:105/orders/get_orders")
    for i in response.json():
        box.insert("", "end", values=i)

    label = Label(ordersFrame, text="Order ID", font=text)
    label.grid(row=2, column=0, pady=(10, 0))

    user_enter = Entry(ordersFrame, font=entry)
    user_enter.grid(row=3, column=0, pady=(0, 25))

    search_button = ttk.Button(ordersFrame, text="Inspect Order",
                               command=lambda: [orderItemsFrame.grid(),
                                                ordersFrame.grid_forget(),
                                                order_items(user_enter.get(),{'message':""}),
                                                clear_frame(ordersFrame)],
                               style='my.TButton')
    search_button.grid(row=4, column=0, pady=(0, 0))

    search_button = ttk.Button(ordersFrame, text="Create Order",
                               command=lambda: [createOrderFrame.grid(),
                                                ordersFrame.grid_forget(),
                                                create_order(),
                                                clear_frame(ordersFrame)],
                               style='my.TButton')
    search_button.grid(row=6, column=0, pady=(25, 0))

    delete_button = ttk.Button(ordersFrame, text="Delete Order",
                               command=lambda: [del_order()],
                               style='my.TButton')
    delete_button.grid(row=5, column=0, pady=(25, 0))

    back_button = ttk.Button(ordersFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          ordersFrame.grid_forget(),
                                          clear_frame(ordersFrame)],
                         style='my.TButton')
    back_button.grid(row=7, column=0, pady=(25, 0))

def create_order():
    def create():
        response = requests.post("http://127.0.0.1:105/orders/create_order",
                                json={"orderStatus": order_stat_enter.get(),
                                      "departureTime": dep_time_enter.get(),
                                      "deliveryAddressID": cap_entry.get(),
                                      "handlerID": hand_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(createOrderFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 50))

    label = Label(createOrderFrame, text="Order Status", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    order_stat_enter = Entry(createOrderFrame, font=entry)
    order_stat_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(createOrderFrame, text="Departure Time", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    dep_time_enter = Entry(createOrderFrame, font=entry)
    dep_time_enter.grid(row=6, column=0, pady=(0, 25))

    label = Label(createOrderFrame, text="Delivery Address ID", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    cap_entry = Entry(createOrderFrame, font=entry)
    cap_entry.grid(row=8, column=0, pady=(0, 25))

    label = Label(createOrderFrame, text="Handler ID", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    hand_enter = Entry(createOrderFrame, font=entry)
    hand_enter.grid(row=10, column=0, pady=(0, 25))


    create_button = ttk.Button(createOrderFrame, text="Create",
                         command=lambda: [create()],
                         style='my.TButton')
    create_button.grid(row=14, column=0, pady=(20, 0))

    label_response = Label(createOrderFrame, text="", font=text)
    label_response.grid(row=15, column=0, pady=(10, 10))

    back_button = ttk.Button(createOrderFrame, text="Back",
                         command=lambda: [ordersFrame.grid(),
                                          createOrderFrame.grid_forget(),
                                          orders(),
                                          clear_frame(createOrderFrame)],
                         style='my.TButton')
    back_button.grid(row=16, column=0, pady=(0, 0))

def order_items(temp,error):
    def update():
        response = requests.post("http://127.0.0.1:105/orders/add_item_to_order",
                                json={"orderID": temp,
                                      "itemID": item_enter.get(),
                                      "itemQuantity": qua_enter.get(),
                                      "warehouseID": ware_enter.get()})
        response = json.loads(response.text)
        clear_frame(ordersFrame)
        order_items(temp,response)
    def delete():
        response = requests.delete("http://127.0.0.1:105/orders/delete_item_from_order",
                                 json={"orderID": temp,
                                       "itemID": item_enter.get(),
                                       "warehouseID": ware_enter.get()})
        response = json.loads(response.text)
        clear_frame(ordersFrame)
        order_items(temp, response)

    label = Label(orderItemsFrame, text=f"Order {temp}", font=title)
    label.grid(row=0, column=0, pady=(0, 20))

    box = ttk.Treeview(orderItemsFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(orderItemsFrame, orient="vertical",
                          command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3")
    box['show'] = 'headings'

    box.column("1", width=200)
    box.column("2", width=200)
    box.column("3", width=200)

    box.heading("1", text="Item Name")
    box.heading("2", text="Item ID")
    box.heading("3", text="Item Quantity")


    response = requests.get("http://127.0.0.1:105/orders/get_items_in_orders", json={"orderID": temp})
    for i in response.json():
        box.insert("", "end", values=i)

    label = Label(orderItemsFrame, text="Enter Item ID", font=text)
    label.grid(row=2, column=0, pady=(15, 0))

    item_enter = Entry(orderItemsFrame, font=entry)
    item_enter.grid(row=3, column=0, pady=(0, 0))

    label = Label(orderItemsFrame, text="Enter Quantity", font=text)
    label.grid(row=4, column=0, pady=(15, 0))

    qua_enter = Entry(orderItemsFrame, font=entry)
    qua_enter.grid(row=5, column=0, pady=(0, 0))

    label = Label(orderItemsFrame, text="Enter Warehouse ID", font=text)
    label.grid(row=6, column=0, pady=(15, 0))

    ware_enter = Entry(orderItemsFrame, font=entry)
    ware_enter.grid(row=7, column=0, pady=(0, 0))

    add_button = ttk.Button(orderItemsFrame, text="Add",
                         command=lambda: [update()],
                         style='my.TButton')
    add_button.grid(row=13, column=0, pady=(20, 0))

    delete_button = ttk.Button(orderItemsFrame, text="Delete",
                         command=lambda: [delete()],
                         style='my.TButton')
    delete_button.grid(row=14, column=0, pady=(25, 0))

    error = error["message"]

    label_response = Label(orderItemsFrame, text=f"{error}", font=text)
    label_response.grid(row=15, column=0, pady=(5, 5))


    back_button = ttk.Button(orderItemsFrame, text="Back",
                         command=lambda: [ordersFrame.grid(),
                                          orderItemsFrame.grid_forget(),
                                          orders(),
                                          clear_frame(orderItemsFrame)],
                         style='my.TButton')
    back_button.grid(row=16, column=0, pady=(0, 0))


def warehouse():
    label = Label(warehousesFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    box = ttk.Treeview(warehousesFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(warehousesFrame, orient="vertical",
                          command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4", "5", "6", "7")
    box['show'] = 'headings'

    box.column("1", width=50)
    box.column("2", width=70)
    box.column("3", width=100)
    box.column("4", width=200)
    box.column("5", width=200)
    box.column("6", width=100)
    box.column("7", width=100)

    box.heading("1", text="ID")
    box.heading("2", text="capacity")
    box.heading("3", text="addressNum")
    box.heading("4", text="street")
    box.heading("5", text="city")
    box.heading("6", text="zipcode")
    box.heading("7", text="addressID")


    response = requests.get("http://127.0.0.1:105/warehouse/get_warehouses")
    for i in response.json():
        box.insert("", "end", values=i)


    label = Label(warehousesFrame, text="Warehouse ID", font=text)
    label.grid(row=2, column=0, pady=(25, 0))

    user_enter = Entry(warehousesFrame, font=entry)
    user_enter.grid(row=3, column=0, pady=(0, 25))

    update_ware_button = ttk.Button(warehousesFrame, text="Update Warehouse",
                               command=lambda: [updateWareFrame.grid(),
                                                warehousesFrame.grid_forget(),
                                                update_warehouse(user_enter.get()),
                                                clear_frame(warehousesFrame)],
                               style='my.TButton')
    update_ware_button.grid(row=4, column=0, pady=(0, 0))

    back_button = ttk.Button(warehousesFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          warehousesFrame.grid_forget(),
                                          clear_frame(warehousesFrame)],
                         style='my.TButton')
    back_button.grid(row=5, column=0, pady=(50, 0))

def update_warehouse(temp):
    def up_ware():
        response = requests.put("http://127.0.0.1:105/warehouse/update_warehouse",
                                 json={"warehouseID": temp,
                                       "warehouseAddressID": add_id_enter.get(),
                                       "capacity": capacity_enter.get(),
                                       "addressNum": add_num_enter.get(),
                                       "street": street_enter.get(),
                                       "city": city_enter.get(),
                                       "zipCode": zip_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(updateWareFrame, text=f"Warehouse ({temp})", font=title)
    label.grid(row=0, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="Warehouse Address ID", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    add_id_enter = Entry(updateWareFrame, font=entry)
    add_id_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="Capacity", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    capacity_enter = Entry(updateWareFrame, font=entry)
    capacity_enter.grid(row=6, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="Address Number", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    add_num_enter = Entry(updateWareFrame, font=entry)
    add_num_enter.grid(row=8, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="Street", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    street_enter = Entry(updateWareFrame, font=entry)
    street_enter.grid(row=10, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="City", font=text)
    label.grid(row=11, column=0, pady=(0, 0))
    city_enter = Entry(updateWareFrame, font=entry)
    city_enter.grid(row=12, column=0, pady=(0, 25))

    label = Label(updateWareFrame, text="Zip Code", font=text)
    label.grid(row=13, column=0, pady=(0, 0))
    zip_enter = Entry(updateWareFrame, font=entry)
    zip_enter.grid(row=14, column=0, pady=(0, 25))

    ware_update = ttk.Button(updateWareFrame, text="Update Warehouse",
                             command=lambda: [up_ware()],
                             style='my.TButton')
    ware_update.grid(row=15, column=0, pady=(0, 0))

    label_response = Label(updateWareFrame, text="", font=text)
    label_response.grid(row=16, column=0, pady=(10, 10))

    back_button = ttk.Button(updateWareFrame, text="Back",
                         command=lambda: [warehousesFrame.grid(),
                                          updateWareFrame.grid_forget(),
                                          warehouse(),
                                          clear_frame(updateWareFrame)],
                         style='my.TButton')
    back_button.grid(row=17, column=0, pady=(0, 0))

def item():
    def search():
        for x in box.get_children():
            box.delete(x)
        if search_enter.get().isnumeric():
            response = requests.get(f"http://127.0.0.1:105/item/get_items_by_warehouse",
                                    json={"warehouseID": search_enter.get()})
            for i in response.json():
                box.insert("", "end", values=i)
        else:

            response = requests.get(f"http://127.0.0.1:105/item/get_items_by_name",
                                    json={"itemName": search_enter.get()})
            for i in response.json():
                box.insert("", "end", values=i)

    label = Label(itemsFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 25))

    box = ttk.Treeview(itemsFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(itemsFrame, orient="vertical", command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4", "5", "6", "7")
    box['show'] = 'headings'

    box.column("1", width=50)
    box.column("2", width=200)
    box.column("3", width=100)
    box.column("4", width=70)
    box.column("5", width=70)
    box.column("6", width=100)
    box.column("7", width=100)


    box.heading("1", text="ID")
    box.heading("2", text="Name")
    box.heading("3", text="Weight")
    box.heading("4", text="Price")
    box.heading("5", text="Quantity")
    box.heading("6", text="WarehouseID")
    box.heading("7", text="ItemLocation")


    response = requests.get("http://127.0.0.1:105/item/get_items")
    for i in response.json():
        box.insert("", "end", values=i)

    create_button = ttk.Button(itemsFrame, text="Add Item to Warehouse",
                         command=lambda: [addItemsFrame.grid(),
                                          itemsFrame.grid_forget(),
                                          clear_frame(itemsFrame),
                                          add_item()],
                         style='my.TButton')
    create_button.grid(row=7, column=0, pady=(25, 0))

    search_button = ttk.Button(itemsFrame, text="Search",
                         command=lambda: [search()],
                         style='my.TButton')
    search_button.grid(row=4, column=0, pady=(25, 0))

    label = Label(itemsFrame, text="Item Name or WarehouseID", font=text)
    label.grid(row=2, column=0, pady=(25, 0))

    search_enter = Entry(itemsFrame, font=entry)
    search_enter.grid(row=3, column=0, pady=(0, 0))

    create_button = ttk.Button(itemsFrame, text="Create Item",
                         command=lambda: [createItemsFrame.grid(),
                                          itemsFrame.grid_forget(),
                                          clear_frame(itemsFrame),
                                          create_item()],
                         style='my.TButton')
    create_button.grid(row=6, column=0, pady=(25, 0))

    back_button = ttk.Button(itemsFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          itemsFrame.grid_forget(),
                                          clear_frame(itemsFrame)],
                         style='my.TButton')
    back_button.grid(row=8, column=0, pady=(25, 0))

def add_item():
    def add():
        response = requests.post("http://127.0.0.1:105/warehouse/add_items",
                                 json={"warehouseID": warehouse_id_enter.get(),
                                       "itemID": item_id_enter.get(),
                                       "itemLocation": item_loc_enter.get(),
                                       "itemQuantity": item_quantity_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])


    label = Label(addItemsFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    label = Label(addItemsFrame, text="Warehouse ID", font=text)
    label.grid(row=1, column=0, pady=(0, 0))
    warehouse_id_enter = Entry(addItemsFrame, font=entry)
    warehouse_id_enter.grid(row=2, column=0, pady=(0, 25))

    label = Label(addItemsFrame, text="Item ID", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    item_id_enter = Entry(addItemsFrame, font=entry)
    item_id_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(addItemsFrame, text="Item Location", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    item_loc_enter = Entry(addItemsFrame, font=entry)
    item_loc_enter.grid(row=8, column=0, pady=(0, 25))

    label = Label(addItemsFrame, text="Item Quantity", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    item_quantity_enter = Entry(addItemsFrame, font=entry)
    item_quantity_enter.grid(row=10, column=0, pady=(0, 25))

    label_response = Label(addItemsFrame, text="", font=text)
    label_response.grid(row=11, column=0, pady=(25, 25))

    create_button = ttk.Button(addItemsFrame, text="Add",
                         command=lambda: [add()],
                         style='my.TButton')
    create_button.grid(row=12, column=0, pady=(0, 0))

    back_button = ttk.Button(addItemsFrame, text="Back",
                         command=lambda: [itemsFrame.grid(),
                                          addItemsFrame.grid_forget(),
                                          clear_frame(addItemsFrame),
                                          item()],
                         style='my.TButton')
    back_button.grid(row=13, column=0, pady=(50, 0))
def create_item():
    def create():
        response = requests.post("http://127.0.0.1:105/item/create_item",
                                 json={"itemName": item_name_enter.get(),
                                       "itemWeight": item_weight_enter.get(),
                                       "itemPrice": item_price_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(createItemsFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    label = Label(createItemsFrame, text="Item Name", font=text)
    label.grid(row=1, column=0, pady=(0, 0))
    item_name_enter = Entry(createItemsFrame, font=entry)
    item_name_enter.grid(row=2, column=0, pady=(0, 25))

    label = Label(createItemsFrame, text="Item Weight", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    item_weight_enter = Entry(createItemsFrame, font=entry)
    item_weight_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(createItemsFrame, text="Item Price", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    item_price_enter = Entry(createItemsFrame, font=entry)
    item_price_enter.grid(row=6, column=0, pady=(0, 25))

    label_response = Label(createItemsFrame, text="", font=text)
    label_response.grid(row=7, column=0, pady=(25, 25))

    create_button = ttk.Button(createItemsFrame, text="Create",
                         command=lambda: [create()],
                         style='my.TButton')
    create_button.grid(row=8, column=0, pady=(50, 0))

    back_button = ttk.Button(createItemsFrame, text="Back",
                         command=lambda: [itemsFrame.grid(),
                                          createItemsFrame.grid_forget(),
                                          clear_frame(createItemsFrame),
                                          item()],
                         style='my.TButton')
    back_button.grid(row=9, column=0, pady=(50, 0))

def employee():
    def del_emp():
        requests.delete(f"http://127.0.0.1:105/employee/delete_employee/{user_enter.get()}")
        clear_frame(employeesFrame)
        employee()

    label = Label(employeesFrame, text="", font=title)
    label.grid(row=0, column=0, pady=(0, 25))

    box = ttk.Treeview(employeesFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = ttk.Scrollbar(employeesFrame, orient="vertical",
                           command=box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4")
    box['show'] = 'headings'

    box.column("1", width=50)
    box.column("2", width=300)
    box.column("3", width=150)
    box.column("4", width=150)

    box.heading("1", text="ID")
    box.heading("2", text="Name")
    box.heading("3", text="Job")
    box.heading("4", text="UserName")

    response = requests.get(f"http://127.0.0.1:105/employee/get_all")
    for i in response.json():
        box.insert("", "end", values=i)

    label = Label(employeesFrame, text="Username", font=text)
    label.grid(row=2, column=0, pady=(25, 0))

    user_enter = Entry(employeesFrame, font=entry)
    user_enter.grid(row=3, column=0, pady=(0, 25))

    update_emp_button = ttk.Button(employeesFrame, text="Update Employee",
                               command=lambda: [updateEmpFrame.grid(),
                                                employeesFrame.grid_forget(),
                                                update_employee(user_enter.get()),
                                                clear_frame(employeesFrame)],
                               style='my.TButton')
    update_emp_button.grid(row=4, column=0, pady=(0, 0))

    del_button = ttk.Button(employeesFrame, text="Delete Employee",
                        command=lambda: [del_emp()],
                        style='my.TButton')
    del_button.grid(row=5, column=0, pady=(25, 0))

    cre_button = ttk.Button(employeesFrame, text="Create Employee",
                        command=lambda: [createEmpFrame.grid(),
                                         employeesFrame.grid_forget(),
                                         create_employee(),
                                         clear_frame(employeesFrame)],
                        style='my.TButton')
    cre_button.grid(row=6, column=0, pady=(25, 0))

    back_button = ttk.Button(employeesFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          employeesFrame.grid_forget(),
                                          clear_frame(employeesFrame)],
                         style='my.TButton')
    back_button.grid(row=7, column=0, pady=(25, 0))


def create_employee():
    def create_user():
        response = requests.post(f"http://127.0.0.1:105/employee/create_user",
                                json={"firstName": first_enter.get(),
                                      "middleName": mid_enter.get(),
                                      "lastName": last_enter.get(),
                                      "jobTitle": job_enter.get(),
                                      "username": user_enter.get(),
                                      "password": pass_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(createEmpFrame, text=f"", font=title)
    label.grid(row=0, column=0, pady=(0, 0))

    label = Label(createEmpFrame, text="First Name", font=text)
    label.grid(row=1, column=0, pady=(0, 0))
    first_enter = Entry(createEmpFrame, font=entry)
    first_enter.grid(row=2, column=0, pady=(0, 25))

    label = Label(createEmpFrame, text="Middle Name", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    mid_enter = Entry(createEmpFrame, font=entry)
    mid_enter.grid(row=4, column=0, pady=(0, 25))

    label = Label(createEmpFrame, text="Last Name", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    last_enter = Entry(createEmpFrame, font=entry)
    last_enter.grid(row=6, column=0, pady=(0, 25))

    label = Label(createEmpFrame, text="Job Title", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    job_enter = Entry(createEmpFrame, font=entry)
    job_enter.grid(row=8, column=0, pady=(0, 25))

    label = Label(createEmpFrame, text="Username", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    user_enter = Entry(createEmpFrame, font=entry)
    user_enter.grid(row=10, column=0, pady=(0, 25))

    label = Label(createEmpFrame, text="Password", font=text)
    label.grid(row=11, column=0, pady=(0, 0))
    pass_enter = Entry(createEmpFrame, font=entry)
    pass_enter.grid(row=12, column=0, pady=(0, 0))

    label_response = Label(createEmpFrame, font=text)
    label_response.grid(row=13, column=0, pady=(20, 20))

    create_button = ttk.Button(createEmpFrame, text="Create",
                           command=lambda: [create_user()],
                           style='my.TButton')
    create_button.grid(row=14, column=0, pady=(0, 25))

    back_button = ttk.Button(createEmpFrame, text="Back",
                         command=lambda: [employeesFrame.grid(),
                                          createEmpFrame.grid_forget(),
                                          employee(),
                                          clear_frame(createEmpFrame)],
                         style='my.TButton')
    back_button.grid(row=15, column=0, pady=(0, 0))


def update_employee(temp):
    def up_user():
        response = requests.put(f"http://127.0.0.1:105/login/update_username/{temp}",
                                json={"new_username": user_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])
        x = user_enter.get()
        clear_frame(updateEmpFrame)
        update_employee(x)

    def up_title():
        response = requests.put(f"http://127.0.0.1:105/employee/update_title/{temp}",
                                json={"new_title": job_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    def up_pass():
        response = requests.put(f"http://127.0.0.1:105/login/update_password/{temp}",
                                json={"old_password": password_old.get(),
                                      "new_password": password_new.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(updateEmpFrame, text=f"{temp}", font=title)
    label.grid(row=0, column=0, pady=(0, 25))

    label = Label(updateEmpFrame, text="Username", font=text)
    label.grid(row=1, column=0, pady=(0, 0))

    user_enter = Entry(updateEmpFrame, font=entry)
    user_enter.grid(row=2, column=0, pady=(0, 0))

    user_update = ttk.Button(updateEmpFrame, text="Update Username",
                         command=lambda: [up_user()],
                         style='my.TButton')
    user_update.grid(row=3, column=0, pady=(10, 50))

    label = Label(updateEmpFrame, text="Job", font=text)
    label.grid(row=4, column=0, pady=(0, 0))

    job_enter = Entry(updateEmpFrame, font=entry)
    job_enter.grid(row=5, column=0, pady=(0, 0))

    job_update = ttk.Button(updateEmpFrame, text="Update Job",
                        command=lambda: [up_title()],
                        style='my.TButton')
    job_update.grid(row=6, column=0, pady=(10, 50))

    label = Label(updateEmpFrame, text="Old Password", font=text)
    label.grid(row=7, column=0, pady=(0, 0))

    password_old = Entry(updateEmpFrame, font=entry)
    password_old.grid(row=8, column=0, pady=(0, 0))

    label = Label(updateEmpFrame, text="New Password", font=text)
    label.grid(row=9, column=0, pady=(0, 0))

    password_new = Entry(updateEmpFrame, font=entry)
    password_new.grid(row=10, column=0, pady=(0, 0))

    password_update = ttk.Button(updateEmpFrame, text="Update Password",
                             command=lambda: [up_pass()],
                             style='my.TButton')
    password_update.grid(row=11, column=0, pady=(10, 25))

    label_response = Label(updateEmpFrame, text="", font=text)
    label_response.grid(row=12, column=0, pady=(0, 0))

    back_button = ttk.Button(updateEmpFrame, text="Back",
                         command=lambda: [employeesFrame.grid(),
                                          updateEmpFrame.grid_forget(),
                                          employee(),
                                          clear_frame(updateEmpFrame)],
                         style='my.TButton')
    back_button.grid(row=13, column=0, pady=(0, 0))


login()
loginFrame.grid()

if __name__ == '__main__':
    root.mainloop()