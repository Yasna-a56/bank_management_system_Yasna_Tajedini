'''
Yasna: salam vaqteton bekhair
soal ---> bebakhshid baraye "relationships" bayad do tarafe dar "classs" vared beshan? 
          masala ham dar class customer(Base): ---> accounts = relationship("Account", back_populates="customers")
          a ham dar class account(Base): ---> customer = relationship("Customer", back_populates="accounts")
          ya faqat yeki az classha be relationships(ertebat table ha) eshare kone kafie?


APM: salam , bale kamelan dorost neveshtid inja relationship ro .
shayad bazi az tabel ha nakahn relationship vali baraye mohkam kari khobe b hamashon add krd
moafagh abshid


Yasna: mamnonam

'''



from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Database import Base


#-------Customers-------
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    #---optional items---
    age = Column(Integer, nullable=True)
    phone = Column(Integer, nullable=True)
    address = Column(String, nullable=True)

    # -------relationships-------
    accounts = relationship("Account", back_populates="customers")
    transactions = relationship("Transaction", back_populates="customers")

#-------Accounts-------
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)  # mojodi , 00
    type = Column(String, default="standard")  # 'standard', 'foreign', 'crypto'
    pin = Column(String, nullable=False)  # pin kodom account ro khod kon

    customer_id = Column(Integer, ForeignKey("customers.id"))

    #-------relationships-------
    customers = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="accounts")

#-------Transactions-------
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # transfer --> deposit, withdraw
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))

    #---transfer accounts---

    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    # -------relationships-------
    customers = relationship("Customer", back_populates="transactions")
    accounts = relationship("Account", back_populates="transactions")


