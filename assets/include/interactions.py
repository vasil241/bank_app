from pyteal import *
from algosdk.future.transaction import *

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

# def call_app(client, sender_addr, sender_pk, on_complete, app_id, note, appr_prog="", clear_prog="", app_args=[], foreign_apps=[], foreign_accs=[]) :
#     # get node suggested parameters
#     params = client.suggested_params()
#     # create unsigned transaction based on on_complete 
#     txn = Cond(
#         [
#             on_complete == Int(0),
#             ApplicationNoOpTxn(sender_addr, params, app_id, app_args, foreign_accs, foreign_apps, note=note)
#         ],
#         [
#             on_complete == Int(1),
#             ApplicationOptInTxn(sender_addr, params, app_id, note=note)
#         ],
#         [
#             # if the client wishes to close his account, he should provide its app id in foreign apps array
#             on_complete == Int(2),
#             ApplicationCloseOutTxn(sender_addr, params, app_id, foreign_apps=foreign_apps, note=note)
#         ],
#         [
#             on_complete == Int(3),
#             ApplicationClearStateTxn(sender_addr, params, app_id, foreign_apps=foreign_apps, note=note)
#         ],
#         [
#             on_complete == Int(4),
#             ApplicationUpdateTxn(sender_addr, params, app_id, appr_prog, clear_prog, note=note)
#         ],
#         [
#             on_complete == Int(5),
#             ApplicationDeleteTxn(sender_addr, params, app_id, note=note)
#         ]
#     )

#     # sign transaction
#     signed_txn = txn.sign(sender_pk)
#     tx_id = signed_txn.transaction.get_txid()
#     # send transaction
#     client.send_transactions([signed_txn])
#     print("Sending an Application call from type {} to {}".format(on_complete, app_id))

#     try:
#         transaction_response = transaction.wait_for_confirmation(client, tx_id, 5)
#         print("TXID: ", tx_id)
#         print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

#     except Exception as err:
#         print(err)
#         return
#     print("Application called successfully")