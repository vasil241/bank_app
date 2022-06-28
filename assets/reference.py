import os
from pyteal import *

# this smart contract actually represents the bank account
def approval_program():

    is_bank = Global.caller_app_id() == App.globalGet(Bytes("bank"))
    is_account_owner = Txn.application_args[0] == App.globalGet(Bytes("account_owner"))

    # this smart contract requires 1 global int and 1 global byte slice as state schema 
    handle_setup = Seq(
        Assert(Txn.application_args.length() == Int(2)),
        App.globalPut(Bytes("bank"), Txn.application_args[0]),
        App.globalPut(Bytes("account_owner"), Txn.application_args[1]),
        Approve()
    )

    handle_deleteapp = If(
                            is_bank,
                            Seq(
                                # send all the funds to the account owner and then delete the bank account
                                InnerTxnBuilder.Begin(),
                                InnerTxnBuilder.SetFields({
                                    TxnField.type_enum: TxnType.Payment,
                                    TxnField.close_remainder_to: App.globalGet(Bytes("account_owner"))
                                }),
                                InnerTxnBuilder.Submit(),
                                Approve() # proceed with deletion of bank account
                            ),
                            Reject()
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