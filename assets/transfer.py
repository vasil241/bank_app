import os
from pyteal import *

def transfer():
    txn_check = And(
        Txn.type_enum() == TxnType.ApplicationCall,
        Txn.on_completion() == OnComplete.NoOp,
        Txn.application_id() == Int(0),
        # client has to pass applications[his own bank acc, foreign bank to transfer to]
        # accounts[receiver public addr, receiver bank account address]
        # args[the sum to be transfered]
        Txn.applications.length() == Int(2),
        Txn.accounts.length() == Int(2),
        Txn.application_args.length() == Int(1)
    ) 
    
    return Seq(
        Assert(txn_check),
        # to make sure the client is making a transfer from his own bank account
        Assert(Txn.sender() == App.globalGetEx(Txn.applications[1], Bytes("account_owner"))),
        # make sure that the transfer is not from a bank account to the same bank account - not allowed
        addr := AppParam.address(Txn.applications[1]),
        Assert(Txn.accounts[2] != addr.value()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            # app call to the bank account
            TxnField.application_id: Txn.applications[1],
            # giving the bank to which the recipient's bank account belongs
            TxnField.applications: [Txn.applications[2]],
            # giving the public address of the client and his bank account that will receive funds
            TxnField.accounts: [Txn.accounts[1], Txn.accounts[2]],
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
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(0),
                TxnField.receiver: Global.creator_address(), 
                TxnField.close_remainder_to: Global.creator_address(),
                TxnField.note: Bytes("Return the remaining funds from transfer contract to bank")
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