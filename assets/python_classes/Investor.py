from .Client import *
from .Bank import *
from .Transactions import *
from contracts.bank import bank_approval, bank_clear

class Investor(Client):
    def __init__(self, name, algorand_account):
        super().__init__(name, algorand_account)
        self.transactions = Transactions()

    def create_bank(self, bank_name):
        if self.bank == None:
            investor_addr = self.get_addr()
            investor_pk = self.get_pk()
            # transactions.deploy method should return id and addr of newly created bank [id, addr]
            l = self.transactions.deploy(investor_pk, bank_name, bank_approval, bank_clear, 2, 1, 1, 1)
            self.bank = Bank(bank_name, investor_addr, investor_pk, l[0], l[1])
        else:
            print("\nInvestor {} has already created a bank called {}".format(self.name ,self.bank.get_name()))

    def fund_bank(self, amount):
        investor_addr = self.get_addr()
        investor_pk = self.get_pk()
        note = "Investor {} makes a {} micro algos payment transaction to {}".format(self.get_name(), amount, self.bank.get_name())
        print("\n" + note)
        val = self.transactions.payment_txn(investor_addr, investor_pk, amount, self.bank.get_bank_addr(), note)
        if val:
            print("Payment transaction was successful!")
        else:
            print("Payment transaction failed!")

    def update_bank(self):
        investor_addr = self.get_addr()
        investor_pk = self.get_pk()
        appr_bytes = self.transactions.compile_program(bank_approval())
        clear_bytes = self.transactions.compile_program(bank_clear())
        bank_id = self.bank.get_bank_id()
        note = "The investor {} updates the bank {}".format(self.get_name(), self.bank.get_name())
        print("\n" + note)
        val = self.transactions.call_app(investor_addr, investor_pk, 4, bank_id, note, appr_bytes, clear_bytes)
        if val:
            print("Bank was successfully updated")
        else:
            print("Bank update operation failed!")
    
    def delete_bank(self):
        investor_addr = self.get_addr()
        investor_pk = self.get_pk()
        bank_id = self.bank.get_bank_id()
        note = "The investor {} deletes the bank {}".format(self.name, self.bank.get_name())
        print("\n" + note)
        val = self.transactions.call_app(investor_addr, investor_pk, 5, bank_id, note)
        if val:
            print("Bank was successfully deleted")
            self.bank = None
        else:
            print("Bank delete operation failed!")