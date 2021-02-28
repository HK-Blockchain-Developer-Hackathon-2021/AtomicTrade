import json
import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn

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



def createAsset(algod_client, passphrase, html, doc_id, doc_name):
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    account_pk = mnemonic.to_public_key(passphrase)
    account_sk = mnemonic.to_private_key(passphrase)
    txn = AssetConfigTxn(
        sender=account_pk,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name=doc_id,
        asset_name=doc_name,
        manager=account_pk,
        reserve=account_pk,
        freeze=account_pk,
        clawback=account_pk,
        url=html,
        decimals=0)
    # Sign with secret key of creator
    stxn = txn.sign(account_sk)

    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(txid)

    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.

    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client,txid)

    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, account_pk, asset_id)
        print_asset_holding(algod_client, account_pk, asset_id)
    except Exception as e:
        print(e)

createAsset(algod_client, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )


# A1[Buyer] Create Letter of Credit 
# python3 sys-create-doc.py "derive load chapter decide hip actress rug pen helmet fantasy avoid damage disease error velvet add candy despair math assume lucky maple width above mass" HTML 5000 tEST
# A3[Shipper] Create Bill of Lading
# python3 sys-create-doc.py "safe problem mammal borrow federal rent hurdle worry pencil barely intact evil tower daring claw maximum hip inmate foil thought talk easily vanish absent boy" HTML BillofLading BOL

