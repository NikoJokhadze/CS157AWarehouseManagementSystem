create database if not exists WarehouseSystem;
use WarehouseSystem;

-- This table details all information about inventory on a unit-to-unit basis (or group of units if applicable)
create table Item (
    itemID int not null, -- The main identifying ID number for an item
    itemName varchar(99) not null, -- The name of the item
    itemWeight int not null, -- Gives weight of unit or group of units in some number of some scale, decide weight scale later
    itemPrice int not null, -- Gives price of each unit/group unit
    arrivalTime date, -- Says when the item arrived at the warehouse
    itemStatus varchar(99) not null, -- Tells if the item is ordered/in stock/out of stock
    orderID int, -- If the item is ordered, give the orderID
    warehouseID int not null, -- Details which warehouse the item belongs in
    itemLocation varchar(99) not null, -- Says where in the warehouse the item is stored in
    primary key (itemID),
    foreign key (warehouseID) references Warehouse(warehouseID),
    foreign key (orderID) references Orders(orderID)
);

-- This table shows how much of each item is present in each warehouse
create table ItemQuantity (
    warehouseID int not null,
    itemName varchar(99) not null,
    itemQuantity int not null, -- Gives total count of each item in each warehouse
    foreign key (itemName) references Item(itemName),
    foreign key (warehouseID) references Warehouse(warehouseID)
);

-- This table shows the warehouse information, meant for if a service owns multiple warehouses
create table Warehouse (
    warehouseID int not null,
    capacity varchar(99) not null, -- Gives info on total capacity of warehouse
    -- Following 4 columns give location data
    city varchar(99) not null,
    street varchar(99) not null,
    buildingNumber int not null,
    zipCode int not null,
    primary key (warehouseID)
);

-- This table details order information based on items
create table Orders (
    orderID int not null,
    orderStatus varchar(99) not null, -- Gives status of order, such as shipped, delivered, in process, etc.
    departureTime date, -- States when the order left the warehouse
    deliveryAddress varchar(999), -- Gives full delivery location information
    handlerID int not null, -- Gives ID of employee/service handling the order
    primary key (orderID)
);

-- This table shows basic information about warehouse employees, those who can access the warehouse's system
create table Employee (
    employeeID int not null, -- Unique ID for each employee
    -- The following 3 columns are for employee names
    firstName varchar(99) not null,
    middleName varchar(99),
    lastName varchar(99) not null,
    jobTitle varchar(99) not null, -- Says the job position of the employee
    primary key (employeeID)
);

-- This table stores the login information to access the system
create table Login (
    username varchar(99) not null,
    hashedPassword varchar(256) not null, -- For security purposes, we store the hashed password
    employeeID int not null
);