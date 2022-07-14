from algosdk import account, mnemonic
from pyteal import *

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("Generated a new address: {}".format(address))
    print("Generated a new private key: {}\n".format(private_key))
    return [address, private_key]