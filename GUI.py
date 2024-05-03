import json
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
create_emp = Frame(root)

title = ("Arial", 25)
text = ("Arial", 12)

root.grid_columnconfigure(0, weight=1)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def login():
    def test_login():
        user = user_enter.get()
        pas = pass_enter.get()
        if user == "1" and pas == "1":
            main()
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
                           command=lambda: [ordersFrame.grid(),
                                            mainFrame.grid_forget(),
                                            orders()],
                           font=("Arial", 20))
    orders_button.grid(row=0, column=0, pady=(25, 0))

    warehouses_button = Button(mainFrame, text="Warehouses",
                               command=lambda: [warehousesFrame.grid(),
                                                mainFrame.grid_forget(),
                                                warehouse()],
                               font=("Arial", 20))
    warehouses_button.grid(row=1, column=0, pady=(50, 0))

    items_button = Button(mainFrame, text="Items",
                          command=lambda: [itemsFrame.grid(),
                                           mainFrame.grid_forget(),
                                           item()],
                          font=("Arial", 20))
    items_button.grid(row=2, column=0, pady=(50, 0))

    employees_button = Button(mainFrame, text="Employees",
                              command=lambda: [employeesFrame.grid(),
                                               mainFrame.grid_forget(),
                                               employee()],
                              font=("Arial", 20))
    employees_button.grid(row=3, column=0, pady=(50, 0))


