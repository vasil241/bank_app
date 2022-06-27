from algosdk import *
from algosdk.v2client import algod
from algosdk.future.transaction import *

from bank import bank_approval, bank_clear
from include.account import get_admin, generate_algorand_keypair
from include.deploy import create_app

client = algod.AlgodClient("a" * 64, "http://localhost:4001")
admin_addr, admin_pk = get_admin()[0], get_admin()[1]

def deploy(app_name, approval, clear, global_ints, global_bytes, local_ints, local_bytes):
    # declare bank application state storage (immutable)
    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    print("Deploying {} application...".format(app_name))
    # Create bank
    app_id = create_app(client, admin_pk, approval, clear, global_schema, local_schema)
    app_addr = logic.get_application_address(app_id)
    #Display results 
    print("Created a {} application with id and addr: {} {}".format(app_name, app_id, app_addr))

def demo():
    pass
    # bank id: 97142346
    # bank addr: JSOJYMDRP7V75MSFTDFP25LT3H5LXGN4DCV2AVQDXEZXOBVDWDNJD3KZQI

if __name__ == "__main__":
    demo()