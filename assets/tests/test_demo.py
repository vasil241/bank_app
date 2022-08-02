import pytest
from python_classes import *

def test_demo():
    
    account_1 = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    account_2 = ["X7FUIUOTDJ3AKVHFN3WAPEJXA2HH5K2IWKNEMEIHAK527YND75VYALTUC4", "UkoEli+7KJQ73A0yFOAD4QnubU3QJY/LouCC1U1Dr+m/y0RR0xp2BVTlbuwHkTcGjn6rSLKaRhEHAruv4aP/aw=="]
    account_3 = ["KSOBHAKZMD2I7SJC7CUHBWBYDSKTDB37USOYBA4IOPIZ3K3IYGMIGRVIBA", "Syj40FEBTK8I9Tml3p8GrPiz4GTXKG1ElBhNCnaTnyxUnBOBWWD0j8ki+Khw2DgclTGHf6SdgIOIc9Gdq2jBmA=="]

    person1 = Person("Vasil", account_1)
    person2 = Person("Bob", account_2)
    person3 = Person("Alice", account_3)
    person1.addRole("investor", Investor(person1))
    person2.addRole("client", Client(person2))
    person3.addRole("client", Client(person3))

    investor = person1.getRole("investor")
    clientB = person2.getRole("client")
    clientA = person3.getRole("client")

    investor.create_bank("Commerzbank")
    bank = investor.get_bank()

    # all of the instructions return a True/False value
    # if something fails, the whole demo fails (test fails)
    # if everything goes well, the assert at the end should be True and the test passed 
    instructions = [
        bank.create("deposit"),
        bank.create("withdraw"),
        bank.create("transfer"),
        bank.create("reference"),
        clientB.open_bank_account(bank, 100000),
        clientA.open_bank_account(bank, 100000),
        clientB.deposit(100000),
        clientB.withdraw(50000),
        clientB.transfer(clientA, 50000),
        clientA.leave_bank(),
        person2.removeRole("client"),
        clientB.leave_bank(),
        person3.removeRole("client"),
        bank.destroy("deposit"),
        bank.destroy("withdraw"),
        bank.destroy("transfer"),
        bank.destroy("reference"),
        investor.delete_bank(),
        person1.removeRole("investor")
    ]

    check = None
    counter = 0
    while counter < len(instructions):
        check = instructions[counter]
        if check == False:
            break
        counter += 1
    
    assert check == True