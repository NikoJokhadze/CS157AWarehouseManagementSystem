create database if not exists WarehouseSystem;
use WarehouseSystem;

-- This table details information about delivery addresses
create table if not exists Addresses (
    addressID int not null, -- Each address will be associated with a unique ID
    addressNum int not null,
    street varchar(99) not null,
    city varchar(99) not null,
    zipCode int not null,
    warehouse bool not null, -- Determines whether this address is a warehouse address or delivery address
    primary key (addressID)
);

-- This table shows the warehouse information, meant for if a service owns multiple warehouses
create table if not exists Warehouse (
    warehouseID int not null,
    warehouseAddressID int not null,
    capacity int not null, -- Gives info on total capacity of warehouse in square feet
    primary key (warehouseID),
    foreign key (warehouseAddressID) references Addresses(addressID)
);

-- This table details all information about inventory on a unit-to-unit basis (or group of units if applicable)
create table if not exists Item (
    itemID int not null AUTO_INCREMENT, -- The main identifying ID number for an item
    itemName varchar(99) not null, -- The name of the item
    itemWeight float not null, -- Gives weight of unit or group of units in pounds
    itemPrice float not null, -- Gives price of each unit/group unit
    primary key (itemID)
);

-- This table stores information for items in case the same item is stored in multiple warehouses
-- as well as quantity of each item
create table if not exists ItemInWarehouse (
    warehouseID int not null, -- Details which warehouse the item belongs in
    itemID int not null,
    arrivalTime date, -- Says when the item arrived at the warehouse
    itemLocation varchar(99) not null, -- Says where in the warehouse the item is stored in
    itemQuantity int not null default 0, -- Gives number of items in warehouse. We assume that all are in same location
    foreign key (warehouseID) references Warehouse(warehouseID),
    foreign key (itemID) references Item(itemID)
);

-- This table details order information based on items
create table if not exists Orders (
    orderID int not null AUTO_INCREMENT,
    orderStatus varchar(99) not null, -- Gives status of order, such as received, shipped, delivered
    departureTime date, -- States when the order left the warehouse
    deliveryAddressID int not null, -- Gives full delivery location information
    handlerID int not null, -- Gives ID of employee/service handling the order
    primary key (orderID),
    foreign key (deliveryAddressID) references Addresses(addressID)
);

-- This table shows how many of each item is in an order
create table if not exists ItemsOrdered (
    orderID int not null, -- Each item will be associated to a respective order ID
    itemID int not null,
    itemQuantity int not null, -- Describes how many of each item is in the order (how many orders)
    foreign key (orderID) references Orders(orderID),
    foreign key (itemID) references Item(itemID)
);

-- This table shows basic information about warehouse employees, those who can access the warehouse's system
create table if not exists Employee (
    employeeID int not null AUTO_INCREMENT, -- Unique ID for each employee
    -- The following 3 columns are for employee names
    firstName varchar(99) not null,
    middleName varchar(99),
    lastName varchar(99) not null,
    jobTitle varchar(99) not null, -- Says the job position of the employee
    primary key (employeeID)
) AUTO_INCREMENT=1000;

-- This table stores the login information to access the system
create table if not exists Login (
    username varchar(99) not null,
    hashedPassword varchar(256) not null, -- For security purposes, we store the hashed password
    employeeID int not null,
    foreign key (employeeID) references Employee(employeeID)
);