import os
from pyteal import *

prefix = Bytes("base16", "151f7c75")
open_acc_selector = MethodSignature("open_acc()void")

@Subroutine(TealType.none)
def open_acc():
    # user has to first opt into the bank smart contract before calling this method
    Assert(App.optedIn(Txn.sender()))
    # acc_check is used to check if the sender has already opened a bank account
    # if yes, then he can't open another one, if no - we can proceed with creating one
    acc_check = App.localGetEx(Int(0), App.id(), Bytes("bank_account"))
    If(
        acc_check.hasValue(),
        Seq(
            print("You already have a bank account here! You can't have more than one!"),
            Reject()
        )
    )
    min_deposit = Int(int(1e5)) # 0.1A - the min required deposit to open a bank account
    # in order to call correctly the open_acc() the user needs to send also a payment transaction
    # the fields of this transaction will be stored in deposit variable in order to check validity 
    deposit = Gtxn[0]
    deposit_check = And(
        Global.group_size() == Int(1),
        deposit.type_enum() == TxnType.Payment,
        deposit.amount() >= min_deposit,
        deposit.receiver() == Global.current_application_address(),
        deposit.close_remainder_to() == Global.zero_address()
    )
    Assert(deposit_check)
    # create the new bank account that replicates the reference.py using the cloner.py to create it
    Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: App.globalGet(Bytes("cloner")),
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.application_args: [Bytes("clone"), Txn.sender()],
            TxnField.applications: [App.globalGet(Bytes("reference"))],
            TxnField.fee: Int(0) 
        }),
        InnerTxnBuilder.Submit()
    )
    # get the app id of the newly created bank account for the customer
    new_acc_id = InnerTxn.created_application_id()
    # save it to the local storage of the customer under "bank_account" key
    App.localPut(Int(0), Bytes("bank_account"), new_acc_id)
    new_acc_addr = AppParam.address(InnerTxn.created_application_id())
    
    Seq(
        new_acc_id,
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                # send the deposit to the newly created bank account of the customer
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: deposit.amount(),
                TxnField.receiver: new_acc_addr.value(),
                TxnField.fee: Int(0),
            }
        ),
        InnerTxnBuilder.Submit(),
    )

def close_acc():
    Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            # before removing local state of the customer and leaving the bank, the bank account should be closed
            # and the funds should be returned to the customer's balance
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: App.localGet(Txn.sender(), Bytes("bank_account")),
            TxnField.on_completion: OnComplete.DeleteApplication,
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )
    
def bank_approval():
    
    # Define our abi methods, route based on method selector defined above
    methods = [
        [
            Txn.application_args[0] == open_acc_selector,
            Return(Seq(open_acc(), Approve()))
        ]
    ]

    # this smart contract will store 4 global state vars: creator, reference.py, cloner.py and counter
    # counter is just to show number of customers at any moment - can be good also for debuggin purposes
    handle_setup = Seq(
        Approve()
        # Finish this up
    )

    on_closeout = Seq(
        close_acc(),
        Approve()
    )
    
    program = Cond(
                    [Txn.application_id() == Int(0), handle_setup],
                    [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
                    [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
                    [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
                    [Txn.on_completion() == OnComplete.OptIn, Approve()],
                    *methods,
                )
    return compileTeal(program, Mode.Application, version=6)

def bank_clear():
    program = Seq(
        close_acc(),
        Approve()
    )
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "bank_approval.teal"), "w") as f:
        f.write(bank_approval())

    with open(os.path.join(path, "bank_clear.teal"), "w") as f:
        f.write(bank_clear())