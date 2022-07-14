import os
from pyteal import *

def withdraw(): 
    txn_check = Seq(
        Assert(Txn.type_enum() == TxnType.ApplicationCall),
        Assert(Txn.on_completion() == OnComplete.NoOp),
        Assert(Txn.application_id() == Global.current_application_id()),
        Assert(Txn.applications.length() == Int(2)),
        Assert(Txn.application_args.length() == Int(1)),
        Assert(Txn.accounts.length() == Int(1))
    )

    return Seq( 
        # make sure that the caller of the withdraw contract is the bank and that the withdraw contract is also a child of bank
        Assert(Txn.sender() == Global.creator_address()),
        txn_check,
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            # call the bank account passed by the bank
            TxnField.application_id: Txn.applications[2],
            TxnField.applications: [Txn.applications[1]],
            # pass the client address
            TxnField.accounts: [Txn.accounts[1]],
            # pass the sum that the client would like to withdraw and also which method in the bank account to activate
            TxnField.application_args: [Bytes("withdraw"), Txn.application_args[0]],
            TxnField.note: Bytes("Calling the bank account from which the withdrawal will be made from the withdraw smart contract"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def withdraw_approval():

    handle_update = Seq(
        # make sure the update call is coming from the bank associated with the bank account
        Assert(Global.caller_app_address() == Global.creator_address()),
        Approve()
    )

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
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
        [Txn.on_completion() == OnComplete.NoOp, withdraw()]
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