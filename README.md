# bank_management_system_Yasna_Tajedini

This Repository is for Bank Management 
Fanavari Co Project Summer 2025 
Supervisor  : Ali Pilehvar Meibody


---
# Description

A simple bank management application built with Python.  
It allows an admin to manage customers, bank accounts, and transactions using a graphical interface (Tkinter) and SQLAlchemy for database operations.

**Features include:**
- Customer management: create and store customers with optional details (age, phone, address)
- Account management: create accounts, check balances, deposit, withdraw, and transfer money
- Transaction management: record and view deposit, withdrawal, and transfer transactions
- Secure PIN storage with SHA-256 hashing



---
# Structure

Bank_Management/
│
├── Core/
│   └── AdminPanel.py        # Business logic and core operations
│
├── Model/
│   └── models.py            # Database models (Customer, Account, Transaction)
│
├── Admin_GUI.py             # Graphical User Interface (Tkinter)
├── Database.py              # Database setup and session management
├── Utils.py                 # Helper functions (hashing, placeholders, etc.)
├── Main.py                  # Application entry point
└── README.md

----
# Requirements

- Python 3.8+
- Libraries:
 `tkinter`
 `sqlalchemy`
 `numpy`

----
<h1 align="left">Installation </h1>

Install required libraries via pip:
```bash
pip install sqlalchemy numpy
```




----
<h1 align="left">How To Use </h1>


1. Run the application by executing `Main.py`.
2. Login with the admin credentials:  
   - Username: Yasna  
   - Password: 246246
3. Use the admin dashboard to:  
   - Create a new customer  
   - Create a bank account for a customer  
   - Check account balances  
   - Deposit money into an account  
   - Withdraw money from an account  
   - Transfer money between accounts  
   - View all transactions of a customer
4. The system uses SQLite (`database.db`) by default.  
5. Account PINs are hashed with SHA-256 and account numbers are 16-digit random numbers.
6. GUI navigation steps:  
   - Step 1: Search and select customer  
   - Step 2: Choose the customer’s account  
   - Step 3: Perform the selected operation (deposit, withdraw, transfer, etc.)
