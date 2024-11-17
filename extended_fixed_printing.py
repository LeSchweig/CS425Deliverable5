from mysql.connector import connect
import sys
curr_user = 'root'
curr_pass = 'Lenargo&1138'
curr_host = 'localhost'
curr_database = 'doordash'
conn = connect(
    user=curr_user,
    password=curr_pass,
    host=curr_host,
    database=curr_database
)
if conn.is_connected():
    print("Connection established")
# Cursor object is used to interact with the database
cursor = conn.cursor()
class DatabaseManager:
    def __init__(self, cursor):
        self.cursor = cursor
    def create(self, query, data):
        self.cursor.execute(query, data)
        conn.commit()
        print("Created successfully")
    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def print_records(self, query, attributes):
        items = self.read(query)
        if items is not None:
            for item in items:
              print("")
              num_attributes = len(attributes)
              for index in range (num_attributes):
                if index == len(attributes) - 1:
                    last_char = " "
                else:
                    last_char = ", "
                print(f"{attributes[index]}: {item[index]}", end = last_char)
                num_attributes -= 1
            print("\n")
        else:
            print("There are no records in this table.\n")
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
        return self.print_records(query, ['CID', 'Name', 'Email', 'PhoneNumber', 'Subscription'])
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
        return self.print_records(query, ['CID', 'Name', 'Email', 'PhoneNumber', 'Subscription'])
    def show_last_order_date(self):
        query = """"
        SELECT c.CID, c.CName, c.Email, MAX(o.OrderDate) AS LastOrderDate
        FROM customers c
        LEFT JOIN orders o ON c.CID = o.CID
        GROUP BY c.CID, c.CName, c.Email
        HAVING MAX(o.OrderDate) < DATE_SUB(NOW(), INTERVAL 3 MONTH) OR MAX(o.OrderDate) IS NULL
        ORDER BY LastOrderDate;
        """
        return self.print_records(query, ['CID', 'Name', 'Email', 'PhoneNumber', 'Subscription'])

class OrderManager(DatabaseManager):
    def create_order(self, cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status):
        query = """
        INSERT INTO Orders (CID, RestaurantID, DriverID, OrderDate, ETA, TotalAmount, OrderStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        self.create(query, (cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status))
    def read_orders(self):
        query = "SELECT * FROM Orders;"
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
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
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
    def show_done_orders(self):
        query = """
        SELECT D.Dname, D.Email, D.PhoneNumber, O.OrderStatus
        FROM Driver AS D JOIN Orders AS O ON D.DID = O.DriverID
        WHERE O.OrderStatus IN ('delivered', 'canceled');
        """
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
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
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
    def show_cumulative_revenue(self):
        query = """
        SELECT CID,OrderID,OrderDate,TotalAmount,
        SUM(TotalAmount) OVER (
            PARTITION BY CID
            ORDER BY OrderDate) AS CumulativeRevenue
        FROM orders
        ORDER BY CID, OrderDate;
        """
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
    def show_total_revenue(self):
        query = """
        SELECT CID, SUM(TotalAmount) AS TotalRevenue
        FROM orders
        WHERE OrderDate >= '2024-08-19'
        GROUP BY CID
        ORDER BY TotalRevenue DESC
        LIMIT 5;
        """
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])
    def show_order_count(self):
        query = """
        SELECT YEAR(OrderDate) as Year, MONTH(OrderDate) AS Month, COUNT(*) AS OrderCount
        FROM History
        GROUP BY YEAR(OrderDate), MONTH(OrderDate)
        ORDER BY Year, Month;
        """
        return self.print_records(query, ['OID', 'CID', 'RID', 'DriverID', 'OrderDate', 'ETA', 'TotalAmount', 'OrderStatus'])

class RestaurantManager(DatabaseManager):
    def create_restaurant(self, name, ftype, otime, ctime, rating, aprice):
        query = """
        INSERT INTO Restaurant (RName, FType, OTime, CTime, Rating, APrice)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (name, ftype, otime, ctime, rating, aprice))
    def read_restaurants(self):
        query = "SELECT * FROM Restaurant;"
        self.print_records(query, ['RID', 'RName', 'FType', 'OTime', 'CTime', 'Rating', 'Aprice'])
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
        WHERE ADDTIME(CURTIME(), '00:30:00') < CTime AND CURTIME() >= OTime;
        """
        self.print_records(query, ['RID', 'RName', 'FType', 'OTime', 'CTime', 'Rating', 'Aprice'])
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
        WHERE Rating > RatingVal AND APrice < AvgPrice;
        """
        self.print_records(query, ['RID', 'RName', 'FType', 'OTime', 'CTime', 'Rating', 'Aprice'])
    def restaurant_rank(self):
        query = """
        SELECT *, 
        DENSE_RANK() OVER (PARTITION BY Aprice ORDER BY Rating DESC) AS Ranking
        FROM Restaurant
        ORDER BY Ranking;
        """
        self.print_records(query, ['RID', 'RName', 'FType', 'OTime', 'CTime', 'Rating', 'Aprice', 'Ranking'])
    def show_orders_between(self):
        query = """
        SELECT * 
        FROM History
        WHERE OrderDate BETWEEN '2022-01-20' AND '2022-01-30';
        """
        self.print_records(query, ['RID', 'RName', 'FType', 'OTime', 'CTime', 'Rating', 'Aprice'])
