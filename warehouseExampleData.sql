Use WarehouseSystem;

insert into Addresses (addressNum, street, city, zipCode, warehouse) values
    (1155, "S Yankton Avenue", "San Jose", 95121, true),
    (90822, "East Street", "Washington D.C.", 20005, false),
    (55, "Green Hill Road", "Los Angeles", 90048, true),
    (33, "Spooner Street", "Chicago", 60602, false),
    (601, "N Alpine Drive", "Austin", 78653, false),
    (7, "12th Avenue", "Oakland", 94605, false),
    (542, "Johnson Drive", "New York", 10010, true);

insert into Warehouse (warehouseID, warehouseAddressID, capacity) values
    (12345, 1, 40000),
    (87439, 7, 6000),
    (78312, 3, 25000);

insert into Employee (firstName, middleName, lastName, jobTitle) values
    ("Mary", NULL, "Poppins", "CEO"),
	("Michael", NULL, "De Santa", "Manager"),
	("Josep", "Emanuel", "Guardiola", "Supervisor"),
    ("Olgilvie", "Maurice", "Hedgehog", "Supervisor"),
    ("Joe", NULL, "Swanson", "Handler"),
    ("Mark", "John", "Paul", "Handler"),
    ("May", NULL, "Heims", "Handler"),
    ("Erik", NULL, "van Den", "Handler"),
    ("test", NULL, "user", "Tool");

insert into Login (username, hashedPassword, employeeId) values
    ("marpop", "PopMar!5", 1000),
    ("micdesan", "micSan2%", 1001),
    ("joemdiola", "JoeGuar6*", 1002),
    ("olgi", "Mauhog5!", 1003),
    ("joeswan", "JoeSon", 1004),
    ("marjonpau", "johnmArk", 1005),
    ("heims", "uniQue2$", 1006),
    ("erikDen", "newPassword@3", 1007),
    ("test", "admin", 1008);

insert into Item (itemName, itemWeight, itemPrice) values
    ("Nintendo Switch", 0.66, 299.99),
    ("XBox Series X", 9.8, 499.99),
    ("XBox Series S", 4.25, 349.99),
    ("XBox One", 7.7, 199.99),
    ("Apple Macbook Air 13-inch", 2.7, 1499.99),
    ("Apple Macbook Pro 15-inch", 3.4, 1699.99),
    ("Apple Airpod Generation 2", 0.00875, 249.99),
    ("Play Station 5", 9.9, 449.99),
    ("Play Station 4", 6.2, 229.99),
    ("Samsung Galaxy Tab", 1.04, 349.99),
    ("Canon ImageClass Printer", 64, 369.99);

insert into ItemInWarehouse (warehouseID, itemID, arrivalTime, itemLocation, itemQuantity) values
    (12345, 1, '2024-01-05', "B4", 300),
    (12345, 2, '2024-02-02', "C2", 400),
    (12345, 3, '2024-02-03', "C3", 400),
    (12345, 4, '2022-10-20', "C1", 0),
    (12345, 8, '2024-01-27', "D3", 150),
    (12345, 9, '2022-09-23', "D4", 0),
    (87439, 5, '2024-02-03', "A3", 800),
    (87439, 6, '2024-02-04', "A4", 800),
    (87439, 7, '2023-09-05', "A2", 3000),
    (87439, 10, '2024-03-21', "B1", 600),
    (87439, 11, '2024-02-29', "D2", 80);

insert into Orders (orderStatus, departureTime, deliveryAddressID, handlerID) values
	("Delivered", '2024-03-01', 2, 1007),
	("Shippped", '2024-03-15', 4, 1004),
	("Received", NULL, 6, 1006),
	("Received", NULL, 5, 1005);

insert into ItemsOrdered (orderID, itemID, itemQuantity) values
    (1, 1, 100),
    (2, 7, 150),
    (1, 6, 500),
    (3, 7, 250),
    (3, 11, 30),
    (4, 3, 100),
    (3, 5, 550),
    (2, 10, 100);