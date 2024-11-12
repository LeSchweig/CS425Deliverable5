# 13/15 queries added

class DatabaseManager:
    def __init__(self,cursor):
        self.cursor = cursor
    def create(self,query,data):
        self.cursor.execute(query, data)
        conn.commit()
        print("Created successfully")
    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def update(self, query, data):
        self.cursor.execute(query, data)
        conn.commit()
        print("Updated successfully")
    def delete(self, query, data):
        self.cursor.execute(query, data)
        conn.commit()
        print("Record deleted successfully.")

class CustomerManager(DatabaseManager):
    def create_customer(self, name, email, phone, subscription='none'):
        query = """
        INSERT INTO Customers (CName, Email, PhoneNumber, Subscription)
        VALUES (%s, %s, %s, %s);
        """
        self.create(query, (name, email, phone, subscription))

    def read_customers(self):
        query = "SELECT * FROM Customers;"
        return self.read(query)

    def update_customer(self, customer_id, name, email, phone, subscription):
        query = """
        UPDATE Customers
        SET CName = %s, Email = %s, PhoneNumber = %s, Subscription = %s
        WHERE CID = %s;
        """
        self.update(query, (name, email, phone, subscription, customer_id))

    def delete_customer(self, customer_id):
        query = "DELETE FROM Customers WHERE CID = %s;"
        self.delete(query, (customer_id,))
    
    def show_num_orders(self):
        query = """
        SELECT customers.CID, customers.CName, COUNT(orders.OrderID) AS NumOrders 
        FROM customers LEFT JOIN orders ON customers.CID = orders.CID GROUP BY customers.CID, customers.CName ORDER BY NumOrders DESC;
        """
        self.read(query)
    
    def show_last_order_date(self):
        query = """"
        SELECT c.CID, c.CName, c.Email, MAX(o.OrderDate) AS LastOrderDate
        FROM customers c
        LEFT JOIN orders o ON c.CID = o.CID
        GROUP BY c.CID, c.CName, c.Email
        HAVING MAX(o.OrderDate) < DATE_SUB(NOW(), INTERVAL 3 MONTH) OR MAX(o.OrderDate) IS NULL
        ORDER BY LastOrderDate;
        """
        self.read(query)

