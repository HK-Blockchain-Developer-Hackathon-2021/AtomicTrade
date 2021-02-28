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

def transfer_asset_holding_return_txn(algodclient, passphrase, receiver, asset_id):
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    account_pk = mnemonic.to_public_key(passphrase)
    account_sk = mnemonic.to_private_key(passphrase)

    txn = AssetTransferTxn(
        sender=account_pk, 
        sp=params,
        receiver=receiver, 
        amt=1,
        index=asset_id)
    return txn 

transfer_asset_holding_return_txn(algod_client, sys.argv[1], sys.argv[2], sys.argv[3])

# A1[Buyer] Transfer Letter of Credit to A2[Seller]
# python3 sys-transfer.py "derive load chapter decide hip actress rug pen helmet fantasy avoid damage disease error velvet add candy despair math assume lucky maple width above mass" EYM36UXESOP4ZIF26ARCPXVIBHTGABOTSSARNN66TJ65GYDINZIRH27Y3I 14209111

# no output error


# A3[Shipper] Transfer Bill of Lading to A1[Buyer]
# !! Update Asset-ID
# python3 sys-transfer.py "safe problem mammal borrow federal rent hurdle worry pencil barely intact evil tower daring claw maximum hip inmate foil thought talk easily vanish absent boy" TDNGCYLB3ZAJDXINUESSNTOEVHROULFX3SJ3F34T6JU6VFY5PH2LJ7GD6I XXX{ID}

