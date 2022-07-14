import os
from pyteal import *

def deposit():
    # the deposit should be called from the bank with a payment and application call transactions in a group
    deposit, deposit_call = Gtxn[0], Gtxn[1]
    gtxn_check = Seq(
        Assert(Global.group_size() == Int(2)),
        Assert(deposit.type_enum() == TxnType.Payment),
        Assert(deposit.receiver() == Global.current_application_address()),
        Assert(deposit.close_remainder_to() == Global.zero_address()),
        Assert(deposit_call.type_enum() == TxnType.ApplicationCall),
        Assert(deposit_call.on_completion() == OnComplete.NoOp),
        Assert(deposit_call.application_id() == Global.current_application_id()),
        # bank should have referenced the bank account address to which the deposit should go 
        Assert(deposit_call.accounts.length() == Int(1))
    )

    return Seq(
        gtxn_check,
        # send the deposit with an inner transactions
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: deposit_call.accounts[1],
            TxnField.amount: deposit.amount(),
            TxnField.note: Bytes("Client has successfully deposited funds into his bank account"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit()
    )

def deposit_approval():

    handle_noop = Seq(
        # make sure that the caller of the deposit contract is the bank and that the deposit contract is also a child of the bank
        Assert(Txn.sender() == Global.creator_address()),
        deposit(),
        Approve()
    )

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
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=6)

def deposit_clear():
    program = Approve()
    return compileTeal(program, Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "deposit_approval.teal"), "w") as f:
        f.write(deposit_approval())

    with open(os.path.join(path, "deposit_clear.teal"), "w") as f:
        f.write(deposit_clear())