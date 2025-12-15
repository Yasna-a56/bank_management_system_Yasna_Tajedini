from Database import get_session
from Model import Account, Customer, Transaction
from Utils import hash_password, check_password, generate_card_number
import numpy as np


class AdminPanel:
    def __init__(self):
        self.session = get_session()

    def get_accounts_of_customer(self, customer_id):
        """
        Return all bank accounts that belong to the given customer.
        """
        return self.session.query(Account).filter_by(customer_id=customer_id).all()


    def get_transactions_by_account(self, account_id):
        """
        Return all transactions related to the specified account, ordered from newest to oldest.
        """
        return (self.session.query(Transaction)
                .filter_by(account_id=account_id)
                .order_by(Transaction.created_at.desc())
                .all())


    def create_customer(self, name, email, age=None, phone=None, address=None):
        """
        Create a new customer: add the customer to the database
        and display confirmation.
        """

        customer = Customer(name = name, email = email,
                            age = age, phone = phone, address = address)   #optional items

        self.session.add(customer)
        self.session.commit()
        print(f'Customer {name} created successfully!')

        new_customer = self.session.query(Customer).filter_by(email=email).first()
        print("Created Customer:", new_customer)


        return customer


    def create_account(self, customer_id, account_type, balance, pin):
        """
        Create a new account for a customer: validate the customer,
        generate card number and hashed PIN, save the account, and return it.
        """

        customer=self.session.get(Customer, customer_id)

        if not customer:
            print(f'Customer with id {customer_id} not found!')
            raise Exception(f'Customer with id {customer_id} not found!')

        # card number
        card_number = generate_card_number()
        print(card_number)

        # pin
        hashed_pin = hash_password(pin)

        account = Account(balance=balance, type=account_type, pin=hashed_pin,
                          customer_id = customer_id, card_number=card_number)

        self.session.add(account)
        self.session.commit()

        return account


    def show_balance(self,account_id):
        """
        Retrieve and display the balance of a specific account:
        validate the account exists and return its current balance.
        """

        account=self.session.get(Account,account_id)

        if not account:
            print(f'Account with id {account_id} not found!')
            raise Exception(f'Account with id {account_id} not found!')

        balance= account.balance

        print(f'Your balance is {balance}')

        return balance


    def deposit(self,account_id,amount):
        """
        Deposit a specified amount into an account: validate the
        account, increase its balance, and record a deposit transaction.
        """

        account=self.session.get(Account,account_id)

        if not account:
            print(f'Account with id {account_id} not found!')
            raise Exception(f'Account with id {account_id} not found')

        account.balance += amount

        # Transaction Recording
        transaction = Transaction(amount=amount,
                                  type="deposit",
                                  description="Deposit into account",
                                  customer_id=account.customer_id,
                                  account_id=account.id)

        self.session.add(transaction)
        self.session.commit()

        return account


    def withdraw(self,account_id,amount):
        """
        Perform a withdrawal from an account: verify the account,
        check sufficient balance, update the balance, and record
        a withdrawal transaction.
        """

        account=self.session.get(Account,account_id)

        if not account:
            print(f'Account with id {account_id} not found!')
            raise Exception(f'Account with id {account_id} not found!')

        balance = account.balance

        if amount > balance:
            return 'Your account balance is not sufficient'

        balance -= amount

        # Transaction Recording
        transaction = Transaction(amount=amount,
                                  type="withdraw",
                                  description="Withdraw from account",
                                  customer_id=account.customer_id,
                                  account_id=account.id)

        self.session.add(transaction)
        self.session.commit()

        return account


    def transfer(self,from_account_id,to_account_id,amount):
        """
        Transfer a specific amount of money from one account to another.
        Validates both accounts, checks balance availability,
        updates both account balances, and records the transfer
        as a transaction in the database.
        """

        account_from = self.session.get(Account, from_account_id)
        account_to = self.session.get(Account, to_account_id)

        if not account_from or not account_to:
            raise Exception("One of the accounts not found!")

        if amount <= 0:
            raise Exception("Amount must be positive!")

        if account_from.balance < amount:
            return "Insufficient balance!"

        account_from.balance -= amount
        account_to.balance += amount

        # Transaction Recording
        transaction = Transaction(amount=amount,
                                  type="transfer",
                                  description="Transfer between accounts",
                                  customer_id=account_from.customer_id,
                                  account_id=account_from.id,
                                  from_account_id=account_from.id,
                                  to_account_id=account_to.id)

        self.session.add(transaction)
        self.session.commit()

        return "Transfer completed successfully!"


    def show_transaction(self, account_id):
        """
        Retrieve and return all transactions for a specific account.
        Results are ordered from newest to oldest.
        Also prints a simple summary of each transaction in the console.
        """

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

