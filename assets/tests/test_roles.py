import pytest
from python_classes import *

# setup
@pytest.fixture
def person():
    algorand_account = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    p = Person("Vasil", algorand_account)
    return p

def test_addRole(person):
    person.addRole("client", Client(person))
    assert person.hasRole("client") and len(person.getRoles()) == 1

def test_addRoles(person):
    person.addRole("investor", Investor(person))
    person.addRole("client", Client(person))
    dict_roles = person.getRoles()
    assert set(("investor","client")).issubset(dict_roles.keys()) and len(dict_roles) == 2

def test_addRole_fail(person):
    # when you try to add the same role twice, it should fail
    person.addRole("investor", Investor(person))
    assert person.addRole("investor", Investor(person)) == False

def test_removeRole(person):
    person.addRole("client", Client(person))
    if person.hasRole("client"):
        person.removeRole("client")
    assert person.hasRole("client") == False and len(person.getRoles()) == 0

def test_removeRole_fail(person):
    # if you try to remove a role that the person doesn't have - it should fail
    assert person.removeRole("client") == False

def test_getRole(person):
    person.addRole("investor", Investor(person))
    person.addRole("client", Client(person))
    client = person.getRole("client")
    investor = person.getRole("investor")
    assert isinstance(client, Client) and isinstance(investor, Investor)
