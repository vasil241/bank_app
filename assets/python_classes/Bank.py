from .Transactions import *
from contracts.deposit import deposit_approval, deposit_clear
from contracts.withdraw import withdraw_approval, withdraw_clear
from contracts.transfer import transfer_approval, transfer_clear
from contracts.reference import reference_approval, reference_clear

# bank objects get created only by an Investor inside his create_bank method
class Bank:
    def __init__(self, name, investor_addr, investor_pk, bank_id, bank_addr):
        self.name = name
        # bank holds an object of type Transactions
        self.transactions = Transactions()
        # algorand account of the investor
        self.investor_addr = investor_addr
        self.investor_pk = investor_pk 
        # id and addr are the algorand smart conctract details of the bank
        self.bank_id = bank_id
        self.bank_addr = bank_addr
        # children of the bank contract, lists that store [id, addr] of the created children smart contracts
        self.deposit = None
        self.withdraw = None
        self.transfer = None
        self.bank_account_reference = None

    def get_name(self):
        return self.name
    
    def get_bank_id(self):
        return self.bank_id

    def get_bank_addr(self):
        return self.bank_addr
    
    def new_account(self, sender_addr, sender_pk, initial_deposit, sender_note):
        # should return the id and addr of the newly created bank account
        l = self.transactions.group_txns(
            sender_addr, sender_pk, self.bank_id, self.bank_addr, initial_deposit, sender_note, app_args=["open_acc"], foreign_apps=[self.bank_account_reference[0]]
            )
        return l
        
    def deposit_method(self, sender_addr, sender_pk, sender_acc_addr, amount, sender_note):
        if self.deposit == None:
            print("\nBank doesn't have a deposit functionality")
            return 0
        return self.transactions.group_txns(
            sender_addr, sender_pk, self.bank_id, self.bank_addr, amount, sender_note, app_args=["deposit"], foreign_apps=[self.deposit[0]], foreign_accs=[self.deposit[1], sender_acc_addr]
        )

    def withdraw_method(self, sender_addr, sender_pk, sender_acc_id, amount, sender_note):
        if self.withdraw == None:
            print("\nBank doesn't have a withdraw functionality")
            return 0
        return self.transactions.call_app(
            sender_addr, sender_pk, 0, self.bank_id, sender_note, app_args=["withdraw", amount], foreign_apps=[self.withdraw[0], sender_acc_id]
        )

    def transfer_method(self, sender_addr, sender_pk, sender_acc_id, receiver, amount, sender_note):
        if self.transfer == None:
            print("\nBank doesn't have a transfer functionality")
            return 0
        receiver_addr = receiver.get_addr()
        receiver_acc_addr = receiver.get_bank_account_addr()
        receiver_bank_id = receiver.get_bank().get_bank_id()
        receiver_bank_addr = receiver.get_bank().get_bank_addr()
        return self.transactions.call_app(
            sender_addr, sender_pk, 0, self.transfer[0], sender_note, app_args=[amount],
            foreign_apps=[self.transfer[0], sender_acc_id, receiver_bank_id], foreign_accs=[receiver_bank_addr, receiver_addr, receiver_acc_addr]
        )

    def close_account(self, sender_addr, sender_pk, sender_acc_id, sender_note):
        return self.transactions.call_app(sender_addr, sender_pk, 2, self.bank_id, sender_note, foreign_apps=[sender_acc_id])

    def client_registration(self, sender_addr, sender_pk, sender_note):
        return self.transactions.call_app(sender_addr, sender_pk, 1, self.bank_id, sender_note)

    def create(self, functionality):
        if functionality == "deposit":
            appr_bytes = self.transactions.compile_program(deposit_approval())
            clear_bytes = self.transactions.compile_program(deposit_clear())
            note = "Bank {} creates the deposit functionality".format(self.name)
            print("\n" + note)
            l = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["create", appr_bytes, clear_bytes, 0, 0]
            )
            if l:
                print("Deposit contract created successfully with id {} and addr {}".format(l[0], l[1]))
                self.deposit = l
            else: 
                print("Creation of the deposit contract failed!")
        elif functionality == "withdraw":
            appr_bytes = self.transactions.compile_program(withdraw_approval())
            clear_bytes = self.transactions.compile_program(withdraw_clear())
            note = "Bank {} creates the withdraw functionality".format(self.name)
            print("\n" + note)
            l = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["create", appr_bytes, clear_bytes, 0, 0]
            )
            if l:
                print("Withdraw contract created successfully with id {} and addr {}".format(l[0], l[1]))
                self.withdraw = l
            else: 
                print("Creation of the withdraw contract failed!")
        elif functionality == "transfer":
            appr_bytes = self.transactions.compile_program(transfer_approval())
            clear_bytes = self.transactions.compile_program(transfer_clear())
            note = "Bank {} creates the transfer functionality".format(self.name)
            print("\n" + note)
            l = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["create", appr_bytes, clear_bytes, 0, 0]
            )
            if l:
                print("Transfer contract created successfully with id {} and addr {}".format(l[0], l[1]))
                self.transfer = l
            else: 
                print("Creation of the transfer contract failed!")
        elif functionality == "reference":
            appr_bytes = self.transactions.compile_program(reference_approval())
            clear_bytes = self.transactions.compile_program(reference_clear())
            note = "Bank {} creates the bank account reference functionality".format(self.name)
            print("\n" + note)
            l = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["create", appr_bytes, clear_bytes, 2, 0]
            )
            if l:
                print("Reference contract created successfully with id {} and addr {}".format(l[0], l[1]))
                self.bank_account_reference = l
            else: 
                print("Creation of the reference contract failed!")
        else: 
            print("Possible inputs are only: deposit, withdraw, transfer, reference! Creation failed!")


    def update(self, functionality):
        if functionality == "deposit":
            deposit_id = self.deposit[0]
            appr_bytes = self.transactions.compile_program(deposit_approval())
            clear_bytes = self.transactions.compile_program(deposit_clear())
            note = "Bank {} updates the deposit functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["update", appr_bytes, clear_bytes], foreign_apps=[deposit_id]
            )
            if val:
                print("Update of deposit was successful!")
            else:
                print("Update of deposit failed!")
        elif functionality == "withdraw":
            withdraw_id = self.withdraw[0]
            appr_bytes = self.transactions.compile_program(withdraw_approval())
            clear_bytes = self.transactions.compile_program(withdraw_clear())
            note = "Bank {} updates the withdraw functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["update", appr_bytes, clear_bytes], foreign_apps=[withdraw_id]
            )
            if val:
                print("Update of withdraw was successful!")
            else:
                print("Update of withdraw failed!")
        elif functionality == "transfer":
            transfer_id = self.transfer[0]
            appr_bytes = self.transactions.compile_program(transfer_approval())
            clear_bytes = self.transactions.compile_program(transfer_clear())
            note = "Bank {} updates the transfer functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["update", appr_bytes, clear_bytes], foreign_apps=[transfer_id]
            )
            if val:
                print("Update of transfer was successful!")
            else:
                print("Update of transfer failed!")
        elif functionality == "reference":
            reference_id = self.bank_account_reference[0]
            appr_bytes = self.transactions.compile_program(reference_approval())
            clear_bytes = self.transactions.compile_program(reference_clear())
            note = "Bank {} updates the bank account reference functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["update", appr_bytes, clear_bytes], foreign_apps=[reference_id]
            )
            if val:
                print("Update of reference was successful!")
            else:
                print("Update of reference failed!")
        else:
            print("Possible inputs are only: deposit, withdraw, transfer, reference! Update failed!")

    def destroy(self, functionality):
        if functionality == "deposit":
            deposit_id = self.deposit[0]
            note = "Bank {} deletes the deposit functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["destroy"], foreign_apps=[deposit_id]
            )
            if val:
                print("Deposit was successfully deleted!")
                self.deposit = None
            else:
                print("Deletion of deposit failed!")
        elif functionality == "withdraw":
            withdraw_id = self.withdraw[0]
            note = "Bank {} deletes the withdraw functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["destroy"], foreign_apps=[withdraw_id]
            )
            if val:
                print("Withdraw was successfully deleted!")
                self.withdraw = None
            else:
                print("Deletion of withdraw failed!")
        elif functionality == "transfer":
            transfer_id = self.transfer[0]
            note = "Bank {} deletes the transfer functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["destroy"], foreign_apps=[transfer_id]
            )
            if val:
                print("Transfer was successfully deleted!")
                self.transfer = None
            else:
                print("Deletion of transfer failed!")
        elif functionality == "reference":
            reference_id = self.bank_account_reference[0]
            note = "Bank {} deletes the bank account reference functionality".format(self.name)
            print("\n" + note)
            val = self.transactions.call_app(
                self.investor_addr, self.investor_pk, 0, self.bank_id, note, app_args=["destroy"], foreign_apps=[reference_id]
            )
            if val:
                print("Reference was successfully deleted!")
                self.bank_account_reference = None
            else:
                print("Deletion of reference failed!")
        else:
            print("Possible inputs are only: deposit, withdraw, transfer, reference! Deletion failed!")