class OrderManager(DatabaseManager):
    def create_order(self, cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status):
        query = """
        INSERT INTO Orders (CID, RestaurantID, DriverID, OrderDate, ETA, TotalAmount, OrderStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        self.create(query, (cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status))

    def read_orders(self):
        query = "SELECT * FROM Orders;"
        return self.read(query)

    def update_order(self, order_id, cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status):
        query = """
        UPDATE Orders
        SET CID = %s, RestaurantID = %s, DriverID = %s, OrderDate = %s, ETA = %s, TotalAmount = %s, OrderStatus = %s
        WHERE OrderID = %s;
        """
        self.update(query, (cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status, order_id))

    def delete_order(self, order_id):
        query = "DELETE FROM Orders WHERE OrderID = %s;"
        self.delete(query, (order_id,))

    def show_active_orders(self):
        query = """
        SELECT RName, COUNT(OrderID) AS Open_Orders
        FROM Orders JOIN Restaurant ON Orders.RestaurantID = Restaurant.RID
        WHERE OrderStatus IN ('scheduled', 'assigned')
        GROUP BY RestaurantID
        ORDER BY Open_Orders DESC;
        """
        self.read(query)
    
    def show_done_orders(self):
        query = """
        SELECT D.Dname, D.Email, D.PhoneNumber, O.OrderStatus
        FROM Driver AS D JOIN Orders AS O ON D.DID = O.DriverID
        WHERE O.OrderStatus IN ('delivered', 'canceled');
        """
        self.read(query)
    
    def show_rolling_week_sales(self):
        query = """
        SELECT OrderID, CID, OrderDate, TotalAmount, SUM(TotalAmount) OVER (
            PARTITION BY CID
            ORDER BY OrderDate
            ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
        ) AS RollingWeekSales
        FROM orders
        ORDER BY OrderDate;
        """
        self.read(query)
    
    def show_cumulative_revenue(self):
        query = """
        SELECT CID,OrderID,OrderDate,TotalAmount,
        SUM(TotalAmount) OVER (
            PARTITION BY CID
            ORDER BY OrderDate) AS CumulativeRevenue
        FROM orders
        ORDER BY CID, OrderDate;
        """
        self.read(query)
    
    def show_total_revenue(self):
        query = """
        SELECT CID, SUM(TotalAmount) AS TotalRevenue
        FROM orders
        WHERE OrderDate >= '2024-08-19'
        GROUP BY CID
        ORDER BY TotalRevenue DESC
        LIMIT 5;
        """
        self.read(query)
    
    def show_order_count(self):
        query = """
        SELECT YEAR(OrderDate) as Year, MONTH(OrderDate) AS Month, COUNT(*) AS OrderCount
        FROM History
        GROUP BY YEAR(OrderDate), MONTH(OrderDate)
        ORDER BY Year, Month;
        """
        self.read(query)

class RestaurantManager(DatabaseManager):
    def create_restaurant(self, name, ftype, otime, ctime, rating, aprice):
        query = """
        INSERT INTO Restaurant (RName, FType, OTime, CTime, Rating, APrice)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (name, ftype, otime, ctime, rating, aprice))

    def read_restaurants(self):
        query = "SELECT * FROM Restaurant;"
        return self.read(query)

    def update_restaurant(self, rid, name, ftype, otime, ctime, rating, aprice):
        query = """
        UPDATE Restaurant
        SET RName = %s, FType = %s, OTime = %s, CTime = %s, Rating = %s, APrice = %s
        WHERE RID = %s;
        """
        self.update(query, (name, ftype, otime, ctime, rating, aprice, rid))

    def delete_restaurant(self, rid):
        query = "DELETE FROM Restaurant WHERE RID = %s;"
        self.delete(query, (rid,))

    def check_open(self):
        query = """"
        SELECT RName, FType, Rating, Distance, APrice
        FROM Restaurant
        WHERE ADDTIME(CURTIME(), '00:30:00') < CTime
        AND CURTIME() >= OTime;
        """
        self.read(query)
    
    def higher_rating_and_price(self):
        query = """
        WITH Avg_Rating AS (
        SELECT AVG(Rating) AS RatingVal
        FROM Restaurant
        ),
        Avg_Price AS (
            SELECT AVG(APrice) AS AvgPrice
            FROM Restaurant
        )
        SELECT RName, FType, OTime, CTime, Rating, APrice
        FROM Restaurant, Avg_Rating, Avg_Price
        WHERE Rating > RatingVal AND APrice > AvgPrice;
        """
        self.read(query)
    
    def restaurant_rank(self):
        query = """
        SELECT *, 
        DENSE_RANK() OVER (PARTITION BY FType ORDER BY Rating DESC) AS Ranking
        FROM Restaurant
        ORDER BY Ranking;
        """
        self.read(query)
    
    def show_orders_between(self):
        query = """
        SELECT * 
        FROM History
        WHERE OrderDate BETWEEN '2022-01-20' AND '2022-01-30';
        """
        self.read(query)

class DriverManager(DatabaseManager):
    def create_driver(self, name, phone, email):
        query = """
        INSERT INTO Driver (DName, PhoneNumber, Email)
        VALUES (%s, %s, %s);
        """
        self.create(query, (name, phone, email))

    def read_drivers(self):
        query = "SELECT * FROM Driver;"
        return self.read(query)

    def update_driver(self, did, name, phone, email):
        query = """
        UPDATE Driver
        SET DName = %s, PhoneNumber = %s, Email = %s
        WHERE DID = %s;
        """
        self.update(query, (name, phone, email, did))

    def delete_driver(self, did):
        query = "DELETE FROM Driver WHERE DID = %s;"
        self.delete(query, (did,))

