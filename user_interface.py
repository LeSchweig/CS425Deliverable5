import tkinter as tk
from tkinter import ttk
from tkinter import *
import database_manager.py
import use_cases.py

def create_entity(entity_name):
    if entity_name == "Customers":
        customer_id_label = ttk.Label(crud_options_frame, text="Customer ID:")
        customer_id_label.grid(row=1, column=0, padx=5, pady=5)
        customer_id_entry = ttk.Entry(crud_options_frame)
        customer_id_entry.grid(row=1, column=1, padx=5, pady=5)
        customer_name_label = ttk.Label(crud_options_frame, text="Customer Name:")
        customer_name_label.grid(row=1, column=0, padx=5, pady=5)
        customer_name_entry = ttk.Entry(crud_options_frame)
        customer_name_entry.grid(row=1, column=1, padx=5, pady=5)
        customer_email_label = ttk.Label(crud_options_frame, text="Customer Email:")
        customer_email_label.grid(row=1, column=0, padx=5, pady=5)
        customer_email_entry = ttk.Entry(crud_options_frame)
        customer_email_entry.grid(row=1, column=1, padx=5, pady=5)
        customer_phone_label = ttk.Label(crud_options_frame, text="Customer Phone Number:")
        customer_phone_label.grid(row=1, column=0, padx=5, pady=5)
        customer_phone_entry = ttk.Entry(crud_options_frame)
        customer_phone_entry.grid(row=1, column=1, padx=5, pady=5)
        customer_subscription_label = ttk.Label(crud_options_frame, text="Customer Subscription:")
        customer_subscription_label.grid(row=1, column=0, padx=5, pady=5)
        customer_subscription_entry = ttk.Entry(crud_options_frame)
        customer_subscription_entry.grid(row=1, column=1, padx=5, pady=5)
        
        create_button = ttk.Button(crud_options_frame, text="Create", command=create_customer)
        create_button.grid(row=2, columnspan=2, padx=5, pady=5)
    elif entity_name == "Orders":
        order_cid_label = ttk.Label(crud_options_frame, text="Customer ID:")
        order_cid_label.grid(row=1, column=0, padx=5, pady=5)
        order_cid_entry = ttk.Entry(crud_options_frame)
        order_cid_entry.grid(row=1, column=1, padx=5, pady=5)
        order_restaurant_id_label = ttk.Label(crud_options_frame, text="Restaurant ID")
        order_restaurant_id_label.grid(row=1, column=0, padx=5, pady=5)
        order_restaurant_id_entry = ttk.Entry(crud_options_frame)
        order_restaurant_id_entry.grid(row=1, column=1, padx=5, pady=5)
        order_driver_id_label = ttk.Label(crud_options_frame, text="Driver ID:")
        order_driver_id_label.grid(row=1, column=0, padx=5, pady=5)
        order_driver_id_entry = ttk.Entry(crud_options_frame)
        order_driver_id_entry.grid(row=1, column=1, padx=5, pady=5)
        order_date_label = ttk.Label(crud_options_frame, text="Order Date:")
        order_date_label.grid(row=1, column=0, padx=5, pady=5)
        order_date_entry = ttk.Entry(crud_options_frame)
        order_date_entry.grid(row=1, column=1, padx=5, pady=5)
        order_eta_label = ttk.Label(crud_options_frame, text="ETA:")
        order_eta_label.grid(row=1, column=0, padx=5, pady=5)
        order_eta_entry = ttk.Entry(crud_options_frame)
        order_eta_entry.grid(row=1, column=1, padx=5, pady=5)
        order_amount_label = ttk.Label(crud_options_frame, text="Total Amount:")
        order_amount_label.grid(row=1, column=0, padx=5, pady=5)
        order_amount_entry = ttk.Entry(crud_options_frame)
        order_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        order_status_label = ttk.Label(crud_options_frame, text="Order Status:")
        order_status_label.grid(row=1, column=0, padx=5, pady=5)
        order_status_entry = ttk.Entry(crud_options_frame)
        order_status_entry.grid(row=1, column=1, padx=5, pady=5)
        
        create_button = ttk.Button(crud_options_frame, text="Create", command=create_order)
        create_button.grid(row=2, columnspan=2, padx=5, pady=5)

    if entity_name == "Restaurants":
        restaurant_name_label = ttk.Label(crud_options_frame, text="Restaurant Name:")
        restaurant_name_label.grid(row=1, column=0, padx=5, pady=5)
        restaurant_name_entry = ttk.Entry(crud_options_frame)
        restaurant_name_entry.grid(row=1, column=1, padx=5, pady=5)

        food_type_label = ttk.Label(crud_options_frame, text="Food Type:")
        food_type_label.grid(row=2, column=0, padx=5, pady=5)
        food_type_entry = ttk.Entry(crud_options_frame)
        food_type_entry.grid(row=2, column=1, padx=5, pady=5)

        opening_time_label = ttk.Label(crud_options_frame, text="Opening Time:")
        opening_time_label.grid(row=3, column=0, padx=5, pady=5)
        opening_time_entry = ttk.Entry(crud_options_frame)
        opening_time_entry.grid(row=3, column=1, padx=5, pady=5)

        closing_time_label = ttk.Label(crud_options_frame, text="Closing Time:")
        closing_time_label.grid(row=4, column=0, padx=5, pady=5)
        closing_time_entry = ttk.Entry(crud_options_frame)
        closing_time_entry.grid(row=4, column=1, padx=5, pady=5)

        rating_label = ttk.Label(crud_options_frame, text="Rating:")
        rating_label.grid(row=5, column=0, padx=5, pady=5)
        rating_entry = ttk.Entry(crud_options_frame)
        rating_entry.grid(row=5, column=1, padx=5, pady=5)

        average_price_label = ttk.Label(crud_options_frame, text="Average Price:")
        average_price_label.grid(row=6, column=0, padx=5, pady=5)
        average_price_entry = ttk.Entry(crud_options_frame)
        average_price_entry.grid(row=6, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_restaurant)
        create_button.grid(row=7, columnspan=2, padx=5, pady=5)
    elif entity_name == "Drivers":
        driver_name_label = ttk.Label(crud_options_frame, text="Driver Name:")
        driver_name_label.grid(row=1, column=0, padx=5, pady=5)
        driver_name_entry = ttk.Entry(crud_options_frame)
        driver_name_entry.grid(row=1, column=1, padx=5, pady=5)

        driver_phone_label = ttk.Label(crud_options_frame, text="Driver Phone Number:")
        driver_phone_label.grid(row=2, column=0, padx=5, pady=5)
        driver_phone_entry = ttk.Entry(crud_options_frame)
        driver_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        driver_email_label = ttk.Label(crud_options_frame, text="Driver Email:")
        driver_email_label.grid(row=3, column=0, padx=5, pady=5)
        driver_email_entry = ttk.Entry(crud_options_frame)
        driver_email_entry.grid(row=3, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_driver)
        create_button.grid(row=4, columnspan=2, padx=5, pady=5)
    elif entity_name == "Payments":
        payment_id_label = ttk.Label(crud_options_frame, text="Payment ID:")
        payment_id_label.grid(row=1, column=0, padx=5, pady=5)
        payment_id_entry = ttk.Entry(crud_options_frame)
        payment_id_entry.grid(row=1, column=1, padx=5, pady=5)
        order_id_label = ttk.Label(crud_options_frame, text="Order ID:")
        order_id_label.grid(row=1, column=0, padx=5, pady=5)
        order_id_entry = ttk.Entry(crud_options_frame)
        order_id_entry.grid(row=1, column=1, padx=5, pady=5)
        amount_label = ttk.Label(crud_options_frame, text="Amount:")
        amount_label.grid(row=2, column=0, padx=5, pady=5)
        amount_entry = ttk.Entry(crud_options_frame)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        payment_date_label = ttk.Label(crud_options_frame, text="Payment Date:")
        payment_date_label.grid(row=3, column=0, padx=5, pady=5)
        payment_date_entry = ttk.Entry(crud_options_frame)
        payment_date_entry.grid(row=3, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_payment)
        create_button.grid(row=4, columnspan=2, padx=5, pady=5)
    elif entity_name == "Customer Address":
        cid_label = ttk.Label(crud_options_frame, text="Customer ID:")
        cid_label.grid(row=1, column=0, padx=5, pady=5)
        cid_entry = ttk.Entry(crud_options_frame)
        cid_entry.grid(row=1, column=1, padx=5, pady=5)

        street_num_label = ttk.Label(crud_options_frame, text="Street Number:")
        street_num_label.grid(row=2, column=0, padx=5, pady=5)
        street_num_entry = ttk.Entry(crud_options_frame)
        street_num_entry.grid(row=2, column=1, padx=5, pady=5)

        street_name_label = ttk.Label(crud_options_frame, text="Street Name:")
        street_name_label.grid(row=3, column=0, padx=5, pady=5)
        street_name_entry = ttk.Entry(crud_options_frame)
        street_name_entry.grid(row=3, column=1, padx=5, pady=5)

        city_label = ttk.Label(crud_options_frame, text="City:")
        city_label.grid(row=4, column=0, padx=5, pady=5)
        city_entry = ttk.Entry(crud_options_frame)
        city_entry.grid(row=4, column=1, padx=5, pady=5)

        state_label = ttk.Label(crud_options_frame, text="State:")
        state_label.grid(row=5, column=0, padx=5, pady=5)
        state_entry = ttk.Entry(crud_options_frame)
        state_entry.grid(row=5, column=1, padx=5, pady=5)

        zip_code_label = ttk.Label(crud_options_frame, text="Zip Code:")
        zip_code_label.grid(row=6, column=0, padx=5, pady=5)
        zip_code_entry = ttk.Entry(crud_options_frame)
        zip_code_entry.grid(row=6, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_address)
        create_button.grid(row=7, columnspan=2, padx=5, pady=5)
    elif entity_name == "Restaurant Address":
        rid_label = ttk.Label(crud_options_frame, text="Restaurant ID:")
        rid_label.grid(row=1, column=0, padx=5, pady=5)
        rid_entry = ttk.Entry(crud_options_frame)
        rid_entry.grid(row=1, column=1, padx=5, pady=5)

        street_num_label = ttk.Label(crud_options_frame, text="Street Number:")
        street_num_label.grid(row=2, column=0, padx=5, pady=5)
        street_num_entry = ttk.Entry(crud_options_frame)
        street_num_entry.grid(row=2, column=1, padx=5, pady=5)

        street_name_label = ttk.Label(crud_options_frame, text="Street Name:")
        street_name_label.grid(row=3, column=0, padx=5, pady=5)
        street_name_entry = ttk.Entry(crud_options_frame)
        street_name_entry.grid(row=3, column=1, padx=5, pady=5)

        city_label = ttk.Label(crud_options_frame, text="City:")
        city_label.grid(row=4, column=0, padx=5, pady=5)
        city_entry = ttk.Entry(crud_options_frame)
        city_entry.grid(row=4, column=1, padx=5, pady=5)

        state_label = ttk.Label(crud_options_frame, text="State:")
        state_label.grid(row=5, column=0, padx=5, pady=5)
        state_entry = ttk.Entry(crud_options_frame)
        state_entry.grid(row=5, column=1, padx=5, pady=5)

        zip_code_label = ttk.Label(crud_options_frame, text="Zip Code:")
        zip_code_label.grid(row=6, column=0, padx=5, pady=5)
        zip_code_entry = ttk.Entry(crud_options_frame)
        zip_code_entry.grid(row=6, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_restaurant_address)
        create_button.grid(row=7, columnspan=2, padx=5, pady=5)

    elif entity_name == "History":
        cid_label = ttk.Label(crud_options_frame, text="Customer ID:")
        cid_label.grid(row=1, column=0, padx=5, pady=5)
        cid_entry = ttk.Entry(crud_options_frame)
        cid_entry.grid(row=1, column=1, padx=5, pady=5)

        order_id_label = ttk.Label(crud_options_frame, text="Order ID:")
        order_id_label.grid(row=2, column=0, padx=5, pady=5)
        order_id_entry = ttk.Entry(crud_options_frame)
        order_id_entry.grid(row=2, column=1, padx=5, pady=5)

        payment_id_label = ttk.Label(crud_options_frame, text="Payment ID:")
        payment_id_label.grid(row=3, column=0, padx=5, pady=5)
        payment_id_entry = ttk.Entry(crud_options_frame)
        payment_id_entry.grid(row=3, column=1, padx=5, pady=5)

        order_date_label = ttk.Label(crud_options_frame, text="Order Date:")
        order_date_label.grid(row=4, column=0, padx=5, pady=5)
        order_date_entry = ttk.Entry(crud_options_frame)
        order_date_entry.grid(row=4, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_history)
        create_button.grid(row=5, columnspan=2, padx=5, pady=5)
    
    elif entity_name == "Customer History Restaurant":
        history_id_label = ttk.Label(crud_options_frame, text="History ID:")
        history_id_label.grid(row=1, column=0, padx=5, pady=5)
        history_id_entry = ttk.Entry(crud_options_frame)
        history_id_entry.grid(row=1, column=1, padx=5, pady=5)

        rid_label = ttk.Label(crud_options_frame, text="Restaurant ID:")
        rid_label.grid(row=2, column=0, padx=5, pady=5)
        rid_entry = ttk.Entry(crud_options_frame)
        rid_entry.grid(row=2, column=1, padx=5, pady=5)

        create_button = ttk.Button(crud_options_frame, text="Create", command=create_customer_history)
        create_button.grid(row=3, columnspan=2, padx=5, pady=5)