def orders():
    label = Label(ordersFrame, text="This the order frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    box = ttk.Treeview(employeesFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    back_button = Button(ordersFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          ordersFrame.grid_forget()],
                         font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


def warehouse():
    label = Label(warehousesFrame, text="This the warehouse frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(warehousesFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          warehousesFrame.grid_forget(),
                                          clear_frame(warehousesFrame)],
                         font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


def item():
    label = Label(itemsFrame, text="This the item frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(itemsFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          itemsFrame.grid_forget(),
                                          clear_frame(itemsFrame)],
                         font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


def employee():
    def del_emp():
        response = requests.delete(f"http://127.0.0.1:105/employee/delete_employee/{user_enter.get()}")
        clear_frame(employeesFrame)
        employee()

    label = Label(employeesFrame, text="This the employee frame", font=title)
    label.grid(row=0, column=0, pady=(0, 50))

    box = ttk.Treeview(employeesFrame, selectmode="browse")
    box.grid(row=1, column=0, pady=(0, 0))

    scroll = Scrollbar(employeesFrame, orient="vertical", command=box.yview)
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

    response = requests.get(f"http://127.0.0.1:105/employee/get_all")
    for i in response.json():
        box.insert("", "end", values=i)

    user_enter = Entry(employeesFrame, font=("Arial", 15))
    user_enter.grid(row=2, column=0, pady=(50, 0))

    update_emp_button = Button(employeesFrame, text="Update Employee",
                               command=lambda: [update_emp.grid(),
                                                employeesFrame.grid_forget(),
                                                update_employee(user_enter.get()),
                                                clear_frame(employeesFrame)],
                               font=("Arial", 20))
    update_emp_button.grid(row=3, column=0, pady=(0, 0))

    del_button = Button(employeesFrame, text="Delete Employee",
                        command=lambda: [del_emp()],
                        font=("Arial", 20))
    del_button.grid(row=4, column=0, pady=(50, 0))

    cre_button = Button(employeesFrame, text="Create Employee",
                        command=lambda: [create_emp.grid(),
                                         employeesFrame.grid_forget(),
                                         create_employee(),
                                         clear_frame(employeesFrame)],
                        font=("Arial", 20))
    cre_button.grid(row=5, column=0, pady=(50, 0))

    back_button = Button(employeesFrame, text="Back",
                         command=lambda: [mainFrame.grid(),
                                          employeesFrame.grid_forget(),
                                          clear_frame(employeesFrame)],
                         font=("Arial", 20))
    back_button.grid(row=6, column=0, pady=(50, 0))


def create_employee():
    def create_user():
        response = requests.post(f"http://127.0.0.1:105/employee/create_user",
                                json={"firstName": first_enter.get(),
                                      "middleName": mid_enter.get(),
                                      "lastName": last_enter.get(),
                                      "jobTitle": job_enter.get(),
                                      "username": user_enter.get(),
                                      "password": pass_enter.get()})
        print(response.text)
        response = json.loads(response.text)
        label_response.config(text=response["message"])

    label = Label(create_emp, text=f"Create Employee", font=title)
    label.grid(row=0, column=0, pady=(0, 0))

    label = Label(create_emp, text="First Name", font=text)
    label.grid(row=1, column=0, pady=(0, 0))
    first_enter = Entry(create_emp, font=("Arial", 15))
    first_enter.grid(row=2, column=0, pady=(0, 50))

    label = Label(create_emp, text="Middle Name", font=text)
    label.grid(row=3, column=0, pady=(0, 0))
    mid_enter = Entry(create_emp, font=("Arial", 15))
    mid_enter.grid(row=4, column=0, pady=(0, 50))

    label = Label(create_emp, text="Last Name", font=text)
    label.grid(row=5, column=0, pady=(0, 0))
    last_enter = Entry(create_emp, font=("Arial", 15))
    last_enter.grid(row=6, column=0, pady=(0, 50))

    label = Label(create_emp, text="Job Title", font=text)
    label.grid(row=7, column=0, pady=(0, 0))
    job_enter = Entry(create_emp, font=("Arial", 15))
    job_enter.grid(row=8, column=0, pady=(0, 50))

    label = Label(create_emp, text="Username", font=text)
    label.grid(row=9, column=0, pady=(0, 0))
    user_enter = Entry(create_emp, font=("Arial", 15))
    user_enter.grid(row=10, column=0, pady=(0, 50))

    label = Label(create_emp, text="Password", font=text)
    label.grid(row=11, column=0, pady=(0, 0))
    pass_enter = Entry(create_emp, font=("Arial", 15))
    pass_enter.grid(row=12, column=0, pady=(0, 50))

    label_response = Label(create_emp, font=text)
    label_response.grid(row=14, column=0, pady=(20, 20))

    create_button = Button(create_emp, text="Create",
                           command=lambda: [create_user()],
                           font=("Arial", 20))
    create_button.grid(row=13, column=0, pady=(0, 25))

    back_button = Button(create_emp, text="Back",
                         command=lambda: [employeesFrame.grid(),
                                          create_emp.grid_forget(),
                                          employee(),
                                          clear_frame(create_emp)],
                         font=("Arial", 20))
    back_button.grid(row=15, column=0, pady=(0, 0))


def update_employee(temp):
    def up_user():
        response = requests.put(f"http://127.0.0.1:105/login/update_username/{temp}",
                                json={"new_username": user_enter.get()})
        response = json.loads(response.text)
        label_response.config(text=response["message"])

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

    label = Label(update_emp, text=f"This Username {temp}", font=title)
    label.grid(row=0, column=1, pady=(0, 0))

    user_enter = Entry(update_emp, font=("Arial", 15))
    user_enter.grid(row=1, column=0, pady=(50, 0))

    user_update = Button(update_emp, text="Update Username",
                         command=lambda: [user_update.configure(text="Done"),
                                          up_user()],
                         font=("Arial", 20))
    user_update.grid(row=1, column=2, pady=(50, 0))

    job_enter = Entry(update_emp, font=("Arial", 15))
    job_enter.grid(row=2, column=0, pady=(50, 0))

    job_update = Button(update_emp, text="Update Job",
                        command=lambda: [job_update.configure(text="Done"),
                                         up_title()],
                        font=("Arial", 20))
    job_update.grid(row=2, column=2, pady=(50, 0))

    password_old = Entry(update_emp, font=("Arial", 15))
    password_old.grid(row=3, column=0, pady=(50, 0))

    password_new = Entry(update_emp, font=("Arial", 15))
    password_new.grid(row=3, column=1, pady=(50, 0))

    password_update = Button(update_emp, text="Update Password",
                             command=lambda: [password_update.configure(text="Done"),
                                              up_pass()],
                             font=("Arial", 20))
    password_update.grid(row=3, column=2, pady=(50, 0))

    label_response = Label(update_emp, text="", font=text)
    label_response.grid(row=4, column=1, pady=(0, 0))

    back_button = Button(update_emp, text="Back",
                         command=lambda: [employeesFrame.grid(),
                                          update_emp.grid_forget(),
                                          employee(),
                                          clear_frame(update_emp)],
                         font=("Arial", 20))
    back_button.grid(row=5, column=1, pady=(0, 0))


login()
loginFrame.grid()

if __name__ == '__main__':
    root.mainloop()