class DriverManager(DatabaseManager):
    def create_driver(self, name, phone, email):
        query = """
        INSERT INTO Driver (DName, PhoneNumber, Email)
        VALUES (%s, %s, %s);
        """
        self.create(query, (name, phone, email))
    def read_drivers(self):
        query = "SELECT * FROM Driver;"
        return self.print_records(query, ['DID', 'Name', 'Phone', 'Email'])
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
    def create_payment(self, order_id, amount, payment_date):
        query = """
        INSERT INTO Payment (OrderID, Amount, PaymentDate)
        VALUES (%s, %s, %s);
        """
        self.create(query, (order_id, amount, payment_date))
    def read_payments(self):
        query = "SELECT * FROM Payment;"
        return self.print_records(query, ['PaymentID', 'OrderID', 'Amount', 'Payment Date'])
    def update_payment(self, payment_id, order_id, amount, payment_date):
        query = """
        UPDATE Payment
        SET OrderID = %s, Amount = %s, PaymentDate = %s
        WHERE PaymentID = %s;
        """
        self.update(query, (order_id, amount, payment_date, payment_id))
    def delete_payment(self, payment_id):
        query = "DELETE FROM Payments WHERE PaymentID = %s;"
        self.delete(query, (payment_id,))
    def show_payment_count(self):
      query = """
      SELECT PaymentType, COUNT(*) as PaymentCount
      FROM Payment
      GROUP BY PaymentType;
      """
      return self.print_records(query, ['PaymentID', 'OrderID', 'Amount', 'Payment Date'])
    def show_previous_payment(self):
      query = """
      SELECT PaymentID, PaymentType, PaymentDate, 
      LAG(PaymentDate, 1) OVER (PARTITION BY PaymentType ORDER BY PaymentDate) AS PreviousPaymentDate
      FROM Payment;
      """
      return self.print_records(query, ['PaymentID', 'OrderID', 'Amount', 'Payment Date'])
    def show_most_used_payment(self):
      query = """
      SELECT PaymentType, COUNT(*) AS MostUsed
      FROM Payment
      GROUP BY PaymentType
      ORDER BY MostUsed DESC
      LIMIT 3;
      """
      return self.print_records(query, ['PaymentID', 'OrderID', 'Amount', 'Payment Date'])
class CustomerAddressManager(DatabaseManager):
    def create_address(self, cid, street_num, street_name, city, state, zip_code):
        query = """
        INSERT INTO Customer_Address (CID, StreetNum, StreetName, City, State, ZipCode)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (cid, street_num, street_name, city, state, zip_code))
    def read_addresses(self):
        query = "SELECT * FROM Customer_Address;"
        return self.print_records(query, ['CID', 'StreetNum', 'StreetName', 'City', 'State', 'ZipCode'])
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
        #return self.print_records(query, ['RID', 'StreetNum', 'StreetName', 'City', 'State', 'ZipCode'])
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
        return self.print_records(query, ['CID', 'OrderID', 'PaymentID', 'OrderDate'])
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
        return self.print_records(query, ['HistoryID', 'RID'])
    def delete_customer_history(self, history_id, rid):
        query = "DELETE FROM CustomerHistory_restaurant WHERE HistoryID = %s AND RID = %s;"
        self.delete(query, (history_id, rid))
customer_manager = CustomerManager(cursor)
order_manager = OrderManager(cursor)
restaurant_manager = RestaurantManager(cursor)
driver_manager = DriverManager(cursor)
payment_manager = PaymentManager(cursor)
history_manager = HistoryManager(cursor)
customer_history_restaurant_manager= CustomerHistoryRestaurantManager(cursor)
customer_address_manager = CustomerAddressManager(cursor)
restaurant_address_manager = RestaurantAddressManager(cursor)
def create_menu():
    while True:
        print("\nMain Menu:")
        print("1. Customer Management")
        print("2. Payment Management")
        print("3. Order Management")
        print("4. Resturant Management")
        print("5. Driver Management")
        print("6. CustomerAdress Management")
        print("7. ResturantAdress Management")
        print("8. History Management")
        print("9. CustomerHistory Management")
        print("10. Exit program")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 10:
                sys.exit() 
            elif user_choice in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                manage_entity(user_choice)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def manage_entity(choice):
    if choice == 1:
        customer_menu()
    elif choice == 2:
        payment_menu()
    elif choice == 3:
        order_menu()
    elif choice == 4:
        restaurant_menu()
    elif choice == 5:
        driver_menu()
    elif choice == 6:
        customer_address_menu()
    elif choice == 7:
        restaurant_address_menu()
    elif choice == 8:
        history_menu()
    elif choice == 9:
        customerhistory_menu()
def customer_menu():
    while True:
        print("\nCustomer Management Menu:")
        print("1. Read Customers")
        print("2. Create Customer")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Show Number of Orders")
        print("6. Show last order date")
        print("7. Back to Main Menu")
        try:
          user_choice = int(input("Please pick a choice: "))
          if user_choice == 7:
              break  # Back to Main Menu
          elif user_choice == 1:
              customers = customer_manager.read_customers()
              for customer in customers:
                  print(customer)
          elif user_choice == 2:
              name = input("Enter customer name: ")
              email = input("Enter customer email: ")
              phone = input("Enter customer phone number: ")
              subscription = input("Enter subscription type (none/monthly/yearly): ")
              customer_manager.create_customer(name, email, phone, subscription)
          elif user_choice == 3:
              customer_id = int(input("Enter customer ID to update: "))
              name = input("Enter new customer name: ")
              email = input("Enter new customer email: ")
              phone = input("Enter new customer phone number: ")
              subscription = input("Enter new subscription type (none/monthly/yearly): ")
              customer_manager.update_customer(customer_id, name, email, phone, subscription)
          elif user_choice == 4:
              customer_id = int(input("Enter customer ID to delete: "))
              customer_manager.delete_customer(customer_id)
              print("Delete method has been completed.")
          elif user_choice == 5:
              customer_manager.show_num_orders()
          elif user_choice == 6:
              customer_manager.show_last_order_date()
          else:
              print("The option you selected was not valid.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def payment_menu():
    while True:
        print("\nPayment Management Menu:")
        print("1. Read Payments")
        print("2. Create Payment")
        print("3. Update Payment")
        print("4. Delete Payment")
        print("5. Show Payment Count")
        print("6. Show Previous Payment")
        print("7. Show Most Used Payment")
        print("8. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 8:
                break  # Back to Main Menu
            elif user_choice == 1:
                payments = payment_manager.read_payment()
                for payment in payments:
                    print(payment)
            elif user_choice == 2:
                order_id = int(input("Enter order ID: "))
                amount = float(input("Enter payment amount: "))
                payment_date = input("Enter payment date (YYYY-MM-DD): ")
                payment_manager.create_payment(order_id, amount, payment_date)
            elif user_choice == 3:
                payment_id = int(input("Enter payment ID to update: "))
                order_id = int(input("Enter new order ID: "))
                amount = float(input("Enter new payment amount: "))
                payment_date = input("Enter new payment date (YYYY-MM-DD): ")
                payment_manager.update_payment(payment_id, order_id, amount, payment_date)
            elif user_choice == 4:
                payment_id = int(input("Enter payment ID to delete: "))
                payment_manager.delete_payment(payment_id)
                print("Delete method has been completed.")
            elif user_choice == 5:
                payment_manager.show_payment_count()
            elif user_choice == 6:
                payment_manager.show_previous_payment()
            elif user_choice == 7:
                payment_manager.show_most_used_payment()
            else:
                print("The option you selected was not valid.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def order_menu():
    while True:
        print("\nOrder Management Menu:")
        print("1. Read Orders")
        print("2. Create Order")
        print("3. Update Order")
        print("4. Delete Order")
        print("5. Show Active Orders")
        print("6. Show Done Orders")
        print("7. Show Rolling Week Sales")
        print("8. Show Cumulative Revenue")
        print("9. Show total revenue")
        print("10. Show Order Count")
        print("11. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 11:
                break  # Back to Main Menu
            elif user_choice == 1:
                orders = order_manager.read_orders()
                for order in orders:
                    print(order)
            elif user_choice == 2:
                cid = int(input("Enter customer ID: "))
                rid = int(input("Enter restaurant ID: "))
                order_date = input("Enter order date (YYYY-MM-DD): ")
                eta = input("Enter estimated time of arrival: ")
                total_amount = float(input("Enter total amount: "))
                order_status = input("Enter order status: ")
                order_manager.create_order(cid, rid, order_date, eta, total_amount, order_status)
            elif user_choice == 3:
                order_id = int(input("Enter order ID to update: "))
                cid = int(input("Enter new customer ID: "))
                rid = int(input("Enter new restaurant ID: "))
                order_date = input("Enter new order date (YYYY-MM-DD): ")
                eta = input("Enter new estimated time of arrival: ")
                total_amount = float(input("Enter new total amount: "))
                order_status = input("Enter new order status: ")
                order_manager.update_order(order_id, cid, rid, order_date, eta, total_amount, order_status)
            elif user_choice == 4:
                order_id = int(input("Enter order ID to delete: "))
                order_manager.delete_order(order_id)
                print("Delete method has been completed.")
            elif user_choice == 5:
                order_manager.show_active_orders()
            elif user_choice == 6:
                order_manager.show_done_orders()
            elif user_choice == 7:
                order_manager.show_rolling_week_sales()
            elif user_choice == 8:
                order_manager.show_cumulative_revenue()
            elif user_choice == 9:
                order_manager.show_total_revenue()
            elif user_choice == 10:
                order_manager.show_order_count()
            else:
                print("The option you selected was not valid.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def restaurant_menu():
    while True:
        print("\nRestaurant Management Menu:")
        print("1. Read Restaurants")
        print("2. Create Restaurant")
        print("3. Update Restaurant")
        print("4. Delete Restaurant")
        print("5. Show Open Restaurants")
        print("6. Show Restaurants with High Rating and High Price")
        print("7. Show Restaurant Rank")
        print("8. Show Orders Between Dates")
        print("9. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 9:
                break  # Back to Main Menu
            elif user_choice == 1:
                restaurant_manager.read_restaurants()
            elif user_choice == 2:
                name = input("Enter restaurant name: ")
                ftype = input("Enter food type: ")
                otime = input("Enter opening time: ")
                ctime = input("Enter closing time: ")
                rating = float(input("Enter restaurant rating (0-5): "))
                aprice = float(input("Enter average price: "))
                restaurant_manager.create_restaurant(name, ftype, otime, ctime, rating, aprice)
            elif user_choice == 3:
                rid = int(input("Enter restaurant ID to update: "))
                name = input("Enter new restaurant name: ")
                ftype = input("Enter new food type: ")
                otime = input("Enter new opening time: ")
                ctime = input("Enter new closing time: ")
                rating = float(input("Enter new restaurant rating (0-5): "))
                aprice = float(input("Enter new average price: "))
                restaurant_manager.update_restaurant(rid, name, ftype, otime, ctime, rating, aprice)
            elif user_choice == 4:
                rid = int(input("Enter restaurant ID to delete: "))
                restaurant_manager.delete_restaurant(rid)
            elif user_choice == 5:
                restaurant_manager.check_open()
            elif user_choice == 6:
                restaurant_manager.higher_rating_and_price()
            elif user_choice == 7:
                restaurant_manager.restaurant_rank()
            elif user_choice == 8:
                restaurant_manager.show_orders_between()
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def driver_menu():
    while True:
        print("\nDriver Management Menu:")
        print("1. Read Drivers")
        print("2. Create Driver")
        print("3. Update Driver")
        print("4. Delete Driver")
        print("5. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                drivers = driver_manager.read_drivers()
                for driver in drivers:
                    print(driver)
            elif user_choice == 2:
                name = input("Enter driver name: ")
                phone = input("Enter driver phone number: ")
                email = input("Enter driver email: ")
                driver_manager.create_driver(name, phone, email)
            elif user_choice == 3:
                driver_id = int(input("Enter driver ID to update: "))
                name = input("Enter new driver name: ")
                phone = input("Enter new driver phone number: ")
                email = input("Enter new driver email: ")
                driver_manager.update_driver(driver_id, name, phone, email)
            elif user_choice == 4:
                driver_id = int(input("Enter driver ID to delete: "))
                driver_manager.delete_driver(driver_id)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def customer_address_menu():
    while True:
        print("\nCustomer Address Management Menu:")
        print("1. Read Customer Addresses")
        print("2. Create Customer Address")
        print("3. Update Customer Address")
        print("4. Delete Customer Address")
        print("5. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                addresses = customer_address_manager.read_addresses()
                for address in addresses:
                    print(address)
            elif user_choice == 2:
                customer_id = int(input("Enter customer ID: "))
                street = input("Enter street: ")
                city = input("Enter city: ")
                state = input("Enter state: ")
                zip_code = input("Enter ZIP code: ")
                customer_address_manager.create_address(customer_id, street, city, state, zip_code)
            elif user_choice == 3:
                address_id = int(input("Enter address ID to update: "))
                customer_id = int(input("Enter new customer ID: "))
                street = input("Enter new street: ")
                city = input("Enter new city: ")
                state = input("Enter new state: ")
                zip_code = input("Enter new ZIP code: ")
                customer_address_manager.update_address(address_id, customer_id, street, city, state, zip_code)
            elif user_choice == 4:
                address_id = int(input("Enter address ID to delete: "))
                customer_address_manager.delete_address(address_id)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def restaurant_address_menu():
    while True:
        print("\nRestaurant Address Management Menu:")
        print("1. Read Restaurant Addresses")
        print("2. Create Restaurant Address")
        print("3. Update Restaurant Address")
        print("4. Delete Restaurant Address")
        print("5. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                addresses = restaurant_address_manager.read_addresses()
                for address in addresses:
                    print(address)
            elif user_choice == 2:
                restaurant_id = int(input("Enter restaurant ID: "))
                street = input("Enter street: ")
                city = input("Enter city: ")
                state = input("Enter state: ")
                zip_code = input("Enter ZIP code: ")
                restaurant_address_manager.create_address(restaurant_id, street, city, state, zip_code)
                print("Restaurant address created successfully.")
            elif user_choice == 3:
                address_id = int(input("Enter address ID to update: "))
                restaurant_id = int(input("Enter new restaurant ID: "))
                street = input("Enter new street: ")
                city = input("Enter new city: ")
                state = input("Enter new state: ")
                zip_code = input("Enter new ZIP code: ")
                restaurant_address_manager.update_address(address_id, restaurant_id, street, city, state, zip_code)
                print("Restaurant address updated successfully.")
            elif user_choice == 4:
                address_id = int(input("Enter address ID to delete: "))
                restaurant_address_manager.delete_address(address_id)
                print("Restaurant address deleted successfully.")
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def history_menu():
    while True:
        print("\nHistory Management Menu:")
        print("1. Read History Records")
        print("2. Create History Record")
        print("3. Update History Record")
        print("4. Delete History Record")
        print("5. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                history_records = history_manager.read_history()
                for record in history_records:
                    print(record)
            elif user_choice == 2:
                cid = int(input("Enter customer ID (CID): "))
                order_id = int(input("Enter order ID: "))
                payment_id = int(input("Enter payment ID: "))
                order_date = input("Enter order date (YYYY-MM-DD): ")
                history_manager.create_history(cid, order_id, payment_id, order_date)
                print("History record created successfully.")
            elif user_choice == 3:
                history_id = int(input("Enter history ID to update: "))
                cid = int(input("Enter new customer ID (CID): "))
                order_id = int(input("Enter new order ID: "))
                payment_id = int(input("Enter new payment ID: "))
                order_date = input("Enter new order date (YYYY-MM-DD): ")
                history_manager.update_history(history_id, cid, order_id, payment_id, order_date)
                print("History record updated successfully.")
            elif user_choice == 4:
                history_id = int(input("Enter history ID to delete: "))
                history_manager.delete_history(history_id)
                print("History record deleted successfully.")
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
def customerhistory_menu():
    while True:
        print("\nCustomer History Management Menu:")
        print("1. Read Customer History Records")
        print("2. Create Customer History Record")
        print("3. Update Customer History Record")
        print("4. Delete Customer History Record")
        print("5. Back to Main Menu")
        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                customer_history_records = customer_address_manager.read_customer_history()
                for record in customer_history_records:
                    print(record)
            elif user_choice == 2:
                cid = int(input("Enter customer ID (CID): "))
                order_id = int(input("Enter order ID: "))
                payment_id = int(input("Enter payment ID: "))
                order_date = input("Enter order date (YYYY-MM-DD): ")
                customer_address_manager.create_customer_history(cid, order_id, payment_id, order_date)
                print("Customer history record created successfully.")
            elif user_choice == 3:
                history_id = int(input("Enter customer history ID to update: "))
                cid = int(input("Enter new customer ID (CID): "))
                order_id = int(input("Enter new order ID: "))
                payment_id = int(input("Enter new payment ID: "))
                order_date = input("Enter new order date (YYYY-MM-DD): ")
                customer_address_manager.update_customer_history(history_id, cid, order_id, payment_id, order_date)
                print("Customer history record updated successfully.")
            elif user_choice == 4:
                history_id = int(input("Enter customer history ID to delete: "))
                customer_address_manager.delete_customer_history(history_id)
                print("Customer history record deleted successfully.")
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Input is not valid, please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    create_menu()