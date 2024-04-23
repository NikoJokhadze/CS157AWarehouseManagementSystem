from tkinter import *
from time import sleep

root = Tk()
root.geometry("450x450")
root.resizable(False, False)

loginFrame = Frame(root)
mainFrame = Frame(root)
ordersFrame = Frame(root)
warehousesFrame = Frame(root)
itemsFrame = Frame(root)
employeesFrame = Frame(root)

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
                              command=lambda: [employeesFrame.grid(),mainFrame.grid_forget()], font=("Arial", 20))
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
    label = Label(employeesFrame, text="This the order frame", font=title)
    label.grid(row=0, column=0, pady=(0, 100))

    back_button = Button(employeesFrame, text="Back",
                              command=lambda: [mainFrame.grid(), employeesFrame.grid_forget()], font=("Arial", 20))
    back_button.grid(row=1, column=0, pady=(50, 0))


main()
login()
orders()
warehouse()
item()
employee()
loginFrame.grid()

if __name__ == '__main__':
    root.mainloop()
