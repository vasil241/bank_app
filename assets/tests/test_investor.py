import pytest
from python_classes import *
from .update_contracts import *

@pytest.fixture
def investor():
    # setup
    algorand_account = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    p = Person("Vasil", algorand_account)
    p.addRole("investor", Investor(p))
    investor = p.getRole("investor")
    yield investor
    # teardown 
    if investor.get_bank() != None:
        investor.delete_bank()

@pytest.fixture
def bank(investor):
    # setup
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()
    yield bank
    # teardown
    investor.delete_bank()

def test_create_bank(investor):
    investor.create_bank("Commerzbank")
    created_bank = investor.get_bank()
    assert isinstance(created_bank, Bank) and created_bank.get_name() == "Commerzbank"

def test_create_bank_fail(investor):
    # if the investor tries to create a second bank - it should fail
    investor.create_bank("Commerzbank")
    assert investor.create_bank("DSK") == False

def test_fund_bank(investor, bank):
    assert investor.fund_bank(100000)

def test_fund_bank_fail(investor):
    # if the investor tries to fund a bank that is not created - it should fail
    assert investor.fund_bank(100000) == False

def test_update_bank(investor, bank):
    assert investor.update_bank(bank_approval, bank_clear)

def test_update_bank_fail(investor):
    # if the investor tries to update a bank that it is not created - it should fail
    assert investor.update_bank(bank_approval, bank_clear) == False

def test_delete_bank_fail1(investor):
    # if the investor tries to delete a bank that is not created - it should fail
    assert investor.delete_bank() == False

def test_delete_bank_fail2(investor):
    # if the investor tries to delete a bank that still has clients - it should fail
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()
    bank.create("reference")

    client_algorand_account = ["X7FUIUOTDJ3AKVHFN3WAPEJXA2HH5K2IWKNEMEIHAK527YND75VYALTUC4", "UkoEli+7KJQ73A0yFOAD4QnubU3QJY/LouCC1U1Dr+m/y0RR0xp2BVTlbuwHkTcGjn6rSLKaRhEHAruv4aP/aw=="]
    p = Person("Vasil", client_algorand_account)
    p.addRole("client", Client(p))
    client = p.getRole("client")
    client.open_bank_account(bank, 100000)

    assert investor.delete_bank() == False

def test_delete_bank_fail3(investor):
    # if the investor tries to delete a bank that still has additional functionality (children) - it should fail
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()
    bank.create("reference")

    assert investor.delete_bank() == False

