from Database import Base, engine
from Model import Customer, Account, Transaction
from Core import AdminPanel
from Admin_GUI import AdminGUI

Base.metadata.create_all(engine)

admin_panel = AdminPanel()
app = AdminGUI(admin_panel)


