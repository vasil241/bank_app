from algosdk import *
from pyteal import *

from python_classes.Client import *
from python_classes.Investor import *
from python_classes.Bank import *
from helpers.account import generate_algorand_keypair

def demo():
    pass
    # new_account = generate_algorand_keypair() Generate a new Algorand account and fund it using https://dispenser.testnet.aws.algodev.network/
    # new_account = ["G56ITUNSGJJSAWQ3AVAV5IRODJB76CJCUYI3MDOVPWIR53DCXGDJDEDZHA", "7oC9Jd+ESBYRwrhJTsJ2nyaqwvWpd+mr4yfT+e1D/e83fInRsjJTIFobBUFeoi4aQ/8JIqYRtg3VfZEe7GK5hg=="] # temporary
    # investor1 = Investor("Vasil", new_account)
    # investor1.create_bank("DSK")
    # investor1.bank = Bank("DSK", new_account[0], new_account[1], 99615274, "YF7QGC22X5JI5K4YKTEI4GRAIZDHILQ772OZLKUNCONG7SFWEXT6KJQTEY") # temporary
    # bank = investor1.get_bank()
    # investor1.fund_bank(2000000)
    # investor1.register_bank(bank)
    # bank.create("deposit")
    # bank.deposit = [99495672, "3SWH434MY736CXTYF42UAQEXLVCBSBZBDUTE5QIZHSAHYIXWD5EHZAUXKM"] # temporary
    # bank.create("reference")
    # bank.bank_account_reference = [99500065, "JN6G2OF77YLEGVB7MB7W3JXSFS6VXRZAWPMZELDDOUTM7ITOLSQ4PNGTNE"] # temporary
    # bank.create("withdraw")
    # bank.withdraw = [99514242, "I6YOM7RLHUAYHB2HNINJ6QEZ5YEOQU4WAGZCNH2XE2XOOG5JB4MZHFMNSQ"] # temporary
    # bank.create("transfer")
    # bank.transfer = [99500586, "XRAZVB3JJXSFI5JRWQEVM6NCK3HSF443S5YVRX57TAOTAK6BVY2ZF3G4RQ"] # temporary
    
    # new_account2 = generate_algorand_keypair()
    # new_account2 = ["W6YQC4VWR7XTFDAOIDRMEH3DC47B6AWNRPAGRNHJJRXIR76MGWYRGPEFZU", "8nvRtb+o0eJHOERe0zpbieOJ3yjgNneaOKxJiK8r4WO3sQFyto/vMowOQOLCH2MXPh8CzYvAaLTpTG6I/8w1sQ=="] # temporary
    # clientA = Client("Boris", new_account2)
    # clientA.register_bank(bank)
    # clientA.bank = bank # temporary
    
    
    #clientA.open_bank_account(300000)
    # clientA.bank_account = [99502820, "EIGEVJFRI52PY76CVDHQOGXKVCMLFABMZDBFHPEGEKBAGFJA3Y5FBCNV2I"] # temporary
    # clientA.deposit(100000)
    # clientA.withdraw(100000)
    # new_account3 = generate_algorand_keypair()
    # new_account3 = ["X24I2QSEHQSKW2WVYFXXIRFE7JVQ77BE6Q3XCVO62JNJVOAJMNP376V2OE", "H+pVGtZFCU30/kfzwTQ8gvKqLhAWaM3yE4Q5VjBcSX++uI1CRDwkq2rVwW90RKT6aw/8JPQ3cVXe0lqauAljXw=="] # temporary
    # clientB = Client("Anatoli", new_account3)
    #clientB.register_bank(bank)
    # clientB.bank = bank # temporary
    # clientB.open_bank_account(300000)
    # clientB.bank_account = [99595351, "Q55YHBOTMSIQ3P63QDVKRQ6CPZ63I3VCRCGXOTKGTT5KE6JG5RJ7PAASAU"] # temporary
    # clientA.transfer(clientB, 100000)
    # clientB.leave_bank()
    # clientA.leave_bank()
    # bank.destroy("deposit")
    # investor1.delete_bank()


if __name__ == "__main__":
    demo()