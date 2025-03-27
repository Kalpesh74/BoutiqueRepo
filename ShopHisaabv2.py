# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 20:39:24 2025

@author: darshu
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
global item_name_combobox, quantity_entry, price_entry  


class ShopHisaabApp:
    def __init__(self, root):
        # Define main window
        self.root = root
        self.root.title("Shop-Hisaab")
        self.root.geometry("900x550")
        self.root.configure(bg="#F8F9FA")  # Light theme background
        
        # Sidebar Frame
        self.sidebar = tk.Frame(root, bg="#2C3E50", width=220, height=550)
        self.sidebar.pack(side="left", fill="y")
        self.db = self.init_firebase()
        icon_paths = {
        "Dashboard": "icons/dashboard.png",
        "Sales": "icons/sales.png",
        "Inventory": "icons/inventory.png",
        "Expenses": "icons/expenses.png"
    }
        icons = {name: self.load_icon(path) for name, path in icon_paths.items()}
        
        # Sidebar Buttons
        buttons = ["Dashboard", "Sales", "Inventory", "Expenses"]
        for btn in buttons:
            frame = tk.Frame(self.sidebar, bg="#34495E", height=50)
            frame.pack(fill="x", pady=5, padx=10)
            icon_label = tk.Label(frame, image=icons[btn] if icons[btn] else None, bg="#34495E")
            icon_label.pack(side="left", padx=10)
            button = tk.Button(frame, text=btn, font=("Arial", 12, "bold"), bg="#34495E", fg="white", bd=0, height=2, relief="flat", activebackground="#1ABC9C")
            button.pack(side="left", fill="x", expand=True)
            if btn == "Inventory":
                button.config(command=lambda: self.show_inventory())
            if btn == "Sales":
                button.config(command=lambda: self.show_sales())
                
    
        # Main Content Frame
        main_content = tk.Frame(root, bg="#FFFFFF", width=680, height=550)
        main_content.pack(side="right", fill="both", expand=True)

        
    # Load Icons with Error Handling
    def load_icon(self,path):
        if os.path.exists(path):
            return ImageTk.PhotoImage(Image.open(path).resize((24, 24)))
        else:
            print(f"Warning: Icon not found at {path}")
            return None  # Placeholder if icon is missing

    
    # Initialize Firebase
    def init_firebase(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("shophisaab-firebase-adminsdk.json")  # Replace with actual path
            firebase_admin.initialize_app(cred)
        return firestore.client()
    
    












# def show_inventory():
#     for widget in main_content.winfo_children():
#         widget.destroy()
    
#     tk.Label(main_content, text="Inventory Management", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#2C3E50").pack(pady=15)
    
#     # Inventory Table
#     columns = ("Item Name", "Quantity", "Price", "Date Added")
#     inventory_table = ttk.Treeview(main_content, columns=columns, show="headings")
#     for col in columns:
#         inventory_table.heading(col, text=col)
#         inventory_table.column(col, width=150, anchor="center")
#     inventory_table.pack(pady=10, padx=20, fill="both", expand=True)
    
#     # Add Item Form
#     form_frame = tk.Frame(main_content, bg="#ECF0F1", padx=20, pady=10)
#     form_frame.pack(pady=10)
    
#     tk.Label(form_frame, text="Item Name:", bg="#ECF0F1", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
#     item_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
#     item_name_entry.grid(row=0, column=1, padx=5, pady=5)
    
#     tk.Label(form_frame, text="Quantity:", bg="#ECF0F1", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
#     quantity_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
#     quantity_entry.grid(row=1, column=1, padx=5, pady=5)
    
#     tk.Label(form_frame, text="Price:", bg="#ECF0F1", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
#     price_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
#     price_entry.grid(row=2, column=1, padx=5, pady=5)
    
#     # Fetch Inventory
#     def fetch_inventory():
#         for row in inventory_table.get_children():
#             inventory_table.delete(row)
#         docs = db.collection("inventory").stream()
#         for doc in docs:
#             data = doc.to_dict()
#             date_added = data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             inventory_table.insert("", "end", values=(data["name"], data["quantity"], data["base_price"], date_added))
    
#     # Add, Update, Delete Item Functions
#     def add_item():
#         item_name = item_name_entry.get().strip()
#         quantity = quantity_entry.get().strip()
#         price = price_entry.get().strip()
#         if not item_name or not quantity or not price:
#             messagebox.showerror("Error", "All fields are required!")
#             return
#         db.collection("inventory").add({"name": item_name, "quantity": int(quantity), "price": float(price), "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
#         fetch_inventory()
    
#     def delete_item():
#         selected_item = inventory_table.selection()
#         if not selected_item:
#             messagebox.showerror("Error", "Please select an item to delete!")
#             return
#         item_values = inventory_table.item(selected_item, "values")
#         docs = db.collection("inventory").where("name", "==", item_values[0]).stream()
#         for doc in docs:
#             doc.reference.delete()
#         fetch_inventory()
    
#     def update_item():
#         fetch_inventory()
    
#     # Buttons
#     button_frame = tk.Frame(form_frame, bg="#ECF0F1")
#     button_frame.grid(row=3, column=0, columnspan=2, pady=10)
    
#     tk.Button(button_frame, text="Add Item", command=add_item, bg="#28A745", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)
#     tk.Button(button_frame, text="Update Item", command=update_item, bg="#FFC107", fg="black", font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5)
#     tk.Button(button_frame, text="Delete Item", command=delete_item, bg="#DC3545", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=0, column=2, padx=5)
    
#     fetch_inventory()






































# # def show_sales():
# #     for widget in main_content.winfo_children():
# #         widget.destroy()

# #     tk.Label(main_content, text="Sales Management", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#2C3E50").pack(pady=15)

# #     # Sales Table
# #     columns = ("Item Name", "Quantity", "Selling Price", "Total", "Date")
# #     sales_table = ttk.Treeview(main_content, columns=columns, show="headings")
# #     for col in columns:
# #         sales_table.heading(col, text=col)
# #         sales_table.column(col, width=150, anchor="center")
# #     sales_table.pack(pady=10, padx=20, fill="both", expand=True)

# #     # Fetch sales records
# #     def fetch_sales():
# #         for row in sales_table.get_children():
# #             sales_table.delete(row)
# #         docs = db.collection("sales").stream()
# #         for doc in docs:
# #             data = doc.to_dict()
# #             date_added = data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# #             sales_table.insert("", "end", values=(data["name"], data["quantity"], data["sale_price"], data["total"], date_added))

# #     # # Sales Form
# #     form_frame = tk.Frame(main_content, bg="#ECF0F1", padx=20, pady=10)
# #     form_frame.pack(pady=10)

# #     # Fetch inventory items for dropdown
# #     def fetch_inventory_items():
# #         inventory_items = []
# #         docs = db.collection("inventory").stream()
# #         for doc in docs:
# #             data = doc.to_dict()
# #             inventory_items.append(data["name"])
# #         return inventory_items

# #     tk.Label(form_frame, text="Item Name:", bg="#ECF0F1", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
# #     item_name_combobox = ttk.Combobox(form_frame, font=("Arial", 12), width=18, state="readonly")
# #     item_name_combobox.grid(row=0, column=1, padx=5, pady=5)
# #     item_name_combobox["values"] = fetch_inventory_items()

# #     tk.Label(form_frame, text="Quantity:", bg="#ECF0F1", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
# #     quantity_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
# #     quantity_entry.grid(row=1, column=1, padx=5, pady=5)

# #     tk.Label(form_frame, text="Selling Price:", bg="#ECF0F1", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
# #     price_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
# #     price_entry.grid(row=2, column=1, padx=5, pady=5)

# #     # Function to add a sale
# #     def add_sale():
# #         item_name = item_name_combobox.get().strip()
# #         quantity = quantity_entry.get().strip()
# #         sale_price = price_entry.get().strip()

# #         if not item_name or not quantity or not sale_price:
# #             messagebox.showerror("Error", "All fields are required!")
# #             return

# #         # Fetch item from inventory
# #         docs = db.collection("inventory").where("name", "==", item_name).stream()
# #         item_doc = None
# #         for doc in docs:
# #             item_doc = doc
# #             break

# #         if not item_doc:
# #             messagebox.showerror("Error", "Item not found in inventory!")
# #             return

# #         item_data = item_doc.to_dict()
# #         if int(quantity) > item_data["quantity"]:
# #             messagebox.showerror("Error", "Not enough stock available!")
# #             return

# #         total_price = int(quantity) * float(sale_price)

# #         # Deduct from inventory
# #         new_quantity = item_data["quantity"] - int(quantity)
# #         item_doc.reference.update({"quantity": new_quantity})

# #         # Add sale record
# #         db.collection("sales").add({
# #             "name": item_name,
# #             "quantity": int(quantity),
# #             "sale_price": float(sale_price),
# #             "total": total_price,
# #             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         })

# #         fetch_sales()

# #     # Buttons
# #     button_frame = tk.Frame(form_frame, bg="#ECF0F1")
# #     button_frame.grid(row=3, column=0, columnspan=2, pady=10)

# #     tk.Button(button_frame, text="Add Sale", command=add_sale, bg="#28A745", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)

# #     fetch_sales()
  
# #     def add_sale():
# #         item_name = item_name_entry.get().strip()
# #         quantity = quantity_entry.get().strip()
# #         price = price_entry.get().strip()
# #         if not item_name or not quantity or not price:
# #             messagebox.showerror("Error", "All fields are required!")
# #             return
    
# #         # Fetch item from inventory
# #         docs = db.collection("inventory").where("name", "==", item_name).stream()
# #         item_doc = None
# #         for doc in docs:
# #             item_doc = doc
# #             break
    
# #         if not item_doc:
# #             messagebox.showerror("Error", "Item not found in inventory!")
# #             return
    
# #         item_data = item_doc.to_dict()
# #         if int(quantity) > item_data["quantity"]:
# #             messagebox.showerror("Error", "Not enough stock available!")
# #             return
    
# #         total_price = int(quantity) * float(price)
    
# #         # Deduct from inventory
# #         new_quantity = item_data["quantity"] - int(quantity)
# #         item_doc.reference.update({"quantity": new_quantity})
    
# #         # Add sale record
# #         db.collection("sales").add({
# #             "name": item_name,
# #             "quantity": int(quantity),
# #             "price": float(price),
# #             "total": total_price,
# #             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         })
# #         fetch_sales()
    
    
    
# #     def delete_sale():
# #         selected_item = sales_table.selection()
# #         if not selected_item:
# #             messagebox.showerror("Error", "Please select a sale to delete!")
# #             return
    
# #         item_values = sales_table.item(selected_item, "values")
# #         docs = db.collection("sales").where("name", "==", item_values[0]).where("date", "==", item_values[4]).stream()
# #         for doc in docs:
# #             doc.reference.delete()
    
# #         # Restore inventory
# #         inventory_docs = db.collection("inventory").where("name", "==", item_values[0]).stream()
# #         for inv_doc in inventory_docs:
# #             inv_doc.reference.update({"quantity": firestore.Increment(int(item_values[1]))})
    
# #         fetch_sales()
    
# #     def update_sale():
# #         fetch_sales()


# # Run application
# root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopHisaabApp(root)
    root.mainloop()





