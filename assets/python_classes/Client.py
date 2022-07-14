class Client:
    def __init__(self, name, algorand_account):
        self.name = name
        # holds [algorand account public addr, alogrand account private key]
        self.algorand_account = algorand_account
        # will hold the corresponding bank object where client has a bank account
        self.bank = None
        # holds [account_id, account_addr]
        self.bank_account = None

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.algorand_account[0]

    def get_pk(self):
        return self.algorand_account[1]

    def get_bank_acccount_id(self):
        return self.bank_account[0]

    def get_bank_account_addr(self):
        return self.bank_account[1]
    
    def get_bank(self):
        return self.bank

    # plays the part of opt in
    def register_bank(self, bank):
        sender_addr = self.get_addr() 
        sender_pk = self.get_pk()
        sender_note = "{} wants to be a client of bank {}".format(self.name, bank.get_name())
        print(sender_note)
        val = bank.client_registration(sender_addr, sender_pk, sender_note)
        if val:
            self.bank = bank
            print("Registration was successful")
        else:
            print("Registration failed!")

    # plays the part of close out
    def leave_bank(self):
        sender_addr = self.get_addr()
        sender_pk = self.get_pk()
        sender_acc_id = self.get_bank_acccount_id()
        sender_note = "{} wants to close his account and leave the bank {}".format(self.name, self.bank.get_name())
        print(sender_note)
        val = self.bank.close_account(sender_addr, sender_pk, sender_acc_id, sender_note)
        if val:
            print("Successfully closed the bank account, {} is no longer a client of {}".format(self.name, self.bank.get_name()))
            self.bank = None
            self.bank_account = None
        else: 
            print("Closing the bank account operation failed!")

    # sends a request to the bank where the client is registered to open a bank account        
    def open_bank_account(self, initial_deposit):
        sender_addr = self.get_addr()
        sender_pk = self.get_pk()
        sender_note = "{} wishes to open a bank account with {}".format(self.name, self.bank.get_name())
        print(sender_note)
        l = self.bank.new_account(sender_addr, sender_pk, initial_deposit, sender_note)
        if l:
            print("A new bank account with id {} and address {} was created for the client {}".format(
                l[0], l[1], self.name
            ))
            self.bank_account = l
        else:
            print("The operation of opening a new bank account with {} has failed!".format(self.bank.get_name()))

    def deposit(self, amount):
        sender_addr = self.get_addr()
        sender_pk = self.get_pk()
        sender_acc_addr = self.get_bank_account_addr()
        sender_note = "Client {} wishes to deposit {} micro Algos to his bank account".format(self.name, amount)
        print(sender_note)
        val = self.bank.deposit_method(sender_addr, sender_pk, sender_acc_addr, amount, sender_note)
        if val:
            print("Deposit was successful!")
        else:
            print("Deposit failed!")

    def withdraw(self, amount):
        sender_addr = self.get_addr()
        sender_pk = self.get_pk()
        sender_acc_id = self.get_bank_acccount_id()
        sender_note = "Client {} wishes to withdraw {} micro Algos from his bank account".format(self.name, amount)
        print(sender_note)
        val = self.bank.withdraw_method(sender_addr, sender_pk, sender_acc_id, amount, sender_note)
        if val:
            print("Withdrawal was successful!")
        else:
            print("Withdrawal failed!")

    def transfer(self, receiver, amount):
        # receiver has to be an object from class Client
        sender_addr = self.get_addr()
        sender_pk = self.get_pk()
        sender_acc_id = self.get_bank_acccount_id()
        sender_note = "{} wishes to make a transfer to {}".format(self.name, receiver.get_name())
        print(sender_note)
        val = self.bank.transfer_method(sender_addr, sender_pk, sender_acc_id, receiver, amount, sender_note)
        if val:
            print("Transfer was successful")
        else:
            print("Transfer failed!")
