import os
from pyteal import *

def bank_approval():
    
    handle_delete = Seq(
        # make sure the delete call is coming from the admin who created the bank
        Assert(Txn.sender() == Global.creator_address()),
        # make sure that the bank doesn't have any more clients and children smart contract left before deleting it
        Assert(App.globalGet(Bytes("clients")) == Int(0)),
        Assert(App.globalGet(Bytes("children")) == Int(0)),
        # return the remaining funds to the admin
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(0),
                TxnField.receiver: Global.creator_address(), 
                TxnField.close_remainder_to: Global.creator_address(),
                TxnField.note: Bytes("Return the remaining funds from the bank to the admin")
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

    program = Cond(
                    [Txn.application_id() == Int(0), Approve()],
                    [Txn.on_completion() == OnComplete.OptIn, Approve()],
                    [Txn.on_completion() == OnComplete.CloseOut, Approve()],
                    [Txn.on_completion() == OnComplete.UpdateApplication, Approve()],
                    [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
                    [Txn.on_completion() == OnComplete.NoOp, Approve()]
                )

    return compileTeal(program, Mode.Application, version=6)

def bank_clear():
    program = Approve()
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "bank_approval.teal"), "w") as f:
        f.write(bank_approval())

    with open(os.path.join(path, "bank_clear.teal"), "w") as f:
        f.write(bank_clear())