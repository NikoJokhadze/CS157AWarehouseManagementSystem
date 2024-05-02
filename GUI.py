import tkinter.ttk
from tkinter import *
from tkinter import scrolledtext, ttk
import requests

from time import sleep

root = Tk()
root.geometry("900x900")
root.resizable(False, False)

loginFrame = Frame(root)
mainFrame = Frame(root)
ordersFrame = Frame(root)
warehousesFrame = Frame(root)
itemsFrame = Frame(root)
employeesFrame = Frame(root)
update_emp = Frame(root)

link = "http://127.0.0.1:5000"


title = ("Arial", 25)
text = ("Arial", 12)

root.grid_columnconfigure(0, weight=1)


def login():
    def test_login():
        user = user_enter.get()
        pas = pass_enter.get()
        if user == "1" and pas == "1":
            loginFrame.grid_forget()
            mainFrame.grid()
        else:
            login_button.configure(text="Wrong", bg="red")
            login_button.after(1000, lambda: login_button.configure(text="Enter", bg="#F0F0F0"))

    label = Label(loginFrame, text="Login", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    login_label = Label(loginFrame, text="Username", font=text)
    login_label.grid(row=1, column=0)

    user_enter = Entry(loginFrame, font=("Arial", 15))
    user_enter.grid(row=2, column=0, pady=(0, 25))

    pass_label = Label(loginFrame, text="Password", font=text)
    pass_label.grid(row=3, column=0)

    pass_enter = Entry(loginFrame, show="*", font=("Arial", 15))
    pass_enter.grid(row=4, column=0)

    login_button = Button(loginFrame, text="Enter", command=test_login, font=("Arial", 20))
    login_button.grid(row=5, column=0, pady=(50, 0))


def main():
    orders_button = Button(mainFrame, text="Orders",
                           command=lambda: [ordersFrame.grid(),mainFrame.grid_forget()], font=("Arial", 20))
    orders_button.grid(row=0, column=0, pady=(25, 0))

    warehouses_button = Button(mainFrame, text="Warehouses",
                               command=lambda: [warehousesFrame.grid(),mainFrame.grid_forget()], font=("Arial", 20))
    warehouses_button.grid(row=1, column=0, pady=(50, 0))

    items_button = Button(mainFrame, text="Items",
                          command=lambda: [itemsFrame.grid(),mainFrame.grid_forget()], font=("Arial", 20))
    items_button.grid(row=2, column=0, pady=(50, 0))

    employees_button = Button(mainFrame, text="Employees",
                              command=lambda: [employeesFrame.grid(),mainFrame.grid_forget(), employee()], font=("Arial", 20))
    employees_button.grid(row=3, column=0, pady=(50, 0))

def orders():
    label = Label(ordersFrame, text="This the order frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(ordersFrame, text="Back",
                              command=lambda: [mainFrame.grid(), ordersFrame.grid_forget()], font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


def warehouse():
    label = Label(warehousesFrame, text="This the warehouse frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(warehousesFrame, text="Back",
                              command=lambda: [mainFrame.grid(), warehousesFrame.grid_forget()], font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))

def item():
    label = Label(itemsFrame, text="This the item frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(itemsFrame, text="Back",
                              command=lambda: [mainFrame.grid(), itemsFrame.grid_forget()], font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


def employee():
    def clear_table():
        for x in box.get_children():
            box.delete(x)

    label = Label(employeesFrame, text="This the employee frame", font=title)
    label.grid(row=0, column=0, pady=(0, 50))

    box = ttk.Treeview(employeesFrame, selectmode ="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = Scrollbar(employeesFrame, orient="vertical", command = box.yview)
    scroll.grid(row=1, column=1, pady=(0, 0), sticky="ns")

    box.configure(yscrollcommand=scroll.set)
    box["columns"] = ("1", "2", "3", "4")
    box['show'] = 'headings'

    box.column("1", width=50)
    box.column("2", width=180)
    box.column("3", width=80)
    box.column("4", width=80)

    box.heading("1", text="ID")
    box.heading("2", text="Name")
    box.heading("3", text="Job")
    box.heading("4", text="UserName")


    response = requests.get(f"{link}/employee/get_all")
    for i in response.json():
        box.insert("","end",values=i)

    user_enter = Entry(employeesFrame, font=("Arial", 15))
    user_enter.grid(row=2, column=0, pady=(50, 0))

    update_emp_button = Button(employeesFrame, text="Update Employee",
                              command=lambda: [update_emp.grid(),
                                               employeesFrame.grid_forget(),
                                               update_employee(user_enter.get()),
                                               clear_table()
                                               ],
                              font=("Arial", 20))
    update_emp_button.grid(row=3, column=0, pady=(0, 0))

    back_button = Button(employeesFrame, text="Back",
                              command=lambda: [mainFrame.grid(), employeesFrame.grid_forget(), clear_table()], font=("Arial", 20))
    back_button.grid(row=4, column=0, pady=(50, 0))

def update_employee(temp):
    label = Label(update_emp, text=f"This Username {temp}", font=title)
    label.grid(row=0, column=0, pady=(0, 0))

    back_button = Button(update_emp, text="Back",
                         command=lambda: [employeesFrame.grid(),
                                          update_emp.grid_forget(),
                                          employee()],
                         font=("Arial", 20))
    back_button.grid(row=4, column=0, pady=(0, 0))


main()
login()
orders()
warehouse()
item()
employee()
loginFrame.grid()
update_employee(0)

if __name__ == '__main__':
    root.mainloop()
