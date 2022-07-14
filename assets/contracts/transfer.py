import os
from pyteal import *

def transfer():
    txn_check = Seq(
        Assert(Txn.type_enum() == TxnType.ApplicationCall),
        Assert(Txn.on_completion() == OnComplete.NoOp),
        Assert(Txn.application_id() == Global.current_application_id()),
        # client has to pass applications[transfer contract id, his own bank acc, foreign bank to transfer to]
        # accounts[receiver bank addr, receiver public addr, receiver bank account address]
        # args[the sum to be transfered]
        Assert(Txn.applications.length() == Int(3)),
        Assert(Txn.accounts.length() == Int(3)),
        Assert(Txn.application_args.length() == Int(1))
    ) 
    
    return Seq(
        txn_check,
        # to make sure the client is making a transfer from his own bank account
        acc_owner := App.globalGetEx(Txn.applications[2], Bytes("account_owner")),
        Assert(acc_owner.hasValue()),
        Assert(Txn.sender() == acc_owner.value()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            # app call to the bank account
            TxnField.application_id: Txn.applications[2],
            # giving the bank to which the recipient's bank account belongs
            TxnField.applications: [Txn.applications[1], Txn.applications[3]],
            # giving the bank addr, public address of the client and his bank account addr that will receive funds
            TxnField.accounts: [Txn.accounts[1], Txn.accounts[2], Txn.accounts[3]],
            # giving which method to call and the sum to be transferred
            TxnField.application_args: [Bytes("transfer"), Txn.application_args[0]],
            TxnField.note: Bytes("Calling the bank account from which funds will be transferred from the transfer smart contract"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def transfer_approval():

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
        [Txn.on_completion() == OnComplete.NoOp, transfer()]
    )

    return compileTeal(program, Mode.Application, version=6)

def transfer_clear():
    program = Approve()
    return compileTeal(program, Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "transfer_approval.teal"), "w") as f:
        f.write(transfer_approval())

    with open(os.path.join(path, "transfer_clear.teal"), "w") as f:
        f.write(transfer_clear())