from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return [address, private_key]

def get_admin():
    #first string is the address of the admin, second is his private key
    return ["7TYDCADJOGINXKFLDBRWFDFLU3X3DISXZTYLRUYUWRI6W6NBN7C5KCZ4HQ","qr9eRQUOkvLQBWJ8rldwkfAf0UM64avQrijbTnpecrL88DEAaXGQ26irGGNijKum77GiV8zwuNMUtFHreaFvxQ=="]

# Uncomment the function call below and run the program to create a new account
# generate_algorand_keypair()

# Admin
# My address: 7TYDCADJOGINXKFLDBRWFDFLU3X3DISXZTYLRUYUWRI6W6NBN7C5KCZ4HQ
# My private key: qr9eRQUOkvLQBWJ8rldwkfAf0UM64avQrijbTnpecrL88DEAaXGQ26irGGNijKum77GiV8zwuNMUtFHreaFvxQ==
# My passphrase: vocal kit pencil theory catch device company ginger sort gadget return animal divide violin spirit thrive betray robust nephew unit virus nurse near absent option