def read_entities(entity_name):
    if entity_name == "Customers":
        customers = database_manager.read_customers()
        display_data(customers, "Customer ID", "Customer Name", "Customer Email", "Customer Phone", "Customer Subscription")
    elif entity_name == "Orders":
        orders = database_manager.read_orders()
        display_data(orders, "Customer ID", "Restaurant ID", "Driver ID", "Order Date", "ETA", "Total Amount", "Order Status")
    elif entity_name == "Restaurants":
        restaurants = database_manager.read_restaurants()
        display_data(restaurants, "Restaurant Name", "Food Type", "Opening Time", "Closing Time", "Rating", "Average Time")
    elif entity_name == "Drivers":
        drivers = database_manager.read_drivers()
        display_data(drivers, "Driver Name", "Phone Number", "Driver Email")
    elif entity_name == "Payments":
        payments = database_manager.read_payments()
        display_data(payments, "Order ID", "Amount", "Payment Date")
    elif entity_name == "Customer Address":
        addresses = database_manager.read_addresses()
        display_data(addresses, "Customer ID", "Street Number", "Street Name", "City", "State", "ZIP code")
    elif entity_name == "Restaurant Address":
        r_addresses = database_manager.read_restaurant_addresses()
        display_data(r_addresses, "Restaurant ID", "Street Number", "Street Name", "City", "State", "ZIP code")
    elif entity_name == "History":
        histories = database_manager.read_history()
        display_data(histories, "History ID", "Customer ID", "Order ID", "Payment ID", "Order Date")
    elif entity_name == "Customer History Restaurant":
        customer_histories = database_manager.read_customer_history_restaurant()
        display_data(customer_histories, "History ID", "Restaurant ID")
