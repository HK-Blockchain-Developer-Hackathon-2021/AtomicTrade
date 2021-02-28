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

def opt_in(algodclient, passphrase, asset_id):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    account_pk = mnemonic.to_public_key(passphrase)
    account_sk = mnemonic.to_private_key(passphrase)

    account_info = algod_client.account_info(account_pk)
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
            sender=account_pk,
            sp=params,
            receiver=account_pk,
            amt=0,
            index=asset_id)
        stxn = txn.sign(account_sk)
        txid = algod_client.send_transaction(stxn)
        print(txid)
        # Wait for the transaction to be confirmed
        wait_for_confirmation(algod_client, txid)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, account_pk, asset_id)

opt_in(algod_client, sys.argv[1], sys.argv[2])


# A2[Seller] Receive LOC
# python3 sys-opt-in.py "stamp rib atom limit crew defy case trophy helmet brain parrot surround enroll doctor cherry giggle large ride aerobic sponsor giggle skill helmet able assist" 14209111

# A1[Buyer] Receive BOL 
# update asset ID !
# python3 sys-opt-in.py "derive load chapter decide hip actress rug pen helmet fantasy avoid damage disease error velvet add candy despair math assume lucky maple width above mass" XXX[ID]


# Traceback (most recent call last):
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/algosdk/v2client/algod.py", line 72, in algod_request
#     resp = urlopen(req)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 222, in urlopen
#     return opener.open(url, data, timeout)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 531, in open
#     response = meth(req, response)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 640, in http_response
#     response = self.parent.error(
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 569, in error
#     return self._call_chain(*args)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 502, in _call_chain
#     result = func(*args)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/urllib/request.py", line 649, in http_error_default
#     raise HTTPError(req.full_url, code, msg, hdrs, fp)
# urllib.error.HTTPError: HTTP Error 400: Bad Request

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/algosdk/v2client/algod.py", line 77, in algod_request
#     raise error.AlgodHTTPError(json.loads(e)["message"], code)
# algosdk.error.AlgodHTTPError: msgpack decode error [pos 247]: cannot decode unsigned integer: unrecognized descriptor byte: a8/string|bytes

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "sys-opt-in.py", line 96, in <module>
#     opt_in(algod_client, sys.argv[1], sys.argv[2])
#   File "sys-opt-in.py", line 88, in opt_in
#     txid = algod_client.send_transaction(stxn)
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/algosdk/v2client/algod.py", line 172, in send_transaction
#     return self.send_raw_transaction(encoding.msgpack_encode(txn),
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/algosdk/v2client/algod.py", line 189, in send_raw_transaction
#     return self.algod_request("POST", req, data=txn, headers=headers, **kwargs)["txId"]
#   File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/algosdk/v2client/algod.py", line 79, in algod_request
#     raise error.AlgodHTTPError(e, code)
# algosdk.error.AlgodHTTPError: {"message":"msgpack decode error [pos 247]: cannot decode unsigned integer: unrecognized descriptor byte: a8/string|bytes"}
