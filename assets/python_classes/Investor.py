from .RoleAbstract import *
from .Bank import *
from .Transactions import *
from contracts import *

class Investor(RoleAbstract):
    def __init__(self, person):
        self.person = person
        self.created_bank = None
        self.transactions = Transactions()
    
    def get_bank(self):
        return self.created_bank

    def create_bank(self, bank_name):
        if self.created_bank == None:
            investor_addr = self.get_account_address()
            investor_pk = self.get_account_pk()
            # transactions.deploy method should return id and addr of newly created bank [id, addr]
            l = self.transactions.deploy(self.get_name(), investor_pk, bank_name, bank_approval, bank_clear, 2, 1, 1, 1)
            self.created_bank = Bank(bank_name, investor_addr, investor_pk, l[0], l[1])
            """
            The created bank has an id and an account address, which requires a min of 0.1 Algo to be on the ledger
            In order for the bank to be fully functional, it is going to create 4 additional smart contracts
            Reference, Deposit, Withdraw, Transfer - each costing 0.1 Algo + 0.1 Algo funding. This equals 0.8 Algos
            Reference also has 2 byteslices as global storage, each costing 0.05 Algo to manage => 0.1 Algo 
            Each bank account smart contract created for a client replicates Reference => 0.1 Algo for account on ledger 
            and 0.1 Algo for global storage. This equals 0.2 Algo for each newly created bank account 
            For 3 bank accounts I will need 0.6 Algo.
            In this case, the total is 1.6 Algos. Just to make the number prettier I want a min of 2 Algos for initial funding of bank
            Every time you want to create more bank accounts or more additional smart contracts for the bank
            you have to make the calculations how much Algos does the bank need as additional funding
            Else transactions will fail because of lack of funds in the smart contract
            """
            if self.fund_bank(2000000):
                print("Investor successfully created and funded the bank with 2 Algos")
                return True
            else: 
                print("Something went wrong with the creation or funding of the bank! Please remember that the investor needs at least 2 Algos for funding!")
                return False
        else:
            print("\nInvestor {} has already created a bank called {}".format(self.get_name() ,self.created_bank.get_name()))
            return False

    def fund_bank(self, amount):
        if self.created_bank == None:
            print("The investor hasn't created a bank yet! Funding not possible")
            return False
        if amount <= 0:
            print("Please add a valid amount for funding the bank!")
            return False

        investor_addr = self.get_account_address()
        investor_pk = self.get_account_pk()
        note = "Investor {} makes a {} micro algos payment transaction to {}".format(self.get_name(), amount, self.created_bank.get_name())
        print("\n" + note)
        val = self.transactions.payment_txn(investor_addr, investor_pk, amount, self.created_bank.get_bank_addr(), note)
        if val:
            print("Payment transaction was successful!")
            return True
        else:
            print("Payment transaction failed!")
            return False

    def update_bank(self, bank_approval, bank_clear):
        if self.created_bank == None:
            print("The investor hasn't created a bank yet! Update not possible")
            return False
        investor_addr = self.get_account_address()
        investor_pk = self.get_account_pk()
        appr_bytes = self.transactions.compile_program(bank_approval())
        clear_bytes = self.transactions.compile_program(bank_clear())
        bank_id = self.created_bank.get_bank_id()
        note = "The investor {} updates the bank {}".format(self.get_name(), self.created_bank.get_name())
        print("\n" + note)
        val = self.transactions.call_app(investor_addr, investor_pk, 4, bank_id, note, appr_bytes, clear_bytes)
        if val:
            print("Bank was successfully updated")
            return True
        else:
            print("Bank update operation failed!")
            return False
    
    def delete_bank(self):
        if self.created_bank == None:
            print("The investor hasn't created a bank yet! Deletion not possible")
            return False
        investor_addr = self.get_account_address()
        investor_pk = self.get_account_pk()
        bank_id = self.created_bank.get_bank_id()
        note = "The investor {} deletes the bank {}".format(self.get_name(), self.created_bank.get_name())
        print("\n" + note)
        val = self.transactions.call_app(investor_addr, investor_pk, 5, bank_id, note)
        if val:
            print("Bank was successfully deleted")
            self.created_bank = None
            return True
        else:
            print("Bank delete operation failed!")
            return False