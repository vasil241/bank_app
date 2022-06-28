import os
from pyteal import *

def clone():
    # Txn.applications[0] is always reserved for the current app, so that's why we use [1]
    approval_prog = AppParam.approvalProgram(Txn.applications[1])
    clear_prog = AppParam.clearStateProgram(Txn.applications[1])
    global_byteslices_number = AppParam.globalNumByteSlice(Txn.applications[1])
    global_uint_number = AppParam.globalNumUnit(Txn.applications[1])
    # I am assigning AppParam to vars, because writing them inline in the inner transaction would have issues with compiling to TEAL
    return Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.approval_program: approval_prog.value(),
            TxnField.clear_state_program: clear_prog.value(),
            TxnField.global_num_byte_slices: global_byteslices_number.value(),
            TxnField.global_num_uints: global_uint_number.value(),
            # reference.py uses args[0] for setting the bank and args[1] for account_owner in global storage
            # in Txn.application_id() is the app id of the bank and in Txn.application_args[1] is the Txn.sender() that called the bank 
            TxnField.application_args: [Txn.application_id(), Txn.application_args[1]],
            TxnField.fee: Int(0) 
            }),
        InnerTxnBuilder.Submit()
    )

def approval_program():
    # this smart contract doesn't have any global or local storage 
    handle_noop = If(
            # the whole purpose of this smart contract is to be called from the bank and create a new bank account 
            # using the reference.py
            Txn.application_args[0] == Bytes("clone"),
            clone(),
            Reject()
    )

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
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