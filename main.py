
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# -----------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "canteen_db"
}

# -----------------------------------------
# DEFAULT FOOD MENU (DICTIONARY)
# -----------------------------------------
DEFAULT_MENU = {
    1: {"name": "Veg Sandwich", "category": "Snacks", "price": 50.00},
    2: {"name": "Cheese Sandwich", "category": "Snacks", "price": 70.00},
    3: {"name": "Veg Burger", "category": "Fast Food", "price": 80.00},
    4: {"name": "French Fries", "category": "Fast Food", "price": 60.00},
    5: {"name": "Samosa", "category": "Snacks", "price": 25.00},
    6: {"name": "Masala Dosa", "category": "South Indian", "price": 90.00},
    7: {"name": "Idli", "category": "South Indian", "price": 45.00},
    8: {"name": "Cold Coffee", "category": "Beverages", "price": 60.00},
    9: {"name": "Tea", "category": "Beverages", "price": 15.00},
    10: {"name": "Water Bottle", "category": "Beverages", "price": 20.00}
}


# =========================================
# DATABASE CLASS
# =========================================
class CanteenDatabase:

    def connect(self):
        # Connect to MySQL server first and create database if needed
        server_config = {
            "host": DB_CONFIG["host"],
            "user": DB_CONFIG["user"],
            "password": DB_CONFIG["password"]
        }

        server_connection = mysql.connector.connect(**server_config)
        server_cursor = server_connection.cursor()

        server_cursor.execute(
            "CREATE DATABASE IF NOT EXISTS canteen_db"
        )

        server_cursor.close()
        server_connection.close()

        # Now connect to the project database
        return mysql.connector.connect(**DB_CONFIG)

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(60) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                available BOOLEAN DEFAULT TRUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                payment_method VARCHAR(30) NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                order_time DATETIME NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                item_id INT NOT NULL,
                item_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                line_total DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

        # Insert default menu only when menu is empty
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        count = cursor.fetchone()[0]

        if count == 0:
            for item_id, item in DEFAULT_MENU.items():
                cursor.execute("""
                    INSERT INTO menu_items
                    (item_id, name, category, price)
                    VALUES (%s, %s, %s, %s)
                """, (
                    item_id,
                    item["name"],
                    item["category"],
                    item["price"]
                ))

        connection.commit()
        cursor.close()
        connection.close()

    def get_menu(self):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT item_id, name, category, price
            FROM menu_items
            WHERE available = TRUE
            ORDER BY item_id
        """)

        menu = cursor.fetchall()

        cursor.close()
        connection.close()

        return menu

    def save_order(self, customer_name, payment_method, cart):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            total = sum(
                item["price"] * item["quantity"]
                for item in cart.values()
            )

            cursor.execute("""
                INSERT INTO orders
                (customer_name, payment_method, total, order_time)
                VALUES (%s, %s, %s, %s)
            """, (
                customer_name,
                payment_method,
                total,
                datetime.now()
            ))

            order_id = cursor.lastrowid

            for item_id, item in cart.items():
                subtotal = item["price"] * item["quantity"]

                cursor.execute("""
                    INSERT INTO order_items
                    (order_id, item_id, item_name, quantity,
                     unit_price, line_total)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    order_id,
                    item_id,
                    item["name"],
                    item["quantity"],
                    item["price"],
                    subtotal
                ))

            connection.commit()
            return order_id, total

        except Error:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()


