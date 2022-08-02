import os
from pyteal import *

def reference_approval():
    # this smart contract requires 2 global byte slice as state schema 
    # it represents the logic of each bank account
    handle_setup = Seq(
        App.globalPut(Bytes("bank"), Txn.sender()), 
        Assert(Txn.accounts.length() == Int(1)),
        App.globalPut(Bytes("account_owner"), Txn.accounts[1]),
        Approve()
    )

    handle_deleteapp = Seq(
            # make sure the delete call is coming from the bank associated with the bank account
            Assert(Global.caller_app_address() == Global.creator_address()),
            # make sure the client that requested the deletion is really the owner of the account 
            Assert(Txn.accounts[1] == App.globalGet(Bytes("account_owner"))),
            # send all the funds to the account owner and then delete the bank account
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(0),
                TxnField.receiver: Txn.accounts[1], 
                TxnField.close_remainder_to: Txn.accounts[1],
                TxnField.note: Bytes("Return the remaining funds to the client and close bank account"),
                TxnField.fee: Int(0)
            }),
            InnerTxnBuilder.Submit(),
            Approve() # proceed with deletion of the bank account
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_setup],
        [Txn.on_completion() == OnComplete.NoOp, Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Approve()],
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