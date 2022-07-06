from algosdk import *
from algosdk.v2client import algod
from algosdk.future.transaction import *
from pyteal import *

from bank import bank_approval, bank_clear
from include.account import get_admin, get_clientA, get_clientB
from include.deploy import deploy
from include.interactions import payment_txn, call_app

client = algod.AlgodClient("a" * 64, "http://localhost:4001")
admin_addr, admin_pk = get_admin()[0], get_admin()[1]
clientA_addr, clientA_pk = get_clientA()[0], get_clientA()[1]
clientB_addr, clientB_pk = get_clientB()[0], get_clientB()[1]

def demo():
    pass
    # deploy(client, admin_pk, "bank", bank_approval, bank_clear, 1, 1, 1, 1)
    # bank to test id: 98520418 addr: NXF44OMVLLF3QHQFVIVXJ6CTLGYR3KNBCY5SJ4VHS2AA3ASBQMZTREWIQU
    
    # a payment txn from the admin to the newly created bank to fund it
    # payment_txn(client, admin_addr, admin_pk, 2000000, "NXF44OMVLLF3QHQFVIVXJ6CTLGYR3KNBCY5SJ4VHS2AA3ASBQMZTREWIQU", "Funding the bank")
    
    #admin opts into the bank
    # call_app(client, admin_addr, admin_pk, Int(1), 98520418, "Admin opts into the bank")


if __name__ == "__main__":
    demo()