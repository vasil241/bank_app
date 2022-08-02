import pytest
from python_classes import *
from .update_contracts import *

@pytest.fixture
def bank():
    algorand_account = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    p1 = Person("Vasil", algorand_account)
    p1.addRole("investor", Investor(p1))
    investor = p1.getRole("investor")
    investor.create_bank("Commerzbank")
    bank = investor.get_bank()

    yield bank
    if bank.deposit != None:
        bank.destroy("deposit")
    if bank.withdraw != None:
        bank.destroy("withdraw")
    if bank.transfer != None:
        bank.destroy("transfer")
    if bank.reference != None:
        bank.destroy("reference")
    investor.delete_bank()

def test_create(bank):
    assert bank.create("deposit") and bank.deposit != None

def test_create_twice(bank):
    bank.create("withdraw")
    assert bank.create("withdraw") == False

def test_create_fail(bank):
    # possible inputs for create are only "deposit", "withdraw", "transfer", "reference"
    # "loan" should fail
    assert bank.create("loan") == False

def test_update(bank):
    bank.create("transfer")
    assert bank.update("transfer", transfer_approval, transfer_clear)

def test_update_fail(bank):
    assert bank.update("transfer", transfer_approval, transfer_clear) == False

def test_destroy_fail(bank):
    assert bank.destroy("deposit") == False