class PaymentManager(DatabaseManager):
    def create_payment(self, order_id, payment_date, payment_type):
        query = """
        INSERT INTO Payment (OrderID, PaymentDate, PaymentType)
        VALUES (%s, %s, %s);
        """
        self.create(query, (order_id, payment_date, payment_type))

    def read_payments(self):
        query = "SELECT * FROM Payment;"
        return self.read(query)

    def update_payment(self, payment_id, order_id, payment_date, payment_type):
        query = """
        UPDATE Payment
        SET OrderID = %s, PaymentDate = %s, PaymentType = %s
        WHERE PaymentID = %s;
        """
        self.update(query, (order_id, payment_date, payment_type, payment_id))

    def delete_payment(self, payment_id):
        query = "DELETE FROM Payment WHERE PaymentID = %s;"
        self.delete(query, (payment_id,))
    
    def show_payment_count(self):
        query = """
        SELECT PaymentType, COUNT(*) as PaymentCount
        FROM Payment
        GROUP BY PaymentType;
        """
        self.read(query)

class CustomerAddressManager(DatabaseManager):
    def create_address(self, cid, street_num, street_name, city, state, zip_code):
        query = """
        INSERT INTO Customer_Address (CID, StreetNum, StreetName, City, State, ZipCode)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (cid, street_num, street_name, city, state, zip_code))

    def read_addresses(self):
        query = "SELECT * FROM Customer_Address;"
        return self.read(query)

    def update_address(self, cid, street_num, street_name, city, state, zip_code):
        query = """
        UPDATE Customer_Address
        SET StreetNum = %s, StreetName = %s, City = %s, State = %s, ZipCode = %s
        WHERE CID = %s;
        """
        self.update(query, (street_num, street_name, city, state, zip_code, cid))

    def delete_address(self, cid):
        query = "DELETE FROM Customer_Address WHERE CID = %s;"
        self.delete(query, (cid,))


class RestaurantAddressManager(DatabaseManager):
    def create_restaurant_address(self, rid, street_num, street_name, city, state, zip_code):
        query = """
        INSERT INTO Restaurant_Address (RID, StreetNum, StreetName, City, State, ZipCode)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (rid, street_num, street_name, city, state, zip_code))

    def read_restaurant_addresses(self):
        query = "SELECT * FROM Restaurant_Address;"
        return self.read(query)

    def update_restaurant_address(self, rid, street_num, street_name, city, state, zip_code):
        query = """
        UPDATE Restaurant_Address
        SET StreetNum = %s, StreetName = %s, City = %s, State = %s, ZipCode = %s
        WHERE RID = %s;
        """
        self.update(query, (street_num, street_name, city, state, zip_code, rid))

    def delete_restaurant_address(self, rid):
        query = "DELETE FROM Restaurant_Address WHERE RID = %s;"
        self.delete(query, (rid,))


class HistoryManager(DatabaseManager):
    def create_history(self, cid, order_id, payment_id, order_date):
        query = """
        INSERT INTO History (CID, OrderID, PaymentID, OrderDate)
        VALUES (%s, %s, %s, %s);
        """
        self.create(query, (cid, order_id, payment_id, order_date))

    def read_history(self):
        query = "SELECT * FROM History;"
        return self.read(query)

    def update_history(self, history_id, cid, order_id, payment_id, order_date):
        query = """
        UPDATE History
        SET CID = %s, OrderID = %s, PaymentID = %s, OrderDate = %s
        WHERE HistoryID = %s;
        """
        self.update(query, (cid, order_id, payment_id, order_date, history_id))

    def delete_history(self, history_id):
        query = "DELETE FROM History WHERE HistoryID = %s;"
        self.delete(query, (history_id,))


class CustomerHistoryRestaurantManager(DatabaseManager):
    def create_customer_history(self, history_id, rid):
        query = """
        INSERT INTO CustomerHistory_restaurant (HistoryID, RID)
        VALUES (%s, %s);
        """
        self.create(query, (history_id, rid))

    def read_customer_history(self):
        query = "SELECT * FROM CustomerHistory_restaurant;"
        return self.read(query)

    def delete_customer_history(self, history_id, rid):
        query = "DELETE FROM CustomerHistory_restaurant WHERE HistoryID = %s AND RID = %s;"
        self.delete(query, (history_id, rid))