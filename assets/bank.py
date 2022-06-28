import os
from pyteal import *

@Subroutine(TealType.none)
def open_acc():
    # user has to first opt into the bank smart contract before calling this method
    Assert(App.optedIn(Txn.sender()))
    # acc_check is used to check if the sender has already opened a bank account
    # if yes, then he can't open another one, if no - we can proceed with creating one
    acc_check = App.localGet(Txn.sender(), Bytes("bank_account"))
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
    deposit, app_call = Gtxn[0], Gtxn[1]
    check = And(
        Global.group_size() == Int(2),
        deposit.type_enum() == TxnType.Payment,
        deposit.amount() >= min_deposit,
        deposit.receiver() == Global.current_application_address(),
        deposit.close_remainder_to() == Global.zero_address(),
        app_call.type_enum() == TxnType.ApplicationCall,
        app_call.on_completion() == OnComplete.NoOp,
        app_call.application_id() == Int(0),
        # user has to pass in the foreign application array of app_call [app id cloner, app id reference] 
        app_call.applications.length() == Int(2),
        App.globalGetEx(app_call.applications[1], Bytes("creator")) == App.globalGet(Bytes("creator")),
        App.globalGetEx(app_call.applications[2], Bytes("creator")) == App.globalGet(Bytes("creator"))
    )
    # check if the grouped transactions sent were truly valid and what this method needs
    Assert(check)
    # create the new bank account that replicates the reference.py using the cloner.py to create it
    Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: app_call.applications[1], # giving the app id of the cloner
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.application_args: [Bytes("clone"), Txn.sender()],
            TxnField.applications: [app_call.applications[2]], # giving the app id of the reference
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
        # increment the number of customers that have a bank account with the bank
        App.globalPut(Bytes("counter"), App.globalGet(Bytes("counter")) + Int(1)),
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
    check = And(
        Txn.applications.length() == Int(1),
        Txn.applications[1] == App.localGet(Txn.sender(), Bytes("bank_account"))
    )
    Assert(check)
    Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            # before removing local state of the customer and leaving the bank, the bank account should be closed
            # and the funds should be returned to the customer's balance
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: Txn.applications[1],
            TxnField.on_completion: OnComplete.DeleteApplication,
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )
    
def bank_approval():
    
    handle_noop = [
        [
            Txn.application_id() == Int(0), Return(handle_setup)
        ],
        [
            Txn.application_args[0] == Bytes("open_acc"),
            Return(Seq(open_acc(), Approve()))
        ]
    ]

    # this smart contract will store 2 global states: creator (byteslice) and counter (uint) to keep count of the clients
    # and 1 local state: store bank_account app_id for each user (uint)
    handle_setup = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), # byteslice
        App.globalPut(Bytes("counter"), Int(0)), # uint
        Approve()        
    )

    on_closeout = Seq(
        close_acc(),
        # decrement the number of customers that have a bank account with the bank
        App.globalPut(Bytes("counter"), App.globalGet(Bytes("counter")) - Int(1)),
        Approve()
    )
    
    program = Cond(
                    [Txn.application_id() == Int(0), handle_setup],
                    [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
                    [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
                    [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
                    [Txn.on_completion() == OnComplete.OptIn, Approve()],
                    [Txn.on_completion() == OnComplete.NoOp, handle_noop]
                )

    return compileTeal(program, Mode.Application, version=6)

def bank_clear():
    program = Seq(
        close_acc(),
        # decrement the number of customers that have a bank account with the bank
        App.globalPut(Bytes("counter"), App.globalGet(Bytes("counter")) - Int(1)),
        Approve()
    )
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "bank_approval.teal"), "w") as f:
        f.write(bank_approval())

    with open(os.path.join(path, "bank_clear.teal"), "w") as f:
        f.write(bank_clear())
