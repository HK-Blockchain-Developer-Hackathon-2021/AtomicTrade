import json
import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetTransferTxn, transaction

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "9GGJPGrPGu7H0LFDH1RjUa9VxJnuXNU059BOxuVB"
headers = {
   "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers);

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

def atomic_transfer(algodclient, txn1, txn2, buyer_mnemonic, carrier_mnemonic):
    
    #Buyer send letter of credit to Seller
    # txn1 
    
    #Shipper send bill of lading to Buyer 
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
    

#Txn1: Buyer transfer Letter of Credit to Seller
#Txn2: Shipper transfer Bill of Lading to Buyer

#passphrase 1 --> Buyer's 
#passphrase 2 --> Carrier's 
#atomic_transfer(algod_client, txn1, txn2, passphrase1, passphrase2)



