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
            "Customers": ["CID", "CName", "Email", "PhoneNumber", "Subscription"],
            "Orders": ["OrderID", "CID", "RestaurantID", "DriverID", "OrderDate", "ETA", "TotalAmount", "OrderStatus"],
            "Restaurants": ["RID", "RName", "FType", "OTime", "CTime", "Rating", "APrice"],
            "Drivers": ["DID", "DName", "PhoneNumber", "Email"],
            "Payments": ["PaymentID", "OrderID", "Amount", "PaymentDate"],
            "Customer Address": ["CID", "StreetNum", "StreetName", "City", "State", "ZipCode"],
            "Restaurant Address": ["RID", "StreetNum", "StreetName", "City", "State", "ZipCode"],
            "History": ["HistoryID", "CID", "OrderID", "PaymentID", "OrderDate"],
            "Customer History Restaurant": ["HistoryID", "RID"]
        }
        
        self.show_table_selection_frame()
    def get_selected_record_id(self):
        selection = self.listbox.curselection()
        if not selection:
            raise ValueError("Please select a record")
        
        
        if selection[0] <= 1:
            raise ValueError("Please select a data record, not the header")
            
        record = self.listbox.get(selection[0])
        return record.split()[0]
    def get_updated_values(self):
        values = {}
        for field, entry in self.entries.items():
            value = entry.get()
            if value.strip():   
                values[field] = self.validate_input(field, value)
        return values

    def display_data(self, data, table_name):
        self.listbox.delete(0, tk.END)
        for record in data:
            self.listbox.insert(tk.END, ' '.join(str(field) for field in record))

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
                customer_manager.create_customer(
                    name=values["Customer Name"],
                    email=values["Customer Email"],
                    phone=values["Customer Phone"],
                    subscription=values["Customer Subscription"]
                )
            elif table_name == "Orders":
                order_manager.create_order(
                    cid=values["Customer ID"],
                    restaurant_id=values["Restaurant ID"],
                    driver_id=values["Driver ID"],
                    order_date=values["Order Date"],
                    eta=values["ETA"],
                    total_amount=values["Total Amount"],
                    order_status=values["Order Status"]
                )
            elif table_name == "Restaurants":
                restaurant_manager.create_restaurant(
                    name=values["Restaurant Name"],
                    ftype=values["Food Type"],
                    otime=values["Opening Time"],
                    ctime=values["Closing Time"],
                    rating=values["Rating"],
                    aprice=values["Average Price"]
                )
            elif table_name == "Drivers":
                driver_manager.create_driver(
                    name=values["Driver Name"],
                    phone=values["Phone Number"],
                    email=values["Driver Email"]
                )
            elif table_name == "Payments":
                payment_manager.create_payment(
                    order_id=values["Order ID"],
                    amount=values["Amount"],
                    payment_date=values["Payment Date"]
                )
            elif table_name == "Customer Address":
                customer_address_manager.create_address(
                    cid=values["Customer ID"],
                    street_num=values["Street Number"],
                    street_name=values["Street Name"],
                    city=values["City"],
                    state=values["State"],
                    zip_code=values["ZIP Code"]
                )
            elif table_name == "Restaurant Address":
                restaurant_address_manager.create_restaurant_address(
                    rid=values["Restaurant ID"],
                    street_num=values["Street Number"],
                    street_name=values["Street Name"],
                    city=values["City"],
                    state=values["State"],
                    zip_code=values["ZIP Code"]
                )
            elif table_name == "History":
                history_manager.create_history(
                    cid=values["Customer ID"],
                    order_id=values["Order ID"],
                    payment_id=values["Payment ID"],
                    order_date=values["Order Date"]
                )
            elif table_name == "Customer History Restaurant":
                customer_history_restaurant_manager.create_customer_history(
                    history_id=values["History ID"],
                    rid=values["Restaurant ID"]
                )

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
            values = {}
            for field, entry in self.entries.items():
                value = entry.get()
                if value.strip():  # Only include non-empty fields
                    values[field] = self.validate_input(field, value)

            if not values:
                raise ValueError("No fields to update")

            if table_name == "Customers":
                customer_manager.update_customer(
                    customer_id=record_id,
                    name=values.get("Customer Name"),
                    email=values.get("Customer Email"),
                    phone=values.get("Customer Phone"),
                    subscription=values.get("Customer Subscription")
                )
            elif table_name == "Orders":
                order_manager.update_order(
                    order_id=record_id,
                    cid=values.get("Customer ID"),
                    restaurant_id=values.get("Restaurant ID"),
                    driver_id=values.get("Driver ID"),
                    order_date=values.get("Order Date"),
                    eta=values.get("ETA"),
                    total_amount=values.get("Total Amount"),
                    order_status=values.get("Order Status")
                )
            elif table_name == "Restaurants":
                restaurant_manager.update_restaurant(
                    rid=record_id,
                    name=values.get("Restaurant Name"),
                    ftype=values.get("Food Type"),
                    otime=values.get("Opening Time"),
                    ctime=values.get("Closing Time"),
                    rating=values.get("Rating"),
                    aprice=values.get("Average Price")
                )
            elif table_name == "Drivers":
                driver_manager.update_driver(
                    did=record_id,
                    name=values.get("Driver Name"),
                    phone=values.get("Phone Number"),
                    email=values.get("Driver Email")
                )
            elif table_name == "Payments":
                payment_manager.update_payment(
                    payment_id=record_id,
                    order_id=values.get("Order ID"),
                    amount=values.get("Amount"),
                    payment_date=values.get("Payment Date")
                )
            elif table_name == "Customer Address":
                customer_address_manager.update_address(
                    cid=record_id,
                    street_num=values.get("Street Number"),
                    street_name=values.get("Street Name"),
                    city=values.get("City"),
                    state=values.get("State"),
                    zip_code=values.get("ZIP Code")
                )
            elif table_name == "Restaurant Address":
                restaurant_address_manager.update_restaurant_address(
                    rid=record_id,
                    street_num=values.get("Street Number"),
                    street_name=values.get("Street Name"),
                    city=values.get("City"),
                    state=values.get("State"),
                    zip_code=values.get("ZIP Code")
                )
            elif table_name == "History":
                history_manager.update_history(
                    history_id=record_id,
                    cid=values.get("Customer ID"),
                    order_id=values.get("Order ID"),
                    payment_id=values.get("Payment ID"),
                    order_date=values.get("Order Date")
                )

            messagebox.showinfo("Success", "Record updated")
            self.read_entities(table_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def display_data(self, data, table_name):
        self.listbox.delete(0, tk.END)
        headers = self.tables[table_name]
        self.listbox.insert(tk.END, " ".join(str(header) for header in headers))
        self.listbox.insert(tk.END, "-" * 80)  
        
        for record in data:
            self.listbox.insert(tk.END, " ".join(str(field) for field in record))
            
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
