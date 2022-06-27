import os
from pyteal import *

prefix = Bytes("base16", "151f7c75")
open_acc_selector = MethodSignature("open_acc()void")

@Subroutine(TealType.none)
def open_acc():
    # acc_check is used to check if the sender has already opened a bank account
    # if yes, then he can't open another one, if no - we can proceed with creating one
    acc_check = App.localGetEx(Int(0), App.id(), Bytes("bank_account"))
    If(
        acc_check.hasValue(), # test condition - 1 is "has account" , 0 is "no account"
        Seq(
            print("You already have a bank account here! You can't have more than one!"),
            Reject()
        )
    )
    # TODO finish this method 

    

def bank_approval():

    # Define our abi methods, route based on method selector defined above
    methods = [
        [
            Txn.application_args[0] == open_acc_selector,
            Return(Seq(open_acc(), Approve())),
        ]
    ]
    
    program = Cond(
                    [Txn.application_id() == Int(0), Approve()],
                    [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
                    [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
                    [Txn.on_completion() == OnComplete.CloseOut, Reject()],
                    [Txn.on_completion() == OnComplete.OptIn, Approve()],
                    *methods,
                )
    return compileTeal(program, Mode.Application, version=6)

def bank_clear():
    program = Approve()
    return compileTeal(program, mode=Mode.Application, version=6)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, "bank_approval.teal"), "w") as f:
        f.write(bank_approval())

    with open(os.path.join(path, "bank_clear.teal"), "w") as f:
        f.write(bank_clear())