import os
from pyteal import *

def open_acc():
    # a correct call to open_acc() needs to include also a payment transaction in addition to the app call
    deposit, app_call = Gtxn[0], Gtxn[1]
    gtxn_check = Seq(
        Assert(Global.group_size() == Int(2)),
        Assert(deposit.type_enum() == TxnType.Payment),
        Assert(deposit.receiver() == Global.current_application_address()),
        Assert(deposit.close_remainder_to() == Global.zero_address()),
        Assert(app_call.type_enum() == TxnType.ApplicationCall),
        Assert(app_call.on_completion() == OnComplete.NoOp),
        Assert(app_call.application_id() == Global.current_application_id()),
        # applications[1] represent the logic in reference.py
        # this is the smart contract that each bank account replicates
        Assert(app_call.applications.length() == Int(1))
    )
    
    return Seq(
        # client has to first be opted into the bank
        Assert(App.optedIn(Txn.sender(), Global.current_application_id())),
        # acc_check is used to check if the sender has already opened a bank account, more than 1 is not allowed
        If(App.localGet(Txn.sender(), Bytes("bank_account_id")), Reject()),
        gtxn_check,
        # the reference contract should be a child of the bank (parent)
        creator := AppParam.creator(app_call.applications[1]),
        Assert(Global.current_application_address() == creator.value()),
        # we take the programs and state schema of the reference contract to create a new bank account
        approval_prog := AppParam.approvalProgram(app_call.applications[1]),
        clear_prog := AppParam.clearStateProgram(app_call.applications[1]),
        global_byteslices_number := AppParam.globalNumByteSlice(app_call.applications[1]),
        Assert(approval_prog.hasValue()),
        Assert(clear_prog.hasValue()),
        Assert(global_byteslices_number.hasValue()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.approval_program: approval_prog.value(),
            TxnField.clear_state_program: clear_prog.value(),
            TxnField.global_num_byte_slices: global_byteslices_number.value(),
            TxnField.global_num_uints: Int(0), # no global uints in bank account
            # client addr in foreign accounts to create a connection between client and bank account
            TxnField.accounts: [Txn.sender()],
            TxnField.note: Bytes("Creates a new bank account for the client"),
            TxnField.fee: Int(0) 
            }),
        InnerTxnBuilder.Submit(),
        # get the app id and address of the newly created bank account
        App.localPut(Txn.sender(), Bytes("bank_account_id"), InnerTxn.created_application_id()),
        acc_addr := AppParam.address(InnerTxn.created_application_id()),
        Assert(acc_addr.hasValue()),
        App.localPut(Txn.sender(), Bytes("bank_account_addr"), acc_addr.value()),
        # fund the bank account with the client's initial deposit 
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: deposit.amount(),
            TxnField.receiver: acc_addr.value(),
            TxnField.note: Bytes("Funds the newly created bank account"),
            TxnField.fee: Int(0),
        }),
        InnerTxnBuilder.Submit(),
        # increase the number of the bank's clients by 1
        App.globalPut(Bytes("clients"), App.globalGet(Bytes("clients")) + Int(1)),
        Approve()
    )

