'''
Yasna: salam vaqteton bekhair
soal ---> baraye code "numpy", behtare ke tooye file "Utils" bashe ya
mitoone ke be soorat tab dar tab dar "Core" bashe?

soal2 ---> vaqti ke dar "if" ma naboode 'account' va ya 'customer' ro be soorate 
"raise Exception" migim hatman bayad "print" ham beshe? va chera?



'''



from Database import get_session
from Model import Account, Customer, Transaction
from Utils import hash_password, check_password
import numpy as np


class AdminPanel:
    def __init__(self):
        self.session = get_session()



    def create_customer(self, name, email, age=None, phone=None, address=None):

        customer = Customer(name = name, email = email,
                            age = age, phone = phone, address = address)   #optional items

        self.session.add(customer)
        self.session.commit()
        print(f'Customer {name} created successfully!')

        return customer



    def create_account(self, customer_id, account_type, balance, pin):
        customer=self.session.get(Customer, customer_id)

        if not customer:
            '''
            way 1:
            print(f'Customer with id {customer_id} not found!')
            '''
            # way 2
            raise Exception(f'Customer with id {customer_id} not found!')



        def generate_card_number():   #^^^#
            digits = np.random.randint(0,10,16)
            card_number = ''.join(digits.astype(str))
            return card_number
        print(generate_card_number())

        hashed_pin = hash_password(pin)

        account = Account(balance=balance, type=account_type, pin=hashed_pin)

        self.session.add(account)
        self.session.commit()

        return account



    def show_balance(self,account_id):
        account=self.session.get(Account,account_id)

        if not account:
            '''
            way 1:
            print(f'Account with id {account_id} not found!')
            '''
            # way 2
            raise Exception(f'Account with id {account_id} not found!')

        balance= account.balance

        print(f'Your balance is {balance}')
        return balance



    def deposit(self,account_id,amount):
        account=self.session.get(Account,account_id)
        if not account:
            '''
            way 1:
            print(f'Account with id {account_id} not found!')
            '''
            # way 2
            raise Exception(f'Account with id {account_id} not found')

        account.balance += amount

        self.session.commit()
        return account



    def withdraw(self,account_id,amount):
        account=self.session.get(Account,account_id)
        if not account:
            '''
            way 1:
            print(f'Account with id {account_id} not found!')
            '''
            # way 2
            raise Exception(f'Account with id {account_id} not found!')

        balance = account.balance

        if amount <= balance:
            return 'Your account balance is not sufficient'

        balance -= amount

        self.session.commit()

        return account



    def transfer(self,from_account_id,to_account_id,amount):
        account_from = self.session.get(Transaction, from_account_id)
        account_to = self.session.get(Transaction, to_account_id)

        if amount <= 0:
            raise Exception("Amount must be positive!")

        if account_from.balance < amount:
            return "Insufficient balance!"

        account_from.balance -= amount
        account_to.balance += amount

        self.session.commit()

        return "Transfer completed successfully!"

    def show_transaction(self, account_id):
        account = self.session.get(Account, account_id)

        if not account:
            raise Exception(f"Account with id {account_id} not found!")

        transactions = (
            self.session.query(Transaction)
            .filter_by(account_id=account_id)
            .order_by(Transaction.created_at.desc())
            .all()
            )

        for t in transactions:
            print(f"{t.id} | {t.type} | {t.amount} | {t.created_at}")

        return transactions