# =========================================
# MAIN APPLICATION CLASS
# =========================================
class CanteenApp:

    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.cart = {}

        self.root.title("Canteen Food Ordering System")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#F2F5F7")

        title = tk.Label(
            root,
            text="CANTEEN FOOD ORDERING SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#234E70",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        main_frame = tk.Frame(root, bg="#F2F5F7", padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # -------- FOOD MENU --------
        menu_frame = tk.LabelFrame(
            main_frame,
            text="Food Menu",
            font=("Arial", 12, "bold"),
            padx=8,
            pady=8
        )
        menu_frame.pack(
            side="left", fill="both", expand=True, padx=5
        )

        self.menu_table = ttk.Treeview(
            menu_frame,
            columns=("ID", "Name", "Category", "Price"),
            show="headings",
            height=16
        )

        for column in ("ID", "Name", "Category", "Price"):
            self.menu_table.heading(column, text=column)

        self.menu_table.column("ID", width=45, anchor="center")
        self.menu_table.column("Name", width=145)
        self.menu_table.column("Category", width=105)
        self.menu_table.column("Price", width=75, anchor="e")

        self.menu_table.pack(fill="both", expand=True)

        tk.Label(
            menu_frame, text="Quantity:", font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 2))

        self.quantity_var = tk.StringVar(value="1")

        tk.Entry(
            menu_frame,
            textvariable=self.quantity_var,
            width=10
        ).pack(anchor="w")

        tk.Button(
            menu_frame,
            text="Add to Cart",
            command=self.add_to_cart,
            bg="#2E8B57",
            fg="white",
            padx=10,
            pady=6
        ).pack(anchor="w", pady=8)

        # -------- SHOPPING CART --------
        cart_frame = tk.LabelFrame(
            main_frame,
            text="Your Cart",
            font=("Arial", 12, "bold"),
            padx=8,
            pady=8
        )
        cart_frame.pack(
            side="right", fill="both", expand=True, padx=5
        )

        self.cart_table = ttk.Treeview(
            cart_frame,
            columns=("ID", "Name", "Qty", "Price", "Subtotal"),
            show="headings",
            height=16
        )

        for column in ("ID", "Name", "Qty", "Price", "Subtotal"):
            self.cart_table.heading(column, text=column)

        self.cart_table.column("ID", width=35, anchor="center")
        self.cart_table.column("Name", width=115)
        self.cart_table.column("Qty", width=45, anchor="center")
        self.cart_table.column("Price", width=65, anchor="e")
        self.cart_table.column("Subtotal", width=75, anchor="e")

        self.cart_table.pack(fill="both", expand=True)

        self.total_label = tk.Label(
            cart_frame,
            text="Total: Rs. 0.00",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack(anchor="e", pady=10)

        tk.Button(
            cart_frame,
            text="Remove Selected Item",
            command=self.remove_from_cart,
            bg="#C0392B",
            fg="white",
            pady=5
        ).pack(fill="x", pady=3)

        tk.Button(
            cart_frame,
            text="Clear Cart",
            command=self.clear_cart,
            pady=5
        ).pack(fill="x", pady=3)

        tk.Button(
            cart_frame,
            text="PLACE ORDER & GENERATE BILL",
            command=self.place_order,
            bg="#234E70",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=9
        ).pack(fill="x", pady=8)

        self.load_menu()

    # -------- LOAD MENU FROM DATABASE --------
    def load_menu(self):
        try:
            items = self.database.get_menu()

            for row in self.menu_table.get_children():
                self.menu_table.delete(row)

            for item in items:
                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        item["item_id"],
                        item["name"],
                        item["category"],
                        f'{float(item["price"]):.2f}'
                    )
                )

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load menu:\n{error}"
            )

    # -------- ADD ITEM TO CART --------
    def add_to_cart(self):
        selected = self.menu_table.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a food item first."
            )
            return

        try:
            quantity = int(self.quantity_var.get())

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Quantity",
                "Enter a whole number greater than zero."
            )
            return

        values = self.menu_table.item(selected[0], "values")

        item_id = int(values[0])
        name = values[1]
        price = float(values[3])

        if item_id in self.cart:
            self.cart[item_id]["quantity"] += quantity
        else:
            self.cart[item_id] = {
                "name": name,
                "price": price,
                "quantity": quantity
            }

        self.refresh_cart()

    # -------- REFRESH CART AND TOTAL --------
    def refresh_cart(self):
        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        total = 0

        for item_id, item in self.cart.items():
            subtotal = item["price"] * item["quantity"]
            total += subtotal

            self.cart_table.insert(
                "",
                "end",
                values=(
                    item_id,
                    item["name"],
                    item["quantity"],
                    f'{item["price"]:.2f}',
                    f"{subtotal:.2f}"
                )
            )

        self.total_label.config(text=f"Total: Rs. {total:.2f}")

    # -------- REMOVE ITEM FROM CART --------
    def remove_from_cart(self):
        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Select an item from your cart."
            )
            return

        values = self.cart_table.item(selected[0], "values")
        item_id = int(values[0])

        self.cart.pop(item_id, None)
        self.refresh_cart()

    # -------- CLEAR CART --------
    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart()

    # -------- PLACE ORDER AND GENERATE BILL --------
    def place_order(self):
        if not self.cart:
            messagebox.showwarning(
                "Empty Cart",
                "Please add food items to your cart first."
            )
            return

        order_window = tk.Toplevel(self.root)
        order_window.title("Confirm Order")
        order_window.geometry("350x280")
        order_window.resizable(False, False)

        tk.Label(
            order_window,
            text="Confirm Your Order",
            font=("Arial", 16, "bold")
        ).pack(pady=12)

        tk.Label(order_window, text="Customer Name:").pack()

        name_entry = tk.Entry(order_window, width=30)
        name_entry.pack(pady=5)

        tk.Label(order_window, text="Payment Method:").pack()

        payment_var = tk.StringVar(value="Cash")

        ttk.Combobox(
            order_window,
            textvariable=payment_var,
            values=["Cash", "UPI", "Card"],
            state="readonly",
            width=27
        ).pack(pady=5)

        def save_order():
            customer_name = name_entry.get().strip()
            payment_method = payment_var.get()

            if not customer_name:
                messagebox.showwarning(
                    "Missing Name",
                    "Please enter the customer name.",
                    parent=order_window
                )
                return

            try:
                order_id, total = self.database.save_order(
                    customer_name,
                    payment_method,
                    self.cart
                )

                order_time = datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

                bill = [
                    "       CANTEEN FOOD ORDERING SYSTEM",
                    "=" * 42,
                    f"Order ID: {order_id}",
                    f"Customer: {customer_name}",
                    f"Payment: {payment_method}",
                    f"Date: {order_time}",
                    "-" * 42,
                    f"{'Item':<18}{'Qty':>5}{'Amount':>12}",
                    "-" * 42
                ]

                for item in self.cart.values():
                    subtotal = item["price"] * item["quantity"]

                    bill.append(
                        f"{item['name'][:18]:<18}"
                        f"{item['quantity']:>5}"
                        f"{subtotal:>12.2f}"
                    )

                bill.extend([
                    "-" * 42,
                    f"TOTAL: Rs. {total:.2f}",
                    "=" * 42,
                    "       Thank you! Visit again."
                ])

                bill_text = "\n".join(bill)

                bill_window = tk.Toplevel(self.root)
                bill_window.title(f"Bill - Order {order_id}")
                bill_window.geometry("520x480")

                text_box = tk.Text(
                    bill_window,
                    font=("Courier New", 11),
                    wrap="none"
                )
                text_box.pack(
                    fill="both",
                    expand=True,
                    padx=10,
                    pady=10
                )

                text_box.insert("1.0", bill_text)
                text_box.config(state="disabled")

                def save_bill_file():
                    filename = f"bill_{order_id}.txt"

                    try:
                        with open(filename, "w", encoding="utf-8") as file:
                            file.write(bill_text)

                        messagebox.showinfo(
                            "Bill Saved",
                            f"Bill saved as {filename}",
                            parent=bill_window
                        )

                    except OSError as error:
                        messagebox.showerror(
                            "File Error",
                            str(error),
                            parent=bill_window
                        )

                tk.Button(
                    bill_window,
                    text="Save Bill as Text File",
                    command=save_bill_file
                ).pack(pady=5)

                self.cart.clear()
                self.refresh_cart()
                order_window.destroy()

                messagebox.showinfo(
                    "Order Successful",
                    f"Order #{order_id} saved successfully!"
                )

            except Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not save order:\n{error}",
                    parent=order_window
                )

        tk.Button(
            order_window,
            text="Confirm and Generate Bill",
            command=save_order,
            bg="#234E70",
            fg="white",
            pady=8
        ).pack(pady=15)


# =========================================
# START THE APPLICATION
# =========================================
def main():
    try:
        database = CanteenDatabase()
        database.create_tables()

        root = tk.Tk()
        CanteenApp(root, database)
        root.mainloop()

    except Error as error:
        messagebox.showerror(
            "Database Connection Error",
            "Could not connect to MySQL.\n\n"
            f"Details: {error}\n\n"
            "Check that MySQL is running and that "
            "your username and password are correct."
        )


if __name__ == "__main__":
    main()
