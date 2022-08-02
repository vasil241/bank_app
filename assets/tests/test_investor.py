import pytest
from python_classes import *
from .update_contracts import *

@pytest.fixture
def investor():
    algorand_account = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    p = Person("Vasil", algorand_account)
    p.addRole("investor", Investor(p))
    investor = p.getRole("investor")
    yield investor
    if investor.get_bank() != None:
        investor.delete_bank()

@pytest.fixture
def bank(investor):
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()
    yield bank
    investor.delete_bank()

def test_create_bank(investor):
    investor.create_bank("Commerzbank")
    created_bank = investor.get_bank()
    assert isinstance(created_bank, Bank) and created_bank.get_name() == "Commerzbank"

def test_create_bank_twice(investor):
    investor.create_bank("Commerzbank")
    assert investor.create_bank("DSK") == False

def test_fund_bank(investor, bank):
    assert investor.fund_bank(10000)

def test_update_bank(investor, bank):
    assert investor.update_bank(bank_approval, bank_clear)

def test_fund_bank_fail(investor):
    assert investor.fund_bank(100000) == False

def test_update_bank_fail(investor):
    assert investor.update_bank(bank_approval, bank_clear) == False

def test_delete_bank_fail(investor):
    assert investor.delete_bank() == False