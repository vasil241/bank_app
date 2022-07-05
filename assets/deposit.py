import os
from pyteal import *

def deposit():
    # the deposit should be called from the bank with a payment and application call transactions in a group
    deposit, deposit_call = Gtxn[0], Gtxn[1]
    gtxn_check = And(
        Global.group_size() == Int(2),
        deposit.type_enum() == TxnType.Payment,
        deposit.receiver() == Global.current_application_address(),
        deposit.close_remainder_to() == Global.zero_address(),
        deposit_call.type_enum() == TxnType.ApplicationCall,
        deposit_call.on_completion() == OnComplete.NoOp,
        deposit_call.application_id() == Int(0),
        # bank should have referenced the bank account to which the deposit should go 
        deposit_call.applications.length() == Int(1)
    )

    return Seq(
        Assert(gtxn_check),
        # store the address of the receiver (the bank account)
        addr := AppParam.address(deposit_call.applications[1]),
        Assert(addr.hasValue()),
        # send the deposit with an inner transactions
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: addr.value(),
            TxnField.amount: deposit.amount(),
            TxnField.close_remainder_to: Global.zero_address(),
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

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
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