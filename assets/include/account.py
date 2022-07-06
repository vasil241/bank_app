from algosdk import account, mnemonic
from pyteal import *

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return [address, private_key]

def get_admin():
    #first string is the address of the admin, second is his private key
    return ["FQ6VLZAUMQA64PRTQVKXJWMK6TUMEY5DBFHR2VOT3MUUSMBGKJHGO66I74","N48DIZPgRk0qreiuqxZ4iuZT27GMMVLfc6q/U41IZ1YsPVXkFGQB7j4zhVV02Yr06MJjowlPHVXT2ylJMCZSTg=="]

def get_clientA():
    return ["4RHDETQC4KDHMUQ22QLEX7B6FY2TSNHZO6XVYASAE23WLU7POKTP3NZ6G4", "NzdILYFcxenkVvj2I8WReP4JVTnTBejxAw7n8vBXjdzkTjJOAuKGdlIa1BZL/D4uNTk0+XevXAJAJrdl0+9ypg=="]

def get_clientB():
    return ["BQV2EEYE23Q2QMBSKJ72RUJVDDRO4TNW7A36WKGPTCBK6B5BDAK34OWAYI", "KBmXTn9C8ibGm2prtmtpqFCw2Wb7lG5QdqeCn94BboMMK6ITBNbhqDAyUn+o0TUY4u5Ntvg36yjPmIKvB6EYFQ=="]

# Uncomment the function call below and run the program to create a new account
# generate_algorand_keypair()

# Admin
# My address: FQ6VLZAUMQA64PRTQVKXJWMK6TUMEY5DBFHR2VOT3MUUSMBGKJHGO66I74
# My private key: N48DIZPgRk0qreiuqxZ4iuZT27GMMVLfc6q/U41IZ1YsPVXkFGQB7j4zhVV02Yr06MJjowlPHVXT2ylJMCZSTg==
# My passphrase: tragic athlete mountain ankle miss nation harsh trim into follow despair hamster pond item grain cover tumble sorry steel desk boy split rebel able item

# Client A
# My address: 4RHDETQC4KDHMUQ22QLEX7B6FY2TSNHZO6XVYASAE23WLU7POKTP3NZ6G4
# My private key: NzdILYFcxenkVvj2I8WReP4JVTnTBejxAw7n8vBXjdzkTjJOAuKGdlIa1BZL/D4uNTk0+XevXAJAJrdl0+9ypg==
# My passphrase: tragic camp note siege melt denial rescue weapon learn behind employ travel become fetch oil alarm dial average mandate common tiger field tongue absorb door

# Client B
# My address: BQV2EEYE23Q2QMBSKJ72RUJVDDRO4TNW7A36WKGPTCBK6B5BDAK34OWAYI
# My private key: KBmXTn9C8ibGm2prtmtpqFCw2Wb7lG5QdqeCn94BboMMK6ITBNbhqDAyUn+o0TUY4u5Ntvg36yjPmIKvB6EYFQ==
# My passphrase: celery fragile point child tonight meadow taste hedgehog sniff put cruise appear gaze reopen swamp neutral assist sun father wealth rule lesson bread above ring