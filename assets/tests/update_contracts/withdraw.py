import os
from pyteal import *

def withdraw_approval():

    handle_delete = Seq(
        # make sure the delete call is coming from the bank associated with the bank account
        Assert(Global.caller_app_address() == Global.creator_address()),
        # return the 0.1 Algo to the bank from the child
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Int(0),
            TxnField.receiver: Txn.sender(),
            TxnField.close_remainder_to: Txn.sender(),
            TxnField.note: Bytes("Returning the funds of the child to the bank"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Approve()],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
        [Txn.on_completion() == OnComplete.NoOp, Approve()]
    )

    return compileTeal(program, Mode.Application, version=6)

def withdraw_clear():
    program = Approve()
    return compileTeal(program, Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "withdraw_approval.teal"), "w") as f:
        f.write(withdraw_approval())

    with open(os.path.join(path, "withdraw_clear.teal"), "w") as f:
        f.write(withdraw_clear())