def delete_entity(entity_name):
    if entity_name == "Customers":
        customer_id = int(customer_id_entry.get())
        database_manager.delete_customer(customer_id)
    elif entity_name == "Orders":
        order_id = int(order_id_entry.get())
        database_manager.delete_order(order_id)
    elif entity_name == "Payments":
        payment_id = int(payment_id_entry.get())
        database_manager.delete_payment(payment_id)
    elif entity_name == "History":
        history_id = int(history_id_entry.get())
        database_manager.delete_history(history_id)
    elif entity_name == "Customer Address":
        address_id = int(address_id_entry.get())
        database_manager.delete_customer_address(address_id)
    elif entity_name == "Restaurant Address":
        restaurant_address_id = int(restaurant_address_id_entry.get())
        database_manager.delete_restaurant_address(restaurant_address_id)
    elif entity_name == "Customer History Restaurant":
        customer_history_id = int(customer_history_id_entry.get())
        database_manager.delete_customer_history_restaurant(customer_history_id)

def update_entity(entity_name):
    if entity_name == "Customers":
        customer_id = int(customer_id_entry.get())
        name = customer_name_entry.get()
        email = customer_email_entry.get()
        phone = customer_phone_entry.get()
        subscription = customer_subscription_entry.get()
        database_manager.update_customer(customer_id, name, email, phone, subscription)
    
    elif entity_name == "Orders":
        order_id = int(order_id_entry.get())
        cid = int(order_cid_entry.get())
        restaurant_id = int(order_restaurant_id_entry.get())
        driver_id = int(order_driver_id_entry.get())
        order_date = order_date_entry.get()
        eta = order_eta_entry.get()
        total_amount = float(order_amount_entry.get())
        order_status = order_status_entry.get()
        database_manager.update_order(order_id, cid, restaurant_id, driver_id, order_date, eta, total_amount, order_status)
    
    elif entity_name == "Restaurants":
        restaurant_id = int(restaurant_id_entry.get())
        name = restaurant_name_entry.get()
        ftype = food_type_entry.get()
        otime = opening_time_entry.get()
        ctime = closing_time_entry.get()
        rating = float(rating_entry.get())
        aprice = float(average_price_entry.get())
        database_manager.update_restaurant(restaurant_id, name, ftype, otime, ctime, rating, aprice)
    
    elif entity_name == "Drivers":
        driver_id = int(driver_id_entry.get())
        name = driver_name_entry.get()
        phone = driver_phone_entry.get()
        email = driver_email_entry.get()
        database_manager.update_driver(driver_id, name, phone, email)
    
    elif entity_name == "Payments":
        payment_id = int(payment_id_entry.get())
        order_id = int(payment_order_id_entry.get())
        amount = float(payment_amount_entry.get())
        payment_date = payment_date_entry.get()
        database_manager.update_payment(payment_id, order_id, amount, payment_date)
    
    elif entity_name == "History":
        history_id = int(history_id_entry.get())
        cid = int(history_cid_entry.get())
        order_id = int(history_order_id_entry.get())
        payment_id = int(history_payment_id_entry.get())
        order_date = history_order_date_entry.get()
        database_manager.update_history(history_id, cid, order_id, payment_id, order_date)
    
    elif entity_name == "Customer Address":
        address_id = int(address_id_entry.get())
        cid = int(address_cid_entry.get())
        street_num = street_number_entry.get()
        street_name = street_name_entry.get()
        city = city_entry.get()
        state = state_entry.get()
        zip_code = zip_code_entry.get()
        database_manager.update_customer_address(address_id, cid, street_num, street_name, city, state, zip_code)
    
    elif entity_name == "Restaurant Address":
        restaurant_address_id = int(restaurant_address_id_entry.get())
        rid = int(restaurant_address_rid_entry.get())
        street_num = restaurant_street_number_entry.get()
        street_name = restaurant_street_name_entry.get()
        city = restaurant_city_entry.get()
        state = restaurant_state_entry.get()
        zip_code = restaurant_zip_code_entry.get()
        database_manager.update_restaurant_address(restaurant_address_id, rid, street_num, street_name, city, state, zip_code)
    
    elif entity_name == "Customer History Restaurant":
        customer_history_id = int(customer_history_id_entry.get())
        history_id = int(customer_history_history_id_entry.get())
        rid = int(customer_history_rid_entry.get())
        database_manager.update_customer_history_restaurant(customer_history_id, history_id, rid)


def show_table_selection_frame():
    table_selection_frame.pack(fill=tk.BOTH, expand=True)

    table_label = ttk.Label(table_selection_frame, text="Select a table:")
    table_label.grid(row=0, column=0, padx=5, pady=5)

    table_combobox = ttk.Combobox(table_selection_frame, values=["Customers", "Orders", "Restaurants", ...])
    table_combobox.grid(row=0, column=1, padx=5, pady=5)

    select_table_button = ttk.Button(table_selection_frame, text="Select", command=lambda: show_crud_options(table_combobox.get()))
    select_table_button.grid(row=1, columnspan=2, padx=5, pady=5)

def show_crud_options(selected_table):
    table_selection_frame.pack_forget()
    crud_options_frame.pack(fill=tk.BOTH, expand=True)
    table_label = ttk.Label(crud_options_frame, text=f"Selected Table: {selected_table}")
    table_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    create_button = ttk.Button(crud_options_frame, text="Create", command=lambda: create_entity(selected_table))
    create_button.grid(row=1, column=0, padx=5, pady=5)
    read_button = ttk.Button(crud_options_frame, text="Read", command=lambda: read_entities(selected_table))
    read_button.grid(row=1, column=1, padx=5, pady=5)
    update_button = ttk.Button(crud_options_frame, text="Update", command=lambda: update_entity(selected_table))
    update_button.grid(row=2, column=0, padx=5, pady=5)
    delete_button = ttk.Button(crud_options_frame, text="Delete", command=lambda: delete_entity(selected_table))
    delete_button.grid(row=2, column=1, padx=5, pady=5)  
    back_button = ttk.Button(crud_options_frame, text="Back", command=show_table_selection_frame)
    back_button.grid(row=3, columnspan=2, padx=5, pady=5)     

def display_data(data, *column_names):
    listbox.delete(0, END)
    for x in data:
        listbox.insert(END, ''.join(str(value) for value in x))


            
root = Tk()
root.title("Doordash Database Management")
table_selection_frame = ttk.Frame(root)
crud_options_frame = ttk.Frame(root)
table_selection_frame.pack(fill=tk.BOTH, expand=True)
crud_options_frame.pack(fill=tk.BOTH, expand=True)
crud_options_frame.pack_forget()

root.mainloop()
