import os
from pyteal import *

def withdraw(): 
    txn_check = And(
        Txn.type_enum() == TxnType.ApplicationCall,
        Txn.on_completion() == OnComplete.NoOp,
        Txn.application_id() == Int(0),
        Txn.applications.length() == Int(1),
        Txn.application_args.length() == Int(1),
        Txn.accounts.length() == Int(1)
    )

    return Seq( 
        # make sure that the caller of the withdraw contract is the bank and that the withdraw contract is also a child of bank
        Assert(Txn.sender() == Global.creator_address()),
        Assert(txn_check),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            # call the bank account passed by the bank
            TxnField.application_id: Txn.applications[1],
            # pass the client address
            TxnField.accounts: [Txn.accounts[1]],
            # pass the sum that the client would like to withdraw and also which method in the bank account to activate
            TxnField.application_args: [Bytes("withdraw"), Txn.application_args[0]],
            TxnField.note: Bytes("Calling the bank account from which the withdrawal will be made from the withdraw smart contract"),
            TxnField.fee: Int(0),
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def withdraw_approval():

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
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