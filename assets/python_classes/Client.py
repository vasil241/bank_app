from .RoleAbstract import * 

class Client(RoleAbstract):
    def __init__(self, person):
        self.person = person
        # will hold the corresponding bank object where client has a bank account
        self.bank = None
        # holds [bank account id, bank account addr]
        self.bank_account = None

    def get_bank_acccount_id(self):
        return self.bank_account[0]

    def get_bank_account_addr(self):
        return self.bank_account[1]
    
    def get_bank(self):
        return self.bank

    # plays the part of close out
    def leave_bank(self):
        if self.bank != None:
            sender_addr = self.get_account_address() 
            sender_pk = self.get_account_pk()
            sender_acc_id = self.get_bank_acccount_id()
            sender_note = "{} wants to close his account and leave the bank {}".format(self.get_name(), self.bank.get_name())
            print("\n" + sender_note)
            val = self.bank.close_account(sender_addr, sender_pk, sender_acc_id, sender_note)
            if val:
                print("Successfully closed the bank account, {} is no longer a client of {}".format(self.get_name(), self.bank.get_name()))
                self.bank = None
                self.bank_account = None
                return True
            else: 
                print("Closing the bank account operation failed!")
                return False
        else:
            print("Client is not connected to any bank!")
            return False

    # sends a request to the bank to get registered as a client and open a bank account        
    def open_bank_account(self, bank, initial_deposit):
        sender_addr = self.get_account_address() 
        sender_pk = self.get_account_pk()
        if initial_deposit < 100000:
                print("Initial deposit for creating bank account should be at least 0.1 Algo!")
                return False
        if self.bank == None:
            sender_note = "{} wants to be a client of bank {}".format(self.get_name(), bank.get_name())
            print("\n" + sender_note)
            reg = bank.client_registration(sender_addr, sender_pk, sender_note)
            if reg:
                self.bank = bank
                print("Registration as a client in the bank was successful")
            else:
                print("Registration as a client in the bank failed!")
                return False
            sender_note = "{} wishes to open a bank account with {}".format(self.get_name(), self.bank.get_name())
            print("\n" + sender_note)
            l = self.bank.new_account(sender_addr, sender_pk, initial_deposit, sender_note)
            if l:
                print("A new bank account with id {} and address {} was created for the client {}".format(
                    l[0], l[1], self.get_name()
                ))
                self.bank_account = l
                return True
            else:
                print("The operation of opening a new bank account with {} has failed!".format(self.bank.get_name()))
                self.bank = None
                return False
        else: 
            print("Client already has a bank account in the bank {}!".format(bank.get_name()))
            return False

    def deposit(self, amount):
        if self.bank_account != None:
            sender_addr = self.get_account_address()
            sender_pk = self.get_account_pk()
            sender_acc_addr = self.get_bank_account_addr()
            sender_note = "Client {} wishes to deposit {} micro Algos to his bank account".format(self.get_name(), amount)
            print("\n" + sender_note)
            val = self.bank.deposit_method(sender_addr, sender_pk, sender_acc_addr, amount, sender_note)
            if val:
                print("Deposit was successful!")
                return True
            else:
                print("Deposit failed!")
                return False
        else:
            print("Client has no bank account! Deposit operation failed")
            return False

    def withdraw(self, amount):
        if self.bank_account != None:
            sender_addr = self.get_account_address()
            sender_pk = self.get_account_pk()
            sender_acc_id = self.get_bank_acccount_id()
            sender_note = "Client {} wishes to withdraw {} micro Algos from his bank account".format(self.get_name(), amount)
            print("\n" + sender_note)
            val = self.bank.withdraw_method(sender_addr, sender_pk, sender_acc_id, amount, sender_note)
            if val:
                print("Withdrawal was successful!")
                return True
            else:
                print("Withdrawal failed!")
                return False
        else: 
            print("Client has no bank account! Withdraw operation failed")
            return False

    def transfer(self, receiver, amount):
        if self.bank_account != None:
            # receiver has to be an object from class Client
            sender_addr = self.get_account_address()
            sender_pk = self.get_account_pk()
            sender_acc_id = self.get_bank_acccount_id()
            sender_note = "{} wishes to make a transfer to {}".format(self.get_name(), receiver.get_name())
            print("\n" + sender_note)
            val = self.bank.transfer_method(sender_addr, sender_pk, sender_acc_id, receiver, amount, sender_note)
            if val:
                print("Transfer was successful")
                return True
            else:
                print("Transfer failed!")
                return False
        else:
            print("Client has no bank account! Transfer operation failed")
            return False