def withdraw():
    txn_check = Seq(
        Assert(Txn.type_enum() == TxnType.ApplicationCall),
        Assert(Txn.on_completion() == OnComplete.NoOp),
        Assert(Txn.application_id() == Global.current_application_id()),
        # the client must reference [withdraw contract, his bank acc]
        Assert(Txn.applications.length() == Int(2)),
        # in args ["withdraw", sum to withdraw] - "withdraw" triggers this method in the bank
        Assert(Txn.application_args.length() == Int(2))
    )

    return Seq(
        txn_check,
        # to check if the withdraw contract referenced by the client is a child of the bank (parent)
        creator := AppParam.creator(Txn.applications[1]),
        Assert(Global.current_application_address() == creator.value()),
        # is the given bank account by the client truly his
        Assert(Txn.applications[2] == App.localGet(Txn.sender(), Bytes("bank_account_id"))),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            # making the call to the withdraw contract
            TxnField.application_id: Txn.applications[1],
            # passing the referenced bank account in the application array
            TxnField.applications: [Txn.applications[1], Txn.applications[2]],
            TxnField.accounts: [Txn.sender()],
            # passing the sum to be withdrawn
            TxnField.application_args: [Txn.application_args[1]],
            TxnField.note: Bytes("Bank calls the withdraw contract"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def transfer_receive():
    # when funds are sent from one bank account to another, the transfer is processed first in the bank
    transfer_sum, transfer_call = Gtxn[0], Gtxn[1]
    gtxn_check = Seq(
        Assert(Global.group_size() == Int(2)),
        Assert(transfer_sum.type_enum() == TxnType.Payment),
        Assert(transfer_sum.receiver() == Global.current_application_address()),
        Assert(transfer_sum.close_remainder_to() == Global.zero_address()),
        Assert(transfer_call.type_enum() == TxnType.ApplicationCall),
        Assert(transfer_call.on_completion() == OnComplete.NoOp),
        Assert(transfer_call.application_id() == Global.current_application_id()), 
        # should include the receiver's public address and the addr of his bank account
        Assert(transfer_call.accounts.length() == Int(2)),
        # should include "transfer" to trigger this method 
        Assert(transfer_call.application_args.length() == Int(1))
    )

    return Seq(
        gtxn_check,
        # to check if the provied receiver really has a bank account in this bank
        Assert(transfer_call.accounts[2] == App.localGet(transfer_call.accounts[1], Bytes("bank_account_addr"))),
        # transfer the funds to the recipient's bank account
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: transfer_call.accounts[2],
            TxnField.amount: transfer_sum.amount(),
            TxnField.note: Bytes("Successful transfer to the recipient's bank account"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def deposit():
    # this method enables the client to deposit more money in his own bank account
    deposit, app_call = Gtxn[0], Gtxn[1]
    gtxn_check = Seq(
        Assert(Global.group_size() == Int(2)),
        Assert(deposit.type_enum() == TxnType.Payment),
        Assert(deposit.receiver() == Global.current_application_address()),
        Assert(deposit.close_remainder_to() == Global.zero_address()),
        Assert(app_call.type_enum() == TxnType.ApplicationCall),
        Assert(app_call.on_completion() == OnComplete.NoOp),
        Assert(app_call.application_id() == Global.current_application_id()),
        # client should reference in the applications[deposit contract app id]  
        Assert(app_call.applications.length() == Int(1)),
        # client should reference deposit contract address and bank account address
        Assert(app_call.accounts.length() == Int(2)),
        # args["deposit"] to trigger this method when calling the bank
        Assert(app_call.application_args.length() == Int(1))
    )

    return Seq(
        gtxn_check,
        # the deposit contract that the client gave as reference should be child of this bank
        creator := AppParam.creator(Txn.applications[1]),
        Assert(Global.current_application_address() == creator.value()),
        # the bank account referenced should be connected to this bank and the client
        Assert(app_call.accounts[2] == App.localGet(Txn.sender(), Bytes("bank_account_addr"))),
        # send a group of 2 inner transactions to the deposit smart contract 
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: Txn.accounts[1],
            TxnField.amount: deposit.amount(),
            TxnField.note: Bytes("Send the deposit amount to the deposit smart contract from the bank"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Next(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: app_call.applications[1],
            TxnField.on_completion: OnComplete.NoOp,
            # reference the bank account address of the client that wishes to make a deposit
            TxnField.accounts: [Txn.accounts[2]],
            TxnField.note: Bytes("Bank calls the deposit smart contract"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def close_acc(): 
    return Seq(
        # client should provide his bank account id when he wants to close it
        Assert(Txn.applications.length() == Int(1)),
        # check if the bank account truly belongs to the client, doesn't apply for the bank account of the admin
        If(
            Txn.sender() != Global.creator_address(), 
            Assert(Txn.applications[1] == App.localGet(Txn.sender(), Bytes("bank_account_id")))
        ),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            # funds should be returned to client before closing his bank account and leaving the bank
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: Txn.applications[1],
            TxnField.on_completion: OnComplete.DeleteApplication,
            TxnField.accounts: [Txn.sender()],
            TxnField.note: Bytes("Bank begins the process of closing the client's bank account"),
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
    )

def create(appr_prog, clear_prog, global_byteslice, global_uint):
    return Seq(
        # only the admin that created the bank can execute the logic inside this method
        Assert(Txn.sender() == Global.creator_address()),
        Assert(Len(appr_prog)),
        Assert(Len(clear_prog)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.approval_program: appr_prog,
            TxnField.clear_state_program: clear_prog,
            TxnField.global_num_byte_slices: Btoi(global_byteslice),
            TxnField.global_num_uints: Btoi(global_uint),
            # this field is only because of the reference contract requirement in setup
            TxnField.accounts: [Txn.sender()],
            TxnField.note: Bytes("Bank deploys a new child/functionality (additional smart contract)"),
        }),
        InnerTxnBuilder.Submit(),
        child_addr := AppParam.address(InnerTxn.created_application_id()),
        Assert(child_addr.hasValue()),
        # fund the newly created child smart contract with funds from the bank 
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Int(100000), # 0.1 Algo is more than enough
            TxnField.receiver: child_addr.value(),
            TxnField.note: Bytes("Fund the newly created child smart contract / additional functionality"),
        }),
        InnerTxnBuilder.Submit(),
        App.globalPut(Bytes("children"), App.globalGet(Bytes("children")) + Int(1)),
        Approve()
    )

def update(app_id, new_appr_prog, new_clear_prog):
    return Seq(
        # only the admin that created the bank can execute the logic inside this method
        Assert(Txn.sender() == Global.creator_address()),
        # check if the app id provided is truly already a child of the bank
        Assert(Txn.applications.length() == Int(1)),
        creator := AppParam.creator(app_id),
        Assert(Global.current_application_address() == creator.value()),
        Assert(Len(new_appr_prog)),
        Assert(Len(new_clear_prog)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.UpdateApplication,
            TxnField.application_id: app_id,
            TxnField.approval_program: new_appr_prog,
            TxnField.clear_state_program: new_clear_prog,
            TxnField.note: Bytes("Update call to a child from the bank"), 
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

def destroy(app_id):
    # only the admin that created the bank can execute the logic inside this method
    return Seq(
        Assert(Txn.sender() == Global.creator_address()),
        Assert(Txn.applications.length() == Int(1)),
        creator := AppParam.creator(Txn.applications[1]),
        Assert(Global.current_application_address() == creator.value()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.on_completion: OnComplete.DeleteApplication,
            TxnField.application_id: app_id,
            TxnField.accounts: [Txn.sender()],
            TxnField.note: Bytes("Delete call to a child from the bank"),
            }),
        InnerTxnBuilder.Submit(),
        App.globalPut(Bytes("children"), App.globalGet(Bytes("children")) - Int(1)),
        Approve()
    )
    
def bank_approval():
    
    handle_noop = Cond(
        # when sending a NoOp app call, the sender should specify in the args[0] which method he wants to execute
        [Txn.application_args[0] == Bytes("open_acc"), open_acc()],
        [
            Txn.application_args[0] == Bytes("create"),
            create(Txn.application_args[1],Txn.application_args[2], Txn.application_args[3], Txn.application_args[4])
        ],
        [Txn.application_args[0] == Bytes("update"), update(Txn.applications[1], Txn.application_args[1], Txn.application_args[2])],
        [Txn.application_args[0] == Bytes("destroy"), destroy(Txn.applications[1])],
        [Txn.application_args[0] == Bytes("withdraw"), withdraw()],
        [Txn.application_args[0] == Bytes("deposit"), deposit()],
        [Txn.application_args[0] == Bytes("transfer"), transfer_receive()]
    )

    # this smart contract will store 3 global states: creator (byteslice) and 2 counters (uint) to keep count of the clients and children of the bank
    # and 2 local states: store the app id of the bank account for each client (uint)
    # store the bank account address for each client (byteslice)
    handle_setup = Seq(
        App.globalPut(Bytes("creator"), Txn.sender()), # byteslice
        App.globalPut(Bytes("clients"), Int(0)), # uint
        App.globalPut(Bytes("children"), Int(0)), #uint
        Approve()        
    )

    on_closeout = Seq(
        # before closing the bank account, return the funds from it to the owner
        close_acc(),
        # decrement the number of clients that have a bank account with the bank
        App.globalPut(Bytes("clients"), App.globalGet(Bytes("clients")) - Int(1)),
        Approve()
    )

    handle_update = Seq(
        # make sure the update call is coming from the admin who created the bank
        Assert(Txn.sender() == Global.creator_address()),
        Approve()
    )

    handle_delete = Seq(
        # make sure the delete call is coming from the admin who created the bank
        Assert(Txn.sender() == Global.creator_address()),
        # make sure that the bank doesn't have any more clients and children smart contract left before deleting it
        Assert(App.globalGet(Bytes("clients")) == Int(0)),
        Assert(App.globalGet(Bytes("children")) == Int(0)),
        # return the remaining funds to the admin
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(0),
                TxnField.receiver: Global.creator_address(), 
                TxnField.close_remainder_to: Global.creator_address(),
                TxnField.note: Bytes("Return the remaining funds from the bank to the admin")
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )
    
    program = Cond(
                    [Txn.application_id() == Int(0), handle_setup],
                    [Txn.on_completion() == OnComplete.OptIn, Approve()],
                    [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
                    [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
                    [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
                    [Txn.on_completion() == OnComplete.NoOp, handle_noop]
                )

    return compileTeal(program, Mode.Application, version=6)

def bank_clear():
    program = Seq(
        Assert(Txn.applications.length() == Int(1)),
        close_acc(),
        # decrement the number of clients that have a bank account with the bank
        App.globalPut(Bytes("clients"), App.globalGet(Bytes("clients")) - Int(1)),
        Approve()
    )
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "bank_approval.teal"), "w") as f:
        f.write(bank_approval())

    with open(os.path.join(path, "bank_clear.teal"), "w") as f:
        f.write(bank_clear())
