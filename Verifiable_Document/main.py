########## IMPORT PACKAGES ##########
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn

########## HELPER FUNCTIONS ##########
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

#   Utility function used to print created asset for account and assetid
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
            print(json.dumps(my_account_info['Sparams'], indent=4))
            break
    return

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
    return


########## SWITCHES ##########

# TODO: change keys into JSON requests
def txn_switch(txn_type): # param should be string
    txn = none
    if txn_type == 'create':
        txn = createDocument()
    elif txn_type == 'verify':
        txn = verifyDocument()
    elif txn_type == 'revoke':
        txn = revokeDocument()
    return txn

def printInformation(txn_type):
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        if txn_type == 'create':
            print_created_asset(algod_client, accounts[1]['pk'], asset_id)
            print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
        elif txn_type == 'verify':
            print("print what?")
    except Exception as e:
        print(e)
    return


########## SUBROUTINES ##########

def createDocument(pk, html_file, doc_id, doc_name):
    wrapDocument(html_file)
    txn = AssetConfigTxn(
        sender = pk,
        sp = params,
        total = 1,
        default_frozen = False,
        unit_name = doc_id,
        asset_name = doc_name,
        manager = pk,
        reserve = pk,
        freeze = pk,
        clawback = pk,
        url = html_file,
        decimals = 0 )
    return txn




# ----------------------- TEST ------------------------ #

Alice = "empower ill risk neglect manual piece kid hover goddess already casino labor crucial couch credit disorder below tennis magic whip away potato betray absorb reduce"
Bob = "require solution security ahead use jelly opera vessel absurd suit grape fork mix tattoo laundry chimney rebel example black swarm trim rib judge abandon nature"
Charlie = "purse traffic harbor almost shine artist keen wrist crime diesel afford bus impact eagle winner once unfold uphold foster relax order nerve glove able disease"

accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# ----------------------------------------------------- #


########## MAIN FUNCTION ##########

# Specify your node address and token. This must be updated.

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

# Get network params for transactions before every transaction.
params = algod_client.suggested_params()

txn = txn_switch(txn_type) #from userinput

# Sign with secret key of transaction creator
stxn = txn.sign(sk)

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print(txid)


# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client,txid)

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
printInformation(txn_type) # from user input
