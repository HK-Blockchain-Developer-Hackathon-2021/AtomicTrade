import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetTransferTxn, transaction

mnemonic1 = "derive load chapter decide hip actress rug pen helmet fantasy avoid damage disease error velvet add candy despair math assume lucky maple width above mass"
mnemonic2 = "stamp rib atom limit crew defy case trophy helmet brain parrot surround enroll doctor cherry giggle large ride aerobic sponsor giggle skill helmet able assist"
mnemonic3 = "safe problem mammal borrow federal rent hurdle worry pencil barely intact evil tower daring claw maximum hip inmate foil thought talk easily vanish absent boy"

accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

# asset_id = 14201143;

def opt_in(algodclient, receiver, receiver_sk, asset_id):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    account_info = algod_client.account_info(receiver)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=receiver,
            sp=params,
            receiver=receiver,
            amt=0,
            index=asset_id)
        stxn = txn.sign(receiver_sk)
        txid = algod_client.send_transaction(stxn)
        print(txid)
        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, receiver, asset_id)

#opt_in(algod_client, accounts[3]['pk'], accounts[3]['sk'], asset_id)

def transfer_asset_holding(algodclient, account, account_sk, receiver, asset_id):
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    txn = AssetTransferTxn(
        sender=account, #accounts[1]['pk'],
        sp=params,
        receiver=receiver, #accounts[3]["pk"],
        amt=1,
        index=asset_id)
    stxn = txn.sign(account_sk)
    txid = algod_client.send_transaction(stxn)
    print(txid)
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid)
    # The balance should now be 10.
    print_asset_holding(algod_client, receiver, asset_id)
    return stxn

def transfer_asset_holding_return_txn(algodclient, account, account_sk, receiver, asset_id):
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True
    txn = AssetTransferTxn(
        sender=account, #accounts[1]['pk'],
        sp=params,
        receiver=receiver, #accounts[3]["pk"],
        amt=1,
        index=asset_id)
    return txn 
    #stxn = txn.sign(account_sk)
    #txid = algod_client.send_transaction(stxn)
    #print(txid)
    # Wait for the transaction to be confirmed
    #wait_for_confirmation(algod_client, txid)
    # The balance should now be 10.
    #print_asset_holding(algod_client, receiver, asset_id)
    #return stxn

#transfer_asset_holding(algod_client, accounts[1]['pk'], accounts[1]['sk'],accounts[3]['pk'], asset_id)

#Account 1 --> Buyer
#Account 2 --> Carrier
#Account 3 --> Seller

def atomic_transfer(algodclient, txn1, txn2, buyer_pk, buyer_mnemonic, carrier_pk, carrier_mnemonic):
    #prepare transaction 1: Account 1 transfer document to Account 2
    #Buyer send letter of credit to Seller
    # txn1 

    #prepare transaction 1: Account 2 transfer document to Account 1
    #Seller send bill of lading to Buyer 
    # txn2

    # group transactions
    print("Grouping transactions...")
    group_id = transaction.calculate_group_id([txn1, txn2])
    print("... computed groupId: ", group_id)
    txn1.group = group_id
    txn2.group = group_id

    # sign transactions
    print("Signing transactions ...")
    stxn1 = txn1.sign(mnemonic.to_private_key(buyer_mnemonic))
    print(" ... buyer signed txn 1, i.e. to transfer Letter of Credit to seller")
    stxn2 = txn2.sign(mnemonic.to_private_key(carrier_mnemonic))
    print(" ... carrier signed txn 2, i.e. to transfer Bill of Lading to buyer")
    
    # assemble transaction group 
    print("Assembling transaction group ...")
    signedtxns = [stxn1, stxn2]

    # send transaction 
    print("Sending transaction group...")
    tx_id = algodclient.send_transactions(signedtxns)

    #wat for confirmation
    wait_for_confirmation(algodclient, tx_id)
    
    # display confirmed transaction group
	# tx1
    confirmed_txn = algodclient.pending_transaction_info(txn1.get_txid())
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

	# tx2
    confirmed_txn = algodclient.pending_transaction_info(txn2.get_txid())
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    
#Account 1 --> Buyer
#Account 2 --> Carrier
#Account 3 --> Seller

letter_of_credit_id = 14201392
#opt_in(algod_client, accounts[3]['pk'], accounts[3]['sk'], letter_of_credit_id)
#txn1 = transfer_asset_holding_return_txn(algod_client, accounts[1]['pk'], accounts[1]['sk'], accounts[3]['pk'], letter_of_credit_id)

bill_of_lading_id = 14201400
#bill of lading created by Carrier [--> [SKIPPED] sent to seller -->] sent to buyer
#opt_in(algod_client, accounts[1]['pk'], accounts[1]['sk'], bill_of_lading_id)
#txn2 = transfer_asset_holding_return_txn(algod_client, accounts[2]['pk'], accounts[2]['pk'], accounts[1]['pk'], bill_of_lading_id)

#atomic_transfer(algod_client, txn1, txn2, accounts[1]['pk'], mnemonic1, accounts[2]['pk'], mnemonic2)

def print_summary(algod_client, accounts1, accounts2, accounts3, bill_of_lading_id, letter_of_credit_id):
    print_asset_holding(algod_client, accounts2, bill_of_lading_id)
    print_asset_holding(algod_client, accounts1, bill_of_lading_id)
    print_asset_holding(algod_client, accounts3, letter_of_credit_id)
    print_asset_holding(algod_client, accounts1, letter_of_credit_id)

print_summary(algod_client, accounts[1]['pk'], accounts[2]['pk'], accounts[3]['pk'], bill_of_lading_id, letter_of_credit_id)

