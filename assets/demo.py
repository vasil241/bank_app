import base64
from algosdk import *
from algosdk.v2client import algod
from algosdk.future.transaction import *
from pyteal import *

from bank import bank_approval, bank_clear
from reference import reference_approval, reference_clear
from deposit import deposit_approval, deposit_clear
from withdraw import withdraw_approval, withdraw_clear
from transfer import transfer_approval, transfer_clear
from include.account import get_admin, get_clientA, get_clientB
from include.interactions import payment_txn, call_app, deploy, group_txns

client = algod.AlgodClient("a" * 64, "http://localhost:4001")
admin_addr, admin_pk = get_admin()[0], get_admin()[1]
clientA_addr, clientA_pk = get_clientA()[0], get_clientA()[1]
clientB_addr, clientB_pk = get_clientB()[0], get_clientB()[1]

def compile_program(source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def demo():
    pass
    # deploy(client, admin_pk, "bank", bank_approval, bank_clear, 2, 1, 1, 1)
    # bank to test id: 98926566 addr: MFWPRM2BCE4AZ7T6IAIWAYME6OPYBQVQTMK4VPKGP4LCC5OLRDXCTUXZCE
    
    # payment_txn(client, admin_addr, admin_pk, 2000000, "MFWPRM2BCE4AZ7T6IAIWAYME6OPYBQVQTMK4VPKGP4LCC5OLRDXCTUXZCE", "Funding the bank")
    
    # call_app(client, clientB_addr, clientB_pk, 1, 98926566, "Client B opts into the bank")
    
    # appr_bytes = compile_program(reference_approval())
    # clear_bytes = compile_program(reference_clear())
    # call_app(client, admin_addr, admin_pk, 0, 98926566, "Creating the reference smart contract", app_args=["create", appr_bytes, clear_bytes, 2, 0])
    # Reference contract 
    # 98926733

    # group_txns(client, clientB_addr, clientB_pk, 98926566,
    #  "MFWPRM2BCE4AZ7T6IAIWAYME6OPYBQVQTMK4VPKGP4LCC5OLRDXCTUXZCE", 300000,
    #  "Client B sends money to bank", "Client B wishes to open a bank account",
    #  app_args=["open_acc"], foreign_apps=[98926733])
    # bank account Client A - 98927148 L276RPOOUUYV3IDPXAKDO6L6ZXOTSVTAUKLCTRA3TJGFIMKOMZTTSOXQS4
    # bank account Client B - 99180574 3NFB3DDVBUXHLHGPNM2FMLIN6VPG4SFLBD4R33EVUXPA4ZUASJNUK3WMGU

    # appr_bytes = compile_program(transfer_approval())
    # clear_bytes = compile_program(transfer_clear())
    # call_app(client, admin_addr, admin_pk, 0, 98926566, "Creating the transfer smart contract", app_args=["create", appr_bytes, clear_bytes, 0, 0])
    # Deposit contract 98927431 NWYOXXQEFU3V4MHI6ATHZMTOBY5LTXMBGW4MEFJRXYSUR43MJJUR57MMYE
    # Withdraw contract 98936027 XEABVCK2VTQSU6UVRFGEMSX7TKSIHNGGNJHLYU4YFP7BDT5JMCTP27VAJQ
    # Transfer contract 99180919 6AA5FCWPZDDJBDE4UTERE7Y5NSDVQMMLHDKHFTG22HE5SSB27VQL6PCNHA

    # group_txns(client, clientA_addr, clientA_pk, 98926566,
    #  "MFWPRM2BCE4AZ7T6IAIWAYME6OPYBQVQTMK4VPKGP4LCC5OLRDXCTUXZCE", 100000,
    #  "Client A deposits into bank account", "Client A calls bank",
    #  app_args=["deposit"], foreign_apps=[98927431, 98927148], foreign_accs=["NWYOXXQEFU3V4MHI6ATHZMTOBY5LTXMBGW4MEFJRXYSUR43MJJUR57MMYE", "L276RPOOUUYV3IDPXAKDO6L6ZXOTSVTAUKLCTRA3TJGFIMKOMZTTSOXQS4"])

    # withdraw some funds 
    # call_app(client, clientA_addr, clientA_pk, 0, 98926566, "Withdraw some funds", app_args=["withdraw","20000"], foreign_apps=[98936027, 98927148], fee=1000)

    # Close a bank account
    # call_app(client, admin_addr, admin_pk, 2, 98912369, "Admin wants to close his account", foreign_apps=[98912943], fee=3000)

    # Delete a child 
    # call_app(client, admin_addr, admin_pk, 0, 98926566, "Delete withdraw contract", app_args=["destroy"], foreign_apps=[98929512])

    # Delete bank 
    # call_app(client, admin_addr, admin_pk, 5, 98912369, "Delete bank")

    # transfer from A to B
    # call_app(client, clientA_addr, clientA_pk, 0, 99180919, "Client A wishes to make a transfer", app_args=[100000], foreign_apps=[98927148, 98926566], foreign_accs=["MFWPRM2BCE4AZ7T6IAIWAYME6OPYBQVQTMK4VPKGP4LCC5OLRDXCTUXZCE", clientB_addr, "3NFB3DDVBUXHLHGPNM2FMLIN6VPG4SFLBD4R33EVUXPA4ZUASJNUK3WMGU"])


if __name__ == "__main__":
    demo()