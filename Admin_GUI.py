import tkinter as tk
from tkinter import messagebox, ttk
from Core import AdminPanel


color = "#BFEFFF"
color_f1 = "#483D8B"
color_save = "#6495ED"
color_back = "#DC143C"


class AdminGUI:

    def __init__(self, bank_system):
        self.bank= bank_system
        self.root = tk.Tk()
        self.root.title("Bank Management System")
        self.root.geometry('500x500')
        self.root.resizable(False,False)
        self.root.configure(bg=color)
        self.show_login_window()
        self.root.mainloop()



    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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
        self.clear()

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold"), bg=color, fg=color_f1).pack(pady=20)

        tk.Button(self.root, text="Create Customer", width=20, command=self.open_create_customer).pack(pady=10)
        tk.Button(self.root, text="Create Account", width=20, command=self.open_create_account).pack(pady=10)
        tk.Button(self.root, text="Check Balance", width=20, command=self.open_check_balance).pack(pady=10)
        tk.Button(self.root, text="Deposit", width=20, command=self.open_deposit).pack(pady=10)
        tk.Button(self.root, text="Withdraw", width=20, command=self.open_withdraw).pack(pady=10)
        tk.Button(self.root, text="Transfer", width=20, command=self.open_transfer).pack(pady=10)
        tk.Button(self.root, text="Transactions", width=20, command=self.open_transactions).pack(pady=10)

        tk.Button(self.root, text="Logout", width=20, command=self.show_login_window).pack(pady=30)


    def open_create_customer(self):
        self.clear()

        tk.Label(self.root, text="Create Customer", font=("arial",21,"bold"), bg=color, fg=color_f1).pack(pady=20)

        # Obligatory
        tk.Label(self.root, text="Name:", font=("arial",15,"bold"), bg= color, fg="blue").place(x=90,y=90)
        name_ent = tk.Entry(self.root, justify="center")
        name_ent.place(x= 220, y=95, width=200, height=21)

        tk.Label(self.root, text="Email:", font=("arial",15,"bold"), bg= color, fg="blue").place(x=90,y=135)
        email_ent = tk.Entry(self.root, justify="center")
        email_ent.place(x= 220, y=140, width=200, height=21)

        #optional
        def add_placeholder(entry, text):
            entry.insert(0, text)
            entry.config(fg="grey")

            # before focus
            def on_focus_in(event):
                if entry.get() == text:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            # after focus
            def on_focus_out(event):
                if entry.get() == "":
                    entry.insert(0, text)
                    entry.config(fg="grey")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

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
                messagebox.showinfo("Success", "Customer created!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Submit Button
        tk.Button(self.root, text="Create", command=submit, bg=color_save).place(x=220, y=360, width=80)
        tk.Button(self.root, text="Back", command=self.show_dashboard, bg=color_back).place(x=90, y=360, width=80)







