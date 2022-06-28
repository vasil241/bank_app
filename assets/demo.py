from algosdk import *
from algosdk.v2client import algod
from algosdk.future.transaction import *

from bank import bank_approval, bank_clear
from include.account import get_admin, generate_algorand_keypair
from include.deploy import deploy

client = algod.AlgodClient("a" * 64, "http://localhost:4001")
admin_addr, admin_pk = get_admin()[0], get_admin()[1]

def demo():
    pass

if __name__ == "__main__":
    demo()