import os
from pyteal import *

def approval_program():

    is_bank = Txn.sender() == App.globalGet(Bytes("bank"))
    is_account_owner = Txn.application_args[0] == App.globalGet(Bytes("account_owner"))

    handle_setup = Seq(
        App.globalPut(Bytes("bank"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(1)),
        App.globalPut(Bytes("account_owner"), Txn.application_args[0]),
        Approve()
    )

    handle_deleteapp = Seq(
        If(
            is_bank,
            Seq(
                # inner transaction to send all the funds to the account owner and then delete the app
                # approve then
            ),
            Reject()
        )
    )

    handle_noop = Approve()

    program = Cond(
        [Txn.application_id() == Int(0), handle_setup],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp]
    )
    return compileTeal(program, Mode.Application, version=6)

def clear_program():
    program = Approve()
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "reference_approval.teal"), "w") as f:
        f.write(approval_program())

    with open(os.path.join(path, "reference_clear.teal"), "w") as f:
        f.write(clear_program())