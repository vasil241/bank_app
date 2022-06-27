import os
from pyteal import *

def approval_program():

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.NoOp, Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()]
    )
    return compileTeal(program, Mode.Application, version=6)

def clear_program():
    program = Approve()
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "cloner_approval.teal"), "w") as f:
        f.write(approval_program())

    with open(os.path.join(path, "cloner_clear.teal"), "w") as f:
        f.write(clear_program())