'''

Yasna: salam ostad, vaqt bekhair
ta injaye project drost pish raftam va ghabele ghabool hast?


APM: salam bale kheyli awli ahsant
fght b README.md ba gpt ya komake khodeton description khob ezafe konid for use later

Yasna: salam bale, ezafe karkam, man ta farda proje ro dar sorat takmili az nazar shoma baraye moasese email mikonam


'''

import tkinter as tk
from tkinter import messagebox, ttk
from Model import Customer, Account, Transaction
from Core import AdminPanel
from Utils import add_placeholder
from sqlalchemy import func


color = "#BFEFFF"
color_f1 = "#483D8B"
color_save = "#6495ED"
color_back = "#DC143C"
color_search = "#68228B"
color_select = "#458B74"
color_back_dashboard = "#B22222"


class AdminGUI:

    def __init__(self, bank_system):
        self.bank= bank_system
        self.root = tk.Tk()
        self.root.title("Bank Management System")
        self.default_width = 500
        self.default_height = 500
        self.set_window_size(self.default_width, self.default_height)
        self.root.configure(bg=color)
        self.show_login_window()
        self.root.mainloop()


    def set_window_size(self, width, height):
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)


    def reset_window_size(self):
        self.set_window_size(self.default_width, self.default_height)


    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def search_customer_and_select_account(self, next_step_callback, step=1, customer=None):
        self.clear()

        # --------Step:1 | Search / Retrieve Customer---------------------------
        if step == 1:
            self.set_window_size(500, 300)

            tk.Label(self.root, text="Search Customer", font=("arial", 21, "bold"), bg=color, fg=color_f1).pack(pady=10)

            tk.Label(self.root, text="Name:", font=("arial", 12, "bold"), bg=color, fg="blue").place(x=90, y=75)
            name_ent = tk.Entry(self.root, justify="center")
            name_ent.place(x=150, y=80, width=200, height=21)

            tk.Label(self.root, text="Email:", font=("arial", 12, "bold"), bg=color, fg="blue").place(x=90, y=115)
            email_ent = tk.Entry(self.root, justify="center")
            email_ent.place(x=150, y=120, width=200, height=21)

            # ---------- Search ----------
            def search():
                name = name_ent.get().strip()
                email = email_ent.get().strip()
                if not name or not email:
                    messagebox.showwarning("Warning", "Please enter both name and email.")
                    return

                session = self.bank.session

                cust = session.query(Customer).filter(
                    func.lower(Customer.name) == name.lower(),
                    func.lower(Customer.email) == email.lower()
                ).first()

                if not cust:
                    messagebox.showerror("Error", "Customer not found!")
                    return

                # open the second page
                next_step_callback(step=2, customer=cust)

            # ---------- Buttons ----------
            tk.Button(self.root, text="Search", command=search, bg=color_search, fg="white").place(x=230, y=180, width=80)
            tk.Button(self.root, text="Back", command=self.show_dashboard, bg=color_back).place(x=90, y=180, width=80)

            return

        # --------Step:2 | Show Customer's Accounts---------------------------
        if step == 2:
            self.set_window_size(500, 490)

            tk.Label(self.root, text=f"Accounts of {customer.name}", font=("Arial", 18, "bold"), fg=color_f1, bg=color).pack(pady=10)

            accounts_list = tk.Listbox(self.root)
            accounts_list.place(x=20, y=60, width=460, height=300)

            # adding the accounts to the list
            for acc in customer.accounts:
                accounts_list.insert(tk.END, f"{acc.id}  |  {acc.type}  |  Balance: {acc.balance}")

            def select_account():
                try:
                    index = accounts_list.curselection()[0]
                    acc = customer.accounts[index]
                    # open the third page
                    next_step_callback(step=3, customer=customer, account=acc)
                except:
                    messagebox.showerror("Error", "Select an account.")

            # ---------- Button ----------
            tk.Button(self.root, text="Select Account", bg=color_select, fg="white", command=select_account).place(x=220, y=400, width=100)
            tk.Button(self.root, text="Back", bg=color_back,
                      command=lambda: self.search_customer_and_select_account(next_step_callback, step=1)).place(x=50,y=400,width=80)

            return


    def show_login_window(self):
        self.clear()
        tk.Label(self.root, text="Admin Login", font=("Arial", 25, "bold"), bg=color, fg="#F08080").pack(pady=70)
        tk.Label(self.root, text="Username", font=("Arial", 12, "bold"), bg=color, fg="#191970").place(x=201, y=150)
        self.username_entry = tk.Entry(self.root, justify="center")
        self.username_entry.place(x=180, y=189)
        tk.Label(self.root, text="Password", font=("Arial", 12, "bold"), bg=color, fg="#191970").place(x=201, y=240)
        self.password_entry = tk.Entry(self.root, show="*", justify="center")
        self.password_entry.place(x=180, y=279)
        tk.Button(self.root, text="Login", bg="blue", fg="white", command=self.login).pack(pady=139)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # For demo, hardcoded admin credentials
        if username == "Yasna" and password == "246246":
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")


    def show_dashboard(self):
        self.reset_window_size()

        self.clear()

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold"), bg=color, fg=color_f1).pack(pady=20)

        tk.Button(self.root, text="Create Customer", width=20, command=self.open_create_customer).pack(pady=10)
        tk.Button(self.root, text="Create Account", width=20, command=self.open_create_account).pack(pady=10)
        tk.Button(self.root, text="Check Balance", width=20, command=self.open_check_balance).pack(pady=10)
        tk.Button(self.root, text="Deposit", width=20, command=self.open_deposit).pack(pady=10)
        tk.Button(self.root, text="Withdraw", width=20, command=self.open_withdraw).pack(pady=10)
        tk.Button(self.root, text="Transfer", width=20, command=self.open_transfer).pack(pady=10)
        tk.Button(self.root, text="Transactions", width=20, command=self.show_transactions).pack(pady=10)

        tk.Button(self.root, text="Logout", width=20, command=self.show_login_window).pack(pady=30)


    def open_create_customer(self):
        self.clear()

        tk.Label(self.root, text="Create Customer", font=("arial",21,"bold"), bg=color, fg=color_f1).pack(pady=20)

        # ---------- Mandatory Fields ----------
        tk.Label(self.root, text="Name:", font=("arial",15,"bold"), bg= color, fg="blue").place(x=90,y=90)
        name_ent = tk.Entry(self.root, justify="center")
        name_ent.place(x= 220, y=95, width=200, height=21)

        tk.Label(self.root, text="Email:", font=("arial",15,"bold"), bg= color, fg="blue").place(x=90,y=135)
        email_ent = tk.Entry(self.root, justify="center")
        email_ent.place(x= 220, y=140, width=200, height=21)

        # ---------- Optional Field ----------
        tk.Label(self.root, text="Age:", font=("arial", 15, "bold"), bg=color, fg="blue").place(x=90, y=180)
        age_ent = tk.Entry(self.root, justify="center")
        age_ent.place(x=220, y=185, width=200, height=21)
        add_placeholder(age_ent, "Optional")

        tk.Label(self.root, text="Phone:", font=("arial", 15, "bold"), bg=color, fg="blue").place(x=90, y=225)
        phone_ent = tk.Entry(self.root, justify="center")
        phone_ent.place(x=220, y=230, width=200, height=21)
        add_placeholder(phone_ent, "Optional")

        tk.Label(self.root, text="Address:", font=("arial", 15, "bold"), bg=color, fg="blue").place(x=90, y=270)
        address_ent = tk.Entry(self.root, justify="center")
        address_ent.place(x=220, y=275, width=200, height=21)
        add_placeholder(address_ent, "Optional")

        # ---------- Submit ----------
        def submit():
            name = name_ent.get()
            email = email_ent.get()
            age = age_ent.get()
            phone = phone_ent.get()
            address = address_ent.get()

            # optional
            age = int(age) if age and age != "Optional" else None
            phone = int(phone) if phone and phone != "Optional" else None
            address = address if address and address != "Optional" else None

            try:
                self.bank.create_customer(name, email, age, phone, address)
                messagebox.showinfo("Success", f"Customer created!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # ---------- Button ----------
        tk.Button(self.root, text="Create", command=submit, bg=color_save).place(x=220, y=360, width=80)
        tk.Button(self.root, text="Back", command=self.show_dashboard, bg=color_back).place(x=90, y=360, width=80)


    def open_create_account(self):
        self.clear()
        self.set_window_size(855, 450)

        tk.Label(self.root, text="Create Account", font=("arial", 21, "bold"), bg=color, fg=color_f1).place(x=20, y=15)

        # --------------------------- Search/Retrieve Customer ---------------------------
        tk.Label(self.root, text="Enter customer name:", font=("arial", 12, "bold"), bg=color, fg="blue").place(x=20, y=75)
        search_name_ent = tk.Entry(self.root, justify="center")
        search_name_ent.place(x=210, y=77, width=150, height=21)

        tk.Label(self.root, text="Enter customer email:", font=("arial", 12, "bold"), bg=color, fg="blue").place(x=20, y=110)
        search_email_ent = tk.Entry(self.root, justify="center")
        search_email_ent.place(x=210, y=112, width=150, height=21)

        result_list = tk.Listbox(self.root)
        result_list.place(x=20, y=160, width=400, height=170)

        def search_customer():
            result_list.delete(0, tk.END)

            name_query = search_name_ent.get().strip()
            email_query = search_email_ent.get().strip()

            if not name_query or not email_query:
                return

            session = self.bank.session

            customer = session.query(Customer).filter(
                Customer.name == name_query,
                Customer.email == email_query
            ).first()

            if customer:
                result_list.insert(tk.END, f"{customer.id} | {customer.name} | {customer.email}")
            else:
                result_list.insert(tk.END, "No matching customer found!")

        # ---------- Search Button ----------
        tk.Button(self.root, text="Search", command=search_customer, bg=color_search, fg="white").place(x=160, y=350, width=80)

        # --------------------------- Create Account ---------------------------
        # ---------- Customer ID ----------
        tk.Label(self.root, text="Customer ID:", font=("arial", 13, "bold"), bg=color, fg="blue").place(x=510, y=75)
        customer_ent = tk.Entry(self.root, justify="center")
        customer_ent.place(x=630, y=77, width=200, height=21)

        # ---------- Account Type ----------
        tk.Label(self.root, text="Account Type:", font=("arial", 13, "bold"), bg=color, fg="blue").place(x=510, y=115)
        account_type_var = tk.StringVar()
        account_type_combo = ttk.Combobox(self.root, textvariable=account_type_var, state="readonly")
        account_type_combo['values'] = ("Checking Account", "Savings Account", "Business Account",
                                        "Fixed Deposit", "Foreign Currency Account", "Crypto Account")
        account_type_combo.current(0)
        account_type_combo.place(x=630, y=117, width=200, height=21)

        # ---------- Initial Balance ----------
        tk.Label(self.root, text="Initial Balance:", font=("arial", 13, "bold"), bg=color, fg="blue").place(x=510, y=155)
        balance_ent = tk.Entry(self.root, justify="center")
        balance_ent.place(x=630, y=157, width=200, height=21)
        add_placeholder(balance_ent,"0.0")

        # ---------- PIN ----------
        tk.Label(self.root, text="PIN:", font=("arial", 13, "bold"), bg=color, fg="blue").place(x=510, y=195)
        pin_ent = tk.Entry(self.root, justify="center", show="*")
        pin_ent.place(x=630, y=197, width=200, height=21)

        # ---------- Submit ----------
        def submit():
            try:
                customer_id = int(customer_ent.get())
                account_type = account_type_var.get()
                balance = float(balance_ent.get())
                pin = pin_ent.get()

                account = self.bank.create_account(customer_id, account_type, balance, pin)
                messagebox.showinfo("Success", f"Account created!\nCard Number: {account.card_number}")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for Customer ID and Balance.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def back_to_dashboard():
            self.reset_window_size()
            self.show_dashboard()

        # ---------- Buttons ----------
        tk.Button(self.root, text="Create", command=submit, bg=color_save).place(x=550, y=350, width=80)
        tk.Button(self.root, text="Back", command=back_to_dashboard, bg=color_back).place(x=660, y=350, width=80)


    def open_check_balance(self, step=1, customer=None, account=None):
        self.clear()
        if step < 3:
            # --------Step:1,2 | search_customer_and_select_account---------------------------
            self.search_customer_and_select_account(next_step_callback=self.open_check_balance, step=step, customer=customer)
            return

        # --------Step:3 | Show Balance---------------------------
        if step == 3:
            self.set_window_size(500, 300)

            tk.Label(self.root, text="Account Balance", font=("Arial", 21, "bold"), bg=color, fg=color_f1).pack(pady=20)

            tk.Label(self.root, text=f"Account ID: {account.id}", font=("Arial", 12, "bold"), bg=color).pack(pady=5)

            tk.Label(self.root, text=f"Type: {account.type}", font=("Arial", 12, "bold"), bg=color).pack(pady=5)

            tk.Label(self.root, text=f"Balance: {account.balance}", font=("Arial", 12, "bold"), fg="forestgreen",
                     bg=color).pack(pady=10)

            # ---------- Buttons ----------
            tk.Button(self.root, text="Back to Accounts", bg=color_back,
                      command=lambda: self.open_check_balance(step=2, customer=customer)).pack(pady=15)
            tk.Button(self.root, text="Dashboard", bg=color_back_dashboard, command=self.show_dashboard, fg="white").pack()

            return


    def open_deposit(self, step=1, customer=None, account=None):
        if step < 3:
            # --------Step:1,2 | search_customer_and_select_account---------------------------
            self.search_customer_and_select_account(next_step_callback=self.open_deposit, step=step, customer=customer)

            return

        # --------Step:3 | Deposit---------------------------
        self.clear()
        self.set_window_size(500, 300)

        tk.Label(self.root, text=f"Deposit to Account with ID: {account.id}", font=("Arial", 21, "bold"), bg=color,
                 fg=color_f1).pack(pady=20)

        tk.Label(self.root, text=f"Current Balance: {account.balance}", font=("Arial", 12, "bold"), fg="chartreuse4",
                 bg=color).pack(pady=5)

        tk.Label(self.root, text="Deposit Amount:", font=("Arial", 12, "bold"), bg=color, fg="blue").pack(pady=10)
        amount_ent = tk.Entry(self.root, justify="center")
        amount_ent.pack()

        # ---------- Submit Deposit ----------
        def submit_deposit():
            try:
                amount = float(amount_ent.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")

                self.bank.deposit(account.id, amount)
                messagebox.showinfo("Success", f"{amount} deposited successfully!")
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # ---------- Buttons ----------
        tk.Button(self.root, text="Deposit", command=submit_deposit, bg="#008B8B", width=8).pack(pady=9)
        tk.Button(self.root, text="Back", command=lambda: self.open_deposit(step=2, customer=customer), bg=color_back, width=8).pack(pady=5)
        tk.Button(self.root, text="Dashboard", bg=color_back_dashboard, command=self.show_dashboard, fg="white").pack(pady=5)

        return


    def open_withdraw(self, step=1, customer=None, account=None):
        if step < 3:
            # --------Step:1,2 | search_customer_and_select_account---------------------------
            self.search_customer_and_select_account(next_step_callback=self.open_withdraw, step=step, customer=customer)

            return

        # --------Step:3 | Withdraw---------------------------
        self.clear()
        self.set_window_size(500, 500)

        tk.Label(self.root, text=f"Withdraw from Account ID: {account.id}", font=("Arial", 21, "bold"), bg=color,
                 fg=color_f1).pack(pady=20)

        tk.Label(self.root, text=f"Current Balance: {account.balance}", font=("Arial", 12, "bold"), fg="chartreuse4",
                 bg=color).pack(pady=5)

        tk.Label(self.root, text="Withdraw Amount:", font=("Arial", 12, "bold"), bg=color, fg="blue").pack(pady=10)
        amount_ent = tk.Entry(self.root, justify="center")
        amount_ent.pack()

        # ---------- Submit Withdraw ----------
        def submit_withdraw():
            try:
                amount = float(amount_ent.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")

                # ---------- Check balance ----------
                if amount > account.balance:
                    raise ValueError("Insufficient balance!")

                # ---------- Perform withdrawal ----------
                self.bank.withdraw(account.id, amount)
                messagebox.showinfo("Success", f"{amount} withdrawn successfully!")
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # ---------- Buttons ----------
        tk.Button(self.root, text="Withdraw", command=submit_withdraw, bg="#008B8B", width=8).pack(pady=9)
        tk.Button(self.root, text="Back", command=lambda: self.open_withdraw(step=2, customer=customer),
                  bg=color_back, width=8).pack(pady=5)
        tk.Button(self.root, text="Dashboard", bg=color_back_dashboard, command=self.show_dashboard, fg="white").pack(pady=5)

        return


    def open_transfer(self, step=1, customer=None, from_account=None, to_account=None):
        if step < 3:
            # --------Step:1,2 | search_customer_and_select_account---------------------------
            def _callback(step, customer, account=None, **kw):
                return self.open_transfer(step=step, customer=customer, from_account=account)

            self.search_customer_and_select_account(next_step_callback=_callback, step=step,customer=customer)
            return

        # --------Step:3 | Select 'TO' Account---------------------------
        if step == 3 and from_account and not to_account:
            self.clear()
            self.set_window_size(500, 460)

            tk.Label(self.root, text=f"Select Destination Account", font=("arial", 21, "bold"),
                     bg=color, fg=color_f1).pack(pady=10)

            tk.Label(self.root, text=f"Source Account: {from_account.id}  | Balance: {from_account.balance}",
                     font=("arial", 12, "bold"), fg="blue", bg=color).pack(pady=5)

            tk.Label(self.root, text="Choose an account to transfer TO", font=("arial", 12,"bold"),
                     bg=color, fg="black").pack(pady=10)

            # ---------- Frame for Listbox ----------
            frame = tk.Frame(self.root)
            frame.pack(pady=10)

            dest_accounts = [acc for acc in customer.accounts if acc.id != from_account.id]
            accounts_list = tk.Listbox(frame, height=len(dest_accounts), width=55, justify="center")
            accounts_list.pack()

            # ---------- List of destination accounts ----------
            self.to_account_candidates = []

            for acc in customer.accounts:
                if acc.id != from_account.id:
                    accounts_list.insert(tk.END, f"{acc.id} | {acc.type} | Balance: {acc.balance}")

                    # Store the true object for safe indexing
                    self.to_account_candidates.append(acc)

            # ---------- Select Destination ----------
            def select_destination():
                try:
                    index = accounts_list.curselection()[0]
                    to_acc = self.to_account_candidates[index]

                    self.open_transfer(step=4, customer=customer, from_account=from_account, to_account=to_acc)

                except:
                    messagebox.showerror("Error", "Please select a destination account.")

            # ---------- Buttons ----------
            tk.Button(self.root, text="Select", bg=color_select, fg="white", width=8, command=select_destination).pack(pady=5)
            tk.Button(self.root, text="Back", bg=color_back, width=8,
                      command=lambda: self.open_transfer(step=2, customer=customer)).pack(pady=5)

            return

        # -------- Step:4 | Enter Transfer Amount and Execute ---------------------------
        if step == 4 and from_account and to_account:
            self.clear()
            self.set_window_size(500, 333)

            tk.Label(self.root, text=f"Transfer from {from_account.id} to {to_account.id}", font=("arial", 21, "bold"),
                     bg=color, fg=color_f1).pack(pady=20)
            tk.Label(self.root, text=f"Source Balance: {from_account.balance}", font=("arial", 12, "bold"),
                     fg="chartreuse4", bg=color).pack(pady=5)

            tk.Label(self.root, text="Transfer Amount:", font=("Arial", 12, "bold"), bg=color, fg="blue").pack(pady=10)
            amount_ent = tk.Entry(self.root, justify="center")
            amount_ent.pack()

            # ---------- Submit Transfer ----------
            def submit_transfer():
                try:
                    amount = float(amount_ent.get())
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                    if amount > from_account.balance:
                        raise ValueError("Insufficient balance!")

                    # ---------- Transfer ----------
                    self.bank.transfer(from_account.id, to_account.id, amount)
                    messagebox.showinfo("Success", f"{amount} transferred successfully!")
                    self.show_dashboard()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            # ---------- Buttons ----------
            tk.Button(self.root, text="Transfer", command=submit_transfer, bg="#008B8B", width=8).pack(pady=9)
            tk.Button(self.root, text="Back",
                      command=lambda: self.open_transfer(step=3, customer=customer, from_account=from_account),
                      bg=color_back, width=8).pack(pady=5)
            tk.Button(self.root, text="Dashboard", bg=color_back_dashboard, fg="white", command=self.show_dashboard).pack(pady=5)


    def show_transactions(self, step=1, customer=None):
        # -------- Step:1 | Find Customer ---------------------------
        if step == 1:
            # callback will be called by the shared search function when a customer is chosen
            def _callback(step, customer, account=None, **kw):
                # we only need the customer for transactions view
                return self.show_transactions(step=2, customer=customer)

            # reuse the shared multi-step selector (search_customer_and_select_account)
            # this will show search -> accounts and call _callback with the chosen customer
            self.search_customer_and_select_account(next_step_callback=_callback, step=step, customer=customer)
            return

        # -------- Step 2 | Show Transaction List ---------------------------
        if step == 2:
            self.clear()
            self.set_window_size(700, 500)

            tk.Label(self.root, text=f"Transactions of {customer.name}", font=("Arial", 20, "bold"),
                bg=color, fg=color_f1).pack(pady=15)

            # ---------- Scrollable Frame (Canvas + Scrollbar) ----------
            container = tk.Frame(self.root, bg=color)
            container.pack(fill="both", expand=True, pady=10)

            canvas = tk.Canvas(container, bg=color, highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scrollbar.set)

            inner = tk.Frame(canvas, bg=color)
            canvas.create_window((0, 0), window=inner, anchor="nw")

            inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            # ---------- Fetch Accounts + Transactions ----------
            accounts = self.bank.get_accounts_of_customer(customer.id)

            all_transactions = []
            for acc in accounts:
                txs = self.bank.get_transactions_by_account(acc.id)
                all_transactions.extend(txs)

            # ---------- If No Transactions ----------
            if not all_transactions:
                tk.Label(inner, text="No transactions found.",
                    font=("Arial", 14), bg=color, fg="red").pack(pady=20)

            # ---------- Render Cards ----------
            else:
                for tx in all_transactions:

                    card = tk.Frame(inner, bg="#1f2c39", bd=1, relief="ridge", padx=10, pady=6)
                    card.pack(fill="x", pady=6, padx=10)

                    # Title: TYPE + AMOUNT
                    tk.Label(card, text=f"{tx.type.upper()}  —  {tx.amount}", fg="white", bg="#1f2c39",
                        font=("Arial", 12, "bold")).pack(anchor="w")

                    # From → To (for transfer)
                    if tx.from_account_id or tx.to_account_id:
                        tk.Label(card,text=f"From {tx.from_account_id} → To {tx.to_account_id}",
                                 fg="#c0c0c0", bg="#1f2c39",font=("Arial", 10)).pack(anchor="w")
                    else:
                        tk.Label(card, text=f"Account: {tx.account_id}",fg="#c0c0c0", bg="#1f2c39",
                            font=("Arial", 10)).pack(anchor="w")

                    # Description (optional)
                    if tx.description:
                        tk.Label(card,text=tx.description,fg="#c0c0c0", bg="#1f2c39",
                            font=("Arial", 10)).pack(anchor="w")

                    # Date
                    tk.Label(card, text=f"Date: {tx.created_at}",fg="orange", bg="#1f2c39",
                             font=("Arial", 9)).pack(anchor="w")

            # ---------- Buttons ----------
            tk.Button(self.root, text="Back", width=10, bg=color_back,
                      command=lambda: self.show_transactions(step=1)).pack(pady=5)
            tk.Button(self.root, text="Dashboard", width=10, bg=color_back_dashboard, fg="white",
                command=self.show_dashboard).pack(pady=5)

            return


