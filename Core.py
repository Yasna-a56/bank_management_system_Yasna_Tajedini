'''
Yasna: salam vaqteton bekhair
soal ---> baraye code "numpy", behtare ke tooye file "Utils" bashe ya
mitoone ke be soorat tab dar tab dar "Core" bashe?

APM: Salam mitonid dar khode class Adminpanel estefade konid chon fght ye tabe koochike, 
vaghty tabe bishtar bozorgtar ya 3,4 khat eutils bnvisid


soal2 ---> vaqti ke dar "if" ma naboode 'account' va ya 'customer' ro be soorate 
"raise Exception" migim hatman bayad "print" ham beshe? va chera?

Bale baya dprint bashe, choon raise exception baraye oon customer namayesh dade mishe
print ( hala dar ayande mikhonid yechizi has bename logg va oonja shoma roo
server har az gahi negah mikonid (mesle printe) va mibinid ahan felan error
pish omde vase ch moshtari ee dar che ghesmati



Yasna: mamnoon



APM:
b nokatre tabeye create_account() dghat konid (dakhelesh comment gozashtam)
tabeye withdraw() sharte if ro eshtebah gozashtid
tabeye show_transaction() shoma bayad tooye deposit() withdraw() bayad y data varede table konid
bad to show_transaction() oon dataharo neshon bdid

baz harkoja ag soal dashtdi begid hatman
'''



from Database import get_session
from Model import Account, Customer, Transaction
from Utils import hash_password, check_password , generate_card_number
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
            print(f'Customer with id {customer_id} not found!')
            raise Exception(f'Customer with id {customer_id} not found!')
            
        # card number
        card_number = generate_card_number()
        print(card_number)

        #inja generate_card_number() 
        #bayad baid zakhire she tooye ye variable bad biad bere too Account
        
        # pin
        hashed_pin = hash_password(pin)

        #man ezafe kardam customer_id va hamchnin , 
        account = Account(balance=balance, type=account_type, pin=hashed_pin ,
                          customer_id = customer_id, card_number=card_number)

        self.session.add(account)
        self.session.commit()

        return account



    def show_balance(self,account_id):
        account=self.session.get(Account,account_id)

        if not account:
            print(f'Account with id {account_id} not found!')
            raise Exception(f'Account with id {account_id} not found!')

        balance= account.balance

        print(f'Your balance is {balance}')
        return balance



    def deposit(self,account_id,amount):
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











