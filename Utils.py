import hashlib
import random
import numpy as np

#----------Password----------
#---hash password---
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

#---check password---
def check_password(hashed_password,plain_password):
    if hashed_password == hash_password(plain_password):
        return True
    else:
        return False

#----------Create 16 digits card number----------
def generate_card_number():
    digits = np.random.randint(0,10,16)
    card_number = ''.join(digits.astype(str))
    return card_number

#----------Placeholder----------
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="grey")

    # after focus and writing
    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg="black")

    # before focus
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

