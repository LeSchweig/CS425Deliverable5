CREATE DATABASE DoorDash;
USE DoorDash;

CREATE TABLE Customers(
	CID INT PRIMARY KEY AUTO_INCREMENT,
    CName VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    Subscription ENUM('none', 'monthly', 'yearly') DEFAULT 'none'
);

CREATE TABLE Customer_Address(
	CID int,
    StreetNum int unsigned,
    StreetName varchar(20),
    City varchar(15),
    State char(2),
    ZipCode int,
    foreign key (CID) REFERENCES Customers(CID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Restaurant(
	RID smallint unsigned auto_increment,
	RName varchar(30) not null,
	FType varchar(30),
	OTime time,
	CTime time,
	Rating decimal (3,2),
	APrice smallint,
	primary key(RID)
);

CREATE TABLE Restaurant_Address(
	RID smallint unsigned,
    StreetNum smallint unsigned,
    StreetName varchar(20),
    City varchar(15),
    State char(2),
    ZipCode int,
    foreign key (RID) REFERENCES Restaurant(RID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Driver(
	DID smallint unsigned auto_increment,
    DName varchar(30) not null,
    PhoneNumber char(12),
    Email varchar(30),
    primary key(DID)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CID INT,
    RestaurantID SMALLINT UNSIGNED,
    DriverID SMALLINT UNSIGNED,
    OrderDate DATE,
    ETA TIME,
    TotalAmount DECIMAL(10,2),
    OrderStatus ENUM('scheduled', 'delivered', 'assigned', 'picked_up', 'canceled'),
    FOREIGN KEY (CID) REFERENCES Customers(CID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DriverID) REFERENCES Driver(DID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Payment(
    PaymentID SMALLINT UNSIGNED AUTO_INCREMENT,
    OrderID INT,
    PaymentDate DATE,
    PaymentType VARCHAR(30),
    PRIMARY KEY(PaymentID),
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE History(
	HistoryID smallint unsigned auto_increment,
    CID INT,
    OrderID int,
    PaymentID smallint unsigned,
    OrderDate date,
    primary key(HistoryID),
	foreign key(CID) references Customers(CID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(OrderID) references Orders(OrderID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE CustomerHistory_restaurant(
	HistoryID smallint unsigned auto_increment,
    RID smallint unsigned,
	primary key (HistoryID, RID),
    foreign key(HistoryID) references History(HistoryID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(RID) references Restaurant(RID) ON DELETE CASCADE ON UPDATE CASCADE
);