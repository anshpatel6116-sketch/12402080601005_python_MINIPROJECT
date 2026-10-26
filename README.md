# Canteen Food Ordering System

## 1. Project Overview

The Canteen Food Ordering System is a Python-based mini project designed to simplify food ordering in a college canteen. It provides a graphical user interface where users can view food items, select quantities, add items to a cart, calculate the total bill, and generate a receipt.

The project uses Python, Tkinter, Object-Oriented Programming (OOP), dictionaries, and MySQL database connectivity.

## 2. Objectives

- To make food ordering simple and user-friendly.
- To display food items with their prices.
- To calculate the total amount automatically.
- To store customer orders in a database.
- To generate a bill receipt after successful ordering.
- To demonstrate Python programming concepts through a mini project.

## 3. Technologies Used

- **Programming Language:** Python
- **GUI:** Tkinter
- **Database:** MySQL
- **Database Connector:** mysql-connector-python
- **Concepts:** OOP, Classes, Objects, Dictionaries, Exception Handling, Database Operations

## 4. Main Features

1. Display food items and prices.
2. Select food items and quantities.
3. Add items to the shopping cart.
4. Remove items from the cart.
5. Clear the cart.
6. Calculate the total bill.
7. Enter the customer's name.
8. Select a payment method.
9. Save orders in the MySQL database.
10. Generate and save a bill receipt.

## 5. Project Files

- `main.py` – Contains the main Python application and GUI.
- `setup.sql` – Contains SQL commands for database setup, if provided.
- `requirements.txt` – Lists the required Python packages.
- `README.md` – Contains project information and instructions.

## 6. Installation Requirements

Install Python 3 and MySQL Server on your computer.

Install the required Python package using Terminal:

```bash
python3 -m pip install mysql-connector-python
```

## 7. Database Configuration

The application uses a MySQL database named `canteen_db`.

Update the database configuration in `main.py` with your MySQL username and password:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "canteen_db"
}
```

Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL password.

The MySQL server must be running before starting the application.

## 8. How to Run the Project

1. Open the project folder in VS Code.
2. Make sure Python and MySQL are installed.
3. Configure the MySQL username and password in `main.py`.
4. Open the VS Code Terminal.
5. Install the required package.
6. Run the following command:

```bash
python3 main.py
```

7. The application window will open.
8. Select food items and quantities.
9. Add the items to the cart.
10. Enter the customer name and select a payment method.
11. Confirm the order and generate the bill.

## 9. Sample Output

**Food Menu**

| Food Item | Price |
|---|---:|
| Veg Sandwich | ₹50 |
| Cheese Sandwich | ₹70 |
| Veg Burger | ₹80 |
| French Fries | ₹60 |
| Samosa | ₹25 |
| Masala Dosa | ₹90 |
| Idli | ₹45 |
| Cold Coffee | ₹60 |
| Tea | ₹15 |
| Water Bottle | ₹20 |

**Example Bill**

- Veg Burger × 2 = ₹160
- Samosa × 2 = ₹50
- Tea × 1 = ₹15

**Total Amount: ₹225**

This is an illustrative example of the expected output.

## 10. Python Concepts Used

### Object-Oriented Programming

Classes such as `CanteenDatabase` and `CanteenApp` organize database operations and GUI functionality.

### Dictionaries

Dictionaries store food details such as item names, categories, prices, and quantities.

### Database Connectivity

MySQL stores menu information and customer order details.

### Exception Handling

Exception handling helps display errors when database operations fail.

### GUI Programming

Tkinter provides windows, buttons, labels, tables, and input fields.

## 11. Advantages

- Easy-to-use graphical interface.
- Automatic bill calculation.
- Organized food menu.
- Database storage of orders.
- Reduced manual calculation errors.
- Useful for demonstrating programming concepts.

## 12. Future Scope

- Online payment integration.
- Admin login and menu management.
- Food availability management.
- Order history and reports.
- Customer login system.
- Improved bill printing functionality.

## 13. Conclusion

The Canteen Food Ordering System demonstrates how Python, Tkinter, OOP, dictionaries, and MySQL can be combined to develop a basic food ordering application. It provides menu selection, cart management, automatic bill calculation, and order storage. This project helps students understand the practical application of programming and database concepts.
