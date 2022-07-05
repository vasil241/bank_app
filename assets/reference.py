import os
from pyteal import *

# every bank account uses this smart contract as reference

def withdraw():
    return Seq(
        # to make sure that the withdraw contract that called this method is child of bank (parent)
        creator := AppParam.creator(Global.caller_app_id()),
        Assert(creator.value() == Global.creator_address()),
        Assert(Txn.accounts[1] == App.globalGet(Bytes("account_owner"))),
        Assert(Btoi(Txn.application_args[0]) <= (Balance(Global.current_application_address()) - MinBalance(Global.current_application_address))),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Btoi(Txn.application_args[0]),
            TxnField.receiver: Txn.accounts[1],
            TxnField.close_remainder_to: Global.zero_address(),
            TxnField.note: Bytes("The client successfully withdrew funds from his bank account"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def transfer():
    txn_check = And(
        Txn.type_enum() == TxnType.ApplicationCall,
        Txn.on_completion() == OnComplete.NoOp,
        Txn.application_id() == Int(0),
        Txn.applications.length() == Int(1),
        Txn.accounts.length() == Int(2),
        Txn.application_args.length() == Int(2)
    )

    return Seq(
        # to make sure that the transfer contract that called this method is child of bank (parent)
        creator := AppParam.creator(Global.caller_app_id()),
        Assert(creator.value() == Global.creator_address()),
        Assert(txn_check),
        Assert(Txn.application_args[1] <= (Balance(Global.current_application_address()) - MinBalance(Global.current_application_address))),
        addr := AppParam.address(Txn.applications[1]),
        Assert(addr.hasValue()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: addr.value(),
            TxnField.amount: Btoi(Txn.application_args[1]),
            TxnField.close_remainder_to: Global.zero_address(),
            TxnField.note: Bytes("Transferring funds to a different bank account in a foreing or the same bank"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Next(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.application_id: Txn.applications[1],
            TxnField.accounts: [Txn.accounts[1], Txn.accounts[2]],
            TxnField.application_args: [Bytes("transfer")],
            TxnField.note: Bytes("Sending the transfer to the bank for processing"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def reference_approval():
    
    # this smart contract requires 2 global byte slice as state schema 
    # it represents the logic of each bank account
    handle_setup = Seq(
        App.globalPut(Bytes("bank"), Txn.sender()), 
        Assert(Txn.accounts.length() == Int(1)),
        App.globalPut(Bytes("account_owner"), Txn.accounts[1]),
        Approve()
    )

    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("withdraw"), withdraw()],
        [Txn.application_args[0] == Bytes("transfer"), transfer()]
    )

    handle_deleteapp = If(
        # make sure the delete call is coming from the bank associated with the bank account
        Assert(Global.caller_app_address() == Global.creator_address()),
        # make sure the client that requested the deletion is really the owner of the account 
        Assert(Txn.accounts[1] == App.globalGet(Bytes("account_owner"))),
        Seq(
            # send all the funds to the account owner and then delete the bank account
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(int(1e4)),
                TxnField.receiver: Txn.accounts[1], 
                TxnField.close_remainder_to: Txn.accounts[1],
                TxnField.note: Bytes("Return the remaining funds to the client and close bank account")
            }),
            InnerTxnBuilder.Submit(),
            Approve() # proceed with deletion of the bank account
        ),
        Reject()
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_setup],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp]
    )
    return compileTeal(program, Mode.Application, version=6)

def reference_clear():
    program = Approve()
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "reference_approval.teal"), "w") as f:
        f.write(reference_approval())

    with open(os.path.join(path, "reference_clear.teal"), "w") as f:
        f.write(reference_clear())