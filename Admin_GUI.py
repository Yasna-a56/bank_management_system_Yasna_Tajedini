import tkinter as tk
from tkinter import messagebox, ttk
from Core import AdminPanel

color = "#BFEFFF"
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
        self.username_entry = tk.Entry(self.root)
        self.username_entry.place(x=180, y=189)
        tk.Label(self.root, text="Password", font=("Arial", 12, "bold"), bg=color, fg="#191970").place(x=201, y=240)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.place(x=180, y=279)
        tk.Button(self.root, text="Login", bg="blue", fg="white", command=self.login).pack(pady=139)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # For demo, hardcoded admin credentials
        if username == "admin" and password == "1234":
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")


app = AdminGUI(None)

