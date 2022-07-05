from algosdk import *
from algosdk.v2client import algod
from algosdk.future.transaction import *
from pyteal import *

from bank import bank_approval, bank_clear
from include.account import get_admin, generate_algorand_keypair
from include.deploy import deploy

client = algod.AlgodClient("a" * 64, "http://localhost:4001")
admin_addr, admin_pk = get_admin()[0], get_admin()[1]

def demo():
    deploy(client, admin_pk, "bank", bank_approval, bank_clear, 1, 1, 1, 1)
    # bank to test id: 98125498 addr: H6YVO2QM4WMJF5SVCUC566VC4WIAPHBEX2SYB2RGQGA77STRIYXOWME47Q
    

if __name__ == "__main__":
    demo()