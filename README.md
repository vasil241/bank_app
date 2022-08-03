# Intro
Hello! This is an application that I developed on Algorand for my bachelor thesis. Please go through this README file and test it out, hope you like it! 

## Setup 
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install [Algorand sandbox](https://github.com/algorand/sandbox)
3. Clone this repository
4. Install Python virtual environment in your project folder by writing in the console
```
python -m venv venv
source ./venv/Scripts/activate # Windows
source ./venv/bin/activate # Linux
```
5. Use Python interpreter from ./venv/Scripts/python.exe
6. Install PyTeal with `pip install pyteal` in the console
7. Go to the folder where you installed sandbox and run `./sandbox up testnet` - this will take a while probably
8. You should be ready to go and run the app, if you are lost, [this video](https://www.youtube.com/watch?v=V3d3VTlgMo8&list=PLpAdAjL5F75CNnmGbz9Dm_k-z5I6Sv9_x) could help 

### INSTALLATION AND GENERATE UML DIAGRAMS 

Please type the following command to get module compilation result.

```bash
python -v -m demo.py
```

Install the following linter 

```bash
pip install pylint
```

To publish the UML diagram, please type as below: 

```bash
pyreverse -o png -p SAMPLEOUTPUT .
```

To install all packages: 

```bash
pip install -r requirements.txt
```

## Just run it! 
Now that you have set up the required environment and cloned the project, you can explore the different folders and contents :) 
All of the app's logic is in the `assets` folder. There you can find all of the classes in `python_classes` and all of the smart contracts in `contracts`. 
Go to `demo.py` and read the instructions. Run it and follow closely the messages in the console. After it is done, you can compare all the results and see all of the history of the transactions using [AlgoExplorer](https://testnet.algoexplorer.io/).

## Testing

Run your test from a folder as follows: 

```bash
pytest tests/
```

### Branch Information

In order to download all branches that you need to use, please use the following commands

```bash 
git pull --all 
git fetch --all
```
## UML diagrams 

![Class diagram of the app](uml_diagrams/ClassDiagram.png)
![Sequence diagram - opening a bank account](uml_diagrams/SD_open-bank-account.jpg)
![Sequence diagram - making a deposit to the bank account](uml_diagrams/SD_deposit.jpg)
![Sequence diagram - withdraw from the bank account](uml_diagrams/SD_withdraw.jpg)
![Sequence diagram - transfer from one bank account to another](uml_diagrams/SD_transfer.jpg)

