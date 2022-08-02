import pytest
from python_classes import *

@pytest.fixture
def setup():
    investor_algorand_account = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    p1 = Person("Vasil", investor_algorand_account)
    p1.addRole("investor", Investor(p1))
    investor = p1.getRole("investor")
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()

    client_algorand_account_1 = ["X7FUIUOTDJ3AKVHFN3WAPEJXA2HH5K2IWKNEMEIHAK527YND75VYALTUC4", "UkoEli+7KJQ73A0yFOAD4QnubU3QJY/LouCC1U1Dr+m/y0RR0xp2BVTlbuwHkTcGjn6rSLKaRhEHAruv4aP/aw=="]
    p2 = Person("Bob", client_algorand_account_1)
    p2.addRole("client", Client(p2))
    clientB = p2.getRole("client")

    client_algorand_account_2 = ["KSOBHAKZMD2I7SJC7CUHBWBYDSKTDB37USOYBA4IOPIZ3K3IYGMIGRVIBA", "Syj40FEBTK8I9Tml3p8GrPiz4GTXKG1ElBhNCnaTnyxUnBOBWWD0j8ki+Khw2DgclTGHf6SdgIOIc9Gdq2jBmA=="]
    p3 = Person("Alice", client_algorand_account_2)
    p3.addRole("client", Client(p3))
    clientA = p3.getRole("client")
    
    yield [bank, clientB, clientA]
    if clientB.bank_account != None:
        clientB.leave_bank()
    if clientA.bank_account != None:
        clientA.leave_bank()
    if bank.deposit != None:
        bank.destroy("deposit")
    if bank.withdraw != None:
        bank.destroy("withdraw")
    if bank.transfer != None:
        bank.destroy("transfer")
    if bank.reference != None:
        bank.destroy("reference")
    investor.delete_bank()

# def test_open_bank_account(setup):
#     bank = setup[0]
#     client = setup[1]
#     bank.create("reference")
#     assert client.open_bank_account(bank, 100000)

# def test_open_bank_account_fail1(setup):
#     bank = setup[0]
#     client = setup[1]
#     bank.create("reference")
#     assert client.open_bank_account(bank, 10000) == False

# def test_open_bank_account_fail2(setup):
#     bank = setup[0]
#     client = setup[1]
#     assert client.open_bank_account(bank, 100000) == False

# def test_open_bank_account_fail3(setup):
#     bank = setup[0]
#     client = setup[1]
#     bank.create("reference")
#     client.open_bank_account(bank, 100000)
#     assert client.open_bank_account(bank, 100000) == False

# def test_leave_bank_fail(setup):
#     client = setup[1]
#     assert client.leave_bank() == False

# def test_deposit(setup):
#     bank = setup[0]
#     client = setup[1]
#     bank.create("reference")
#     bank.create("deposit")
#     client.open_bank_account(bank, 100000)
#     assert client.deposit(50000)

def test_withdraw(setup):
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    bank.create("withdraw")
    client.open_bank_account(bank, 100000)
    assert client.withdraw(50000)









        