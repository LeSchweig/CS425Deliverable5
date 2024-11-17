import tkinter as tk
from tkinter import ttk, messagebox
import database_manager

class DatabaseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DoorDash Database Management")
        self.root.geometry("800x600")
        
        #initialize frames
        self.table_selection_frame = ttk.Frame(self.root)
        self.crud_options_frame = ttk.Frame(self.root)
        self.data_frame = ttk.Frame(self.root)
        
        # entires dictionary
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
                
            getattr(database_manager, f"create_{table_name.lower()}")(**values)
            messagebox.showinfo("Success", f"Created new {table_name} record")
            self.read_entities(table_name)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_entities(self, table_name):
        try:
            data = getattr(database_manager, f"read_{table_name.lower()}")()
            self.data_frame.pack(fill=tk.BOTH, expand=True)
            self.display_data(data, table_name)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_data(self, data, table_name):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, " | ".join(self.tables[table_name]))
        self.listbox.insert(tk.END, "-" * 80)
        
        for row in data:
            self.listbox.insert(tk.END, " | ".join(str(item) for item in row))
    def get_selected_record_id(self):
    selection = self.listbox.curselection()
    if not selection:
        raise ValueError("Please select a record")
    record = self.listbox.get(selection[0])
    return record.split(" | ")[0] 

    def get_updated_values(self):
        values = {}
        for field, entry in self.entries.items():
            value = entry.get()
            if value:
                values[field] = self.validate_input(field, value)
        return values
    def update_entity(self, table_name):
        try:
            record_id = self.get_selected_record_id()
            values = self.get_updated_values()
            if not values:
                raise ValueError("No fields to update")
                
            getattr(database_manager, f"update_{table_name.lower()}")(record_id, **values)
            messagebox.showinfo("Success", "Record updated")
            self.read_entities(table_name)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def delete_entity(self, table_name):
        if messagebox.askyesno("Confirm Delete", "Are you sure?"):
            try:
                record_id = self.get_selected_record_id()
                getattr(database_manager, f"delete_{table_name.lower()}")(record_id)
                messagebox.showinfo("Success", "Record deleted")
                self.read_entities(table_name)  # Refresh display
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
