from algosdk import *
from pyteal import *
from python_classes import *

def demo():
    pass
    # '''
    # 1. Run demo() and you will see in the console 3 created accounts with public addr and private key generated
    # 2. fund the addresses with Algos from https://bank.testnet.algorand.network/ (10 Algos pro account are needed)
    # 3. After you are done with the previous 2 steps, comment out lines 18-20 with a # 
    # 4. Now write the address and private key in the variables account_1 , account_2, account_3 - 0 index is the address, 1 index is the private key
    #    Uncomment the rest of the code and run... Follow the messages in the console and check also https://testnet.algoexplorer.io/
    
    # If you wish you can already check the history of the addresses given below by visiting https://testnet.algoexplorer.io/ 
    # and typing in the address in the search bar
    # '''
    
    account_1 = ["Z5M3VNOXWUKYBXS7YFG5567A6IIEJGNULU2XAXRMVJ5TDUE6ZUOIRLHDVA", "umlKBQf6DaQXoNQamQnj4vQfLAfHt2f+SdkW7PtkTJXPWbq117UVgN5fwU3e++DyEESZtF01cF4sqnsx0J7NHA=="]
    account_2 = ["X7FUIUOTDJ3AKVHFN3WAPEJXA2HH5K2IWKNEMEIHAK527YND75VYALTUC4", "UkoEli+7KJQ73A0yFOAD4QnubU3QJY/LouCC1U1Dr+m/y0RR0xp2BVTlbuwHkTcGjn6rSLKaRhEHAruv4aP/aw=="]
    # account_3 = ["KSOBHAKZMD2I7SJC7CUHBWBYDSKTDB37USOYBA4IOPIZ3K3IYGMIGRVIBA", "Syj40FEBTK8I9Tml3p8GrPiz4GTXKG1ElBhNCnaTnyxUnBOBWWD0j8ki+Khw2DgclTGHf6SdgIOIc9Gdq2jBmA=="]

    # '''
    # Creating the investor and clients - investor can create the bank, clients can 
    # use it and open bank accounts there all of them are wired to an algorand account
    # '''
    person1 = Person("Vasil", account_1)
    person2 = Person("Bob", account_2)
 
    person1.addRole("investor", Investor(person1))
    person2.addRole("client", Client(person2))
    investor = person1.getRole("investor")
    clientB = person2.getRole("client")

    # ''' investor creates a bank object which is wired to a bank smart contract '''
    investor.create_bank("DSK")
    
    bank = investor.get_bank()

    # ''' bank (parent) creates further smart contracts (children) with additional required functionality ''' 
    # bank.create("deposit")
    # bank.create("withdraw")
    # bank.create("transfer")
    bank.create("reference")
    bank.create("withdraw")
    
    # ''' 
    # Bob registers wishes to register himself into the bank and open an account with initial deposit 0.3 Algo
    # The bank account created is a smart contract created by the bank with an owner Bob
    # '''
    clientB.open_bank_account(bank, 100000)
    clientB.withdraw(50000)
    # ''' Bob decides to deposit another 0.1 Algo into his account '''
    # clientA.deposit(100000)
    # ''' Bob decides to withdraw 0.1 Algo from his account '''
    # clientA.withdraw(100000)
    
    # ''' Alice also decides to open an account with bank and deposit 0.3 Algo '''
    # person2.addRole("client", Client(person2))
    # person2.hasRole("client")
    # clientB = person2.getRole("client")
    
    # clientB.register_bank(bank)
    # clientB.open_bank_account(300000)
    
    # ''' Bob transfers from his bank account 0.1 Algo to Alice's bank account '''
    # clientA.transfer(clientB, 100000)
    
    # ''' Alice and Bob wish to close their accounts and no longer be clients of the bank '''
    # person1.getRoles()
    # person2.getRoles()

    # clientB.leave_bank()
    # person2.removeRole("client")
    
    # clientA.leave_bank()
    # person1.removeRole("client")

    # person1.getRoles()
    # person2.getRoles()

    # ''' Bank no longer will exist, it deletes first all of its children (smart contracts) ''' 
    # bank.destroy("deposit")
    # bank.destroy("withdraw")
    # bank.destroy("transfer")
    # bank.destroy("reference")
    
    # ''' Investor closes the bank '''
    # investor.delete_bank()
    # person1.removeRole("investor")
    # person1.getRoles()


if __name__ == "__main__":
    demo()