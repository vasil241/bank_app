import base64
from algosdk.future.transaction import *
from pyteal import *
from algosdk.atomic_transaction_composer import *

def deploy(alog_client, creator_pk, app_name, approval, clear, global_ints, global_bytes, local_ints, local_bytes):
    # declare bank application state storage (immutable)
    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    print("Deploying {} application...".format(app_name))
    # Create bank
    app_id = create_app(alog_client, creator_pk, approval, clear, global_schema, local_schema)
    app_addr = logic.get_application_address(app_id)
    #Display results 
    print("Created a {} application with id and addr: {} {}".format(app_name, app_id, app_addr))

def create_app(algod_client, creator_pk, approval_program, clear_program, global_schema, local_schema):
    # get the address of the sender from its private key
    addr = account.address_from_private_key(creator_pk)
    # get node suggested parameters
    params = algod_client.suggested_params()
    
    # compile approval teal to bytecode
    appr_bytes = compile_program(algod_client, approval_program())
    # compile clear teal to bytecode
    clear_bytes = compile_program(algod_client, clear_program())
    
    # Create the transaction
    # the 3rd argument represents OnComplete and 0 is for NoOp 
    create_txn = ApplicationCreateTxn(addr, params, 0, appr_bytes, clear_bytes, global_schema, local_schema)
    # Sign it
    signed_txn = create_txn.sign(creator_pk)
    # Ship it
    tx_id = algod_client.send_transaction(signed_txn)

    try:
        # Wait for the result so we can return the app id
        result = wait_for_confirmation(algod_client, tx_id, 5)
    except Exception as err:
        print(err)
        return

    app_id = result['application-index']
    return app_id

def payment_txn(algod_client, sender_addr, sender_pk, amount, receiver, note):
    params = algod_client.suggested_params()
    unsigned_txn = PaymentTxn(sender=sender_addr, sp=params, receiver=receiver, amt=amount, note=note)
    signed_txn = unsigned_txn.sign(sender_pk)
    txid = algod_client.send_transaction(signed_txn)
    print("Sending a payment transaction")
    try:
        pmtx = wait_for_confirmation(algod_client, txid, 5)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(pmtx['confirmed-round']))

    except Exception as err:
        print(err)
        return
    return pmtx

def call_app(client, sender_addr, sender_pk, on_complete, app_id, note, appr_prog="", clear_prog="", app_args=[], foreign_apps=[], foreign_accs=[], fee=1000):
    # get node suggested parameters
    params = client.suggested_params()
    params.fee = fee
    # create unsigned transaction based on on_complete 
    txn = None
    match on_complete: 
        case 0: txn = ApplicationNoOpTxn(sender_addr, params, app_id, app_args, foreign_accs, foreign_apps, note=note)
        case 1: txn = ApplicationOptInTxn(sender_addr, params, app_id, note=note)
        case 2:    
            # if the client wishes to close his account, he should provide its app id in foreign apps array
            txn = ApplicationCloseOutTxn(sender_addr, params, app_id, foreign_apps=foreign_apps, note=note)
        case 3: txn = ApplicationClearStateTxn(sender_addr, params, app_id, foreign_apps=foreign_apps, note=note)
        case 4: txn = ApplicationUpdateTxn(sender_addr, params, app_id, appr_prog, clear_prog, note=note)
        case 5: txn = ApplicationDeleteTxn(sender_addr, params, app_id, note=note)

    # sign transaction
    signed_txn = txn.sign(sender_pk)
    tx_id = signed_txn.transaction.get_txid()
    # send transaction
    client.send_transactions([signed_txn])
    print("Sending an Application call from type {} to {}".format(on_complete, app_id))

    try:
        transaction_response = wait_for_confirmation(client, tx_id, 5)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

    except Exception as err:
        print(err)
        return
    print("Application called successfully")


def group_txns(algod_client, sender_addr, sender_pk, receiver_id, receiver_addr, amount, note1="", note2="", app_args=[], foreign_apps=[], foreign_accs=[], fee=1000):
    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(sender_pk)
    params = algod_client.suggested_params()
    params.fee = fee
    
    pay_txn = PaymentTxn(sender_addr, params, receiver_addr, amount, note=note1)
    txn1 = TransactionWithSigner(pay_txn, signer)
    atc.add_transaction(txn1)

    call_txn = ApplicationNoOpTxn(sender_addr, params, receiver_id, app_args, foreign_accs, foreign_apps, note=note2)
    txn2 = TransactionWithSigner(call_txn, signer)
    atc.add_transaction(txn2)

    result = atc.execute(algod_client, 5)
    txn1_result = algod_client.pending_transaction_info(result.tx_ids[0])
    txn2_result = algod_client.pending_transaction_info(result.tx_ids[-1])
    print("Group transaction successfully sent to bank")

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])