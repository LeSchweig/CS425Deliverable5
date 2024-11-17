from mysql.connector import connect
import sys
import tkinter as tk
from tkinter import ttk, messagebox

curr_user = 'root'
curr_pass = 'muFf1n!3'
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
    def create_payment(self, order_id, amount, payment_date):
        query = """
        INSERT INTO Payment (OrderID, Amount, PaymentDate)
        VALUES (%s, %s, %s);
        """
        self.create(query, (order_id, amount, payment_date))

    def read_payments(self):
        query = "SELECT * FROM Payment;"
        return self.read(query)

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


    def create_order(self, cid, rid, order_date, eta, total_amount, order_status):
        query = """
        INSERT INTO Orders (CID, RID, OrderDate, ETA, TotalAmount, OrderStatus)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.create(query, (cid, rid, order_date, eta, total_amount, order_status))

    def read_orders(self):
        query = "SELECT * FROM Orders;"
        return self.read(query)

    def update_order(self, order_id, cid, rid, order_date, eta, total_amount, order_status):
        query = """
        UPDATE Orders
        SET CID = %s, RID = %s, OrderDate = %s, ETA = %s, TotalAmount = %s, OrderStatus = %s
        WHERE OrderID = %s;
        """
        self.update(query, (cid, rid, order_date, eta, total_amount, order_status, order_id))

    def delete_order(self, order_id):
        query = "DELETE FROM Orders WHERE OrderID = %s;"
        self.delete(query, (order_id,))
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

        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 4:
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
        print("5. Back to Main Menu")

        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
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
        print("5. Back to Main Menu")

        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                payments = payment_manager.read_payments()
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
        print("5. Back to Main Menu")

        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
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
        print("5. Back to Main Menu")

        try:
            user_choice = int(input("Please pick a choice: "))
            if user_choice == 5:
                break  # Back to Main Menu
            elif user_choice == 1:
                restaurants = restaurant_manager.read_restaurants()
                for restaurant in restaurants:
                    print(restaurant)
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
                addresses = customer_address_manager.read_address()
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



class DatabaseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DoorDash Database Management")
        self.root.geometry("800x600")
        
        #initialize frames
        self.table_selection_frame = ttk.Frame(self.root)
        self.crud_options_frame = ttk.Frame(self.root)
        self.data_frame = ttk.Frame(self.root)
        
        # entries dictionary
        self.entries = {}
        self.setup_listbox()
        
        # tables and schemas
        self.tables = {
            "Customers": ["Customer ID", "Customer Name", "Customer Email", "Customer Phone", "Customer Subscription"],
            "Orders": ["Customer ID", "Restaurant ID", "Driver ID", "Order Date", "ETA", "Total Amount", "Order Status"],
            "Restaurants": ["Restaurant Name", "Food Type", "Opening Time", "Closing Time", "Rating", "Average Price"],
            "Drivers": ["Driver Name", "Phone Number", "Driver Email"],
            "Payments": ["Payment ID", "Order ID", "Amount", "Payment Date"],
            "Customer Address": ["Customer ID", "Street Number", "Street Name", "City", "State", "ZIP Code"],
            "Restaurant Address": ["Restaurant ID", "Street Number", "Street Name", "City", "State", "ZIP Code"],
            "History": ["History ID", "Customer ID", "Order ID", "Payment ID", "Order Date"],
            "Customer History Restaurant": ["History ID", "Restaurant ID"]
        }
        
        self.show_table_selection_frame()
                
    def setup_listbox(self):
        
        scrollbar = ttk.Scrollbar(self.data_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.data_frame, width=80, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    def show_table_selection_frame(self):
        
        self.clear_frames()
        self.table_selection_frame.pack(expand=True, padx=15, pady=15)
        
        ttk.Label(self.table_selection_frame, text="Select a table:", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        self.table_combobox = ttk.Combobox(
            self.table_selection_frame,
            values=list(self.tables.keys()),
            state="readonly",
            width=30
        )
        self.table_combobox.pack(pady=5)
        
        ttk.Button(
            self.table_selection_frame,
            text="Select",
            command=lambda: self.show_crud_options(self.table_combobox.get())
        ).pack(pady=10)

    def show_crud_options(self, selected_table):
        
        if not selected_table:
            messagebox.showerror("Error", "Please select a table")
            return
            
        self.clear_frames()
        self.crud_options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        
        ttk.Label(
            self.crud_options_frame,
            text=f"Selected Table: {selected_table}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # CRUD buttons
        self.create_crud_buttons(selected_table)
        
        # entry fields
        self.create_entry_fields(selected_table)
        
        # return button
        ttk.Button(
            self.crud_options_frame,
            text="Return",
            command=self.show_table_selection_frame
        ).pack(pady=10)

    def create_crud_buttons(self, selected_table):
        btns_frame = ttk.Frame(self.crud_options_frame)
        btns_frame.pack(pady=10)
        crud_buttons = [
            ("Create", lambda: self.create_entity(selected_table)),
            ("Read", lambda: self.read_entities(selected_table)),
            ("Update", lambda: self.update_entity(selected_table)),
            ("Delete", lambda: self.delete_entity(selected_table))
        ]
        
        for text, command in crud_buttons:
            ttk.Button(
                btns_frame,
                text=text,
                command=command,
                width=15
            ).pack(side=tk.LEFT, padx=5)

    def create_entry_fields(self, table_name):
        self.entries.clear()
        fields_frame = ttk.LabelFrame(self.crud_options_frame, text="Enter Data")
        fields_frame.pack(fill=tk.X, padx=20, pady=10)
        canvas = tk.Canvas(fields_frame)
        scrollbar = ttk.Scrollbar(fields_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        for i, field in enumerate(self.tables[table_name]):
            label = ttk.Label(scrollable_frame, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(scrollable_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def clear_frames(self):
        self.table_selection_frame.pack_forget()
        self.crud_options_frame.pack_forget()
        self.data_frame.pack_forget()
        
        for frame in [self.crud_options_frame, self.data_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def validate_input(self, field_name, value):
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
            
        if "ID" in field_name:
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"{field_name} must be a number")
                
        if "Amount" in field_name or "Price" in field_name or "Rating" in field_name:
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"{field_name} must be a number")
                
        return value

    def create_entity(self, table_name):
        try:
            values = {}
            for field, entry in self.entries.items():
                value = entry.get()
                values[field] = self.validate_input(field, value)
            if table_name == "Customers":
                customer_manager.create_customer(**values)
            elif table_name == "Orders":
                order_manager.create_order(**values)
            elif table_name == "Restaurants":
                restaurant_manager.create_restaurant(**values)
            elif table_name == "Drivers":
                driver_manager.create_driver(**values)
            elif table_name == "Payments":
                payment_manager.create_payment(**values)
            elif table_name == "Customer Address":
                    customer_address_manager.create_address(**values)
            elif table_name == "Restaurant Address":
                restaurant_address_manager.create_restaurant_address(**values)
            elif table_name == "History":
                history_manager.create_history(**values)
            elif table_name == "Customer History Restaurant":
                customer_history_restaurant_manager.create_customer_history(**values)

            messagebox.showinfo("Success", f"Created new {table_name} record")
            self.read_entities(table_name)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_entities(self, table_name):
        try:
            if table_name == "Customers":
                data = customer_manager.read_customers()
            elif table_name == "Orders":
                data = order_manager.read_orders()
            elif table_name == "Restaurants":
                data = restaurant_manager.read_restaurants()
            elif table_name == "Drivers":
                data = driver_manager.read_drivers()
            elif table_name == "Payments":
                data = payment_manager.read_payments()
            elif table_name == "Customer Address":
                data = customer_address_manager.read_addresses()
            elif table_name == "Restaurant Address":
                data = restaurant_address_manager.read_restaurant_addresses()
            elif table_name == "History":
                data = history_manager.read_history()
            elif table_name == "Customer History Restaurant":
                data = customer_history_restaurant_manager.read_customer_history()
                
            self.clear_frames()
            self.data_frame.pack(fill=tk.BOTH, expand=True)
            self.display_data(data, table_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def update_entity(self, table_name):
        try:
            record_id = self.get_selected_record_id()
            values = self.get_updated_values()
            if not values:
                raise ValueError("No fields to update")
                
            if table_name == "Customers":
                customer_manager.update_customer(record_id, **values)
            elif table_name == "Orders":
                order_manager.update_order(record_id, **values)
            elif table_name == "Restaurants":
                restaurant_manager.update_restaurant(record_id, **values)
            elif table_name == "Drivers":
                driver_manager.update_driver(record_id, **values)
            elif table_name == "Payments":
                payment_manager.update_payment(record_id, **values)
            elif table_name == "Customer Address":
                customer_address_manager.update_address(record_id, **values)
            elif table_name == "Restaurant Address":
                restaurant_address_manager.update_restaurant_address(record_id, **values)
            elif table_name == "History":
                history_manager.update_history(record_id, **values)
                
            messagebox.showinfo("Success", "Record updated")
            self.read_entities(table_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def delete_entity(self, table_name):
    if messagebox.askyesno("Confirm Delete", "Are you sure?"):
        try:
            record_id = self.get_selected_record_id()
            
            if table_name == "Customers":
                customer_manager.delete_customer(record_id)
            elif table_name == "Orders":
                order_manager.delete_order(record_id)
            elif table_name == "Restaurants":
                restaurant_manager.delete_restaurant(record_id)
            elif table_name == "Drivers":
                driver_manager.delete_driver(record_id)
            elif table_name == "Payments":
                payment_manager.delete_payment(record_id)
            elif table_name == "Customer Address":
                customer_address_manager.delete_address(record_id)
            elif table_name == "Restaurant Address":
                restaurant_address_manager.delete_restaurant_address(record_id)
            elif table_name == "History":
                history_manager.delete_history(record_id)
            elif table_name == "Customer History Restaurant":
                ids = record_id.split(',')  
                history_id = ids[0]
                restaurant_id = ids[1]
                customer_history_restaurant_manager.delete_customer_history(history_id, restaurant_id)
                
            messagebox.showinfo("Success", "Record deleted")
            self.read_entities(table_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
