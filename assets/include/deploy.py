import base64
from algosdk.future.transaction import *

def deploy(client, admin_pk, app_name, approval, clear, global_ints, global_bytes, local_ints, local_bytes, app_args):
    # declare bank application state storage (immutable)
    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    print("Deploying {} application...".format(app_name))
    # Create bank
    app_id = create_app(client, admin_pk, approval, clear, global_schema, local_schema, app_args)
    app_addr = logic.get_application_address(app_id)
    #Display results 
    print("Created a {} application with id and addr: {} {}".format(app_name, app_id, app_addr))

def create_app(client, pk, approval_program, clear_program, global_schema, local_schema, app_args):
    # get the address of the sender from its private key
    addr = account.address_from_private_key(pk)
    # get node suggested parameters
    params = client.suggested_params()
    
    # compile approval teal to bytecode
    appr_bytes = compile_program(client, approval_program())
    # compile clear teal to bytecode
    clear_bytes = compile_program(client, clear_program())
    
    # Create the transaction
    # the 3rd argument represents OnComplete and 0 is for NoOp 
    create_txn = ApplicationCreateTxn(addr, params, 0, appr_bytes, clear_bytes, global_schema, local_schema, app_args)
    # Sign it
    signed_txn = create_txn.sign(pk)
    # Ship it
    tx_id = client.send_transaction(signed_txn)

    try:
        # Wait for the result so we can return the app id
        result = wait_for_confirmation(client, tx_id, 5)
    except Exception as err:
        print(err)
        return

    app_id = result['application-index']
    return app_id

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])
