import pytest
from python_classes import *

@pytest.fixture
def setup():
    # setup
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
    # teardown
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

def test_open_bank_account(setup):
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    assert client.open_bank_account(bank, 100000)

def test_open_bank_account_fail1(setup):
    # each new algorand account needs at least 0.1 Algo to be operational on the blockchain 
    # if the client funds his new bank account with < 0.1 Algo - it should fail
    # 0.1 Algo = 100000 Mini Algos
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    assert client.open_bank_account(bank, 10000) == False

def test_open_bank_account_fail2(setup):
    # if the reference contract is not created for the bank and client tries to open an account - it should fail
    bank = setup[0]
    client = setup[1]
    assert client.open_bank_account(bank, 100000) == False

def test_open_bank_account_fail3(setup):
    # if the client tries to open a second account with the same bank - it should fail
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    client.open_bank_account(bank, 100000)
    assert client.open_bank_account(bank, 100000) == False

def test_leave_bank_fail(setup):
    # if the person isn't a client of any bank, but tries to leave one - it should fail
    client = setup[1]
    assert client.leave_bank() == False

def test_deposit(setup):
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    bank.create("deposit")
    client.open_bank_account(bank, 100000)
    assert client.deposit(50000)

def test_withdraw(setup):
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    bank.create("withdraw")
    client.open_bank_account(bank, 200000)
    assert client.withdraw(50000)

def test_withdraw_fail(setup):
    # if the withdrawal will leave the funds in the bank account under 0.1 Algo (min balance) - it should fail
    bank = setup[0]
    client = setup[1]
    bank.create("reference")
    bank.create("withdraw")
    client.open_bank_account(bank, 100000)
    assert client.withdraw(50000) == False

def test_transfer(setup):
    bank = setup[0]
    clientB = setup[1]
    clientA = setup[2]
    bank.create("reference")
    bank.create("transfer")
    clientB.open_bank_account(bank, 200000)
    clientA.open_bank_account(bank, 100000)
    assert clientB.transfer(clientA, 50000)

def test_transfer_fail(setup):
    # if the transfer will leave the funds in the bank account under 0.1 Algo (min balance) - it should fail
    bank = setup[0]
    clientB = setup[1]
    clientA = setup[2]
    bank.create("reference")
    bank.create("transfer")
    clientB.open_bank_account(bank, 100000)
    clientA.open_bank_account(bank, 100000)
    assert clientB.transfer(clientA, 50000) == False




        