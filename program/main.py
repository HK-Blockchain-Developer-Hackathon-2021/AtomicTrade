########## IMPORT PACKAGES ##########
from __future__ import division, unicode_literals 
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, transaction

import hashlib

########## CONNECT TO ALGORAND TESTNET ##########

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "OMct1kUCDXBZqIBUGGPu3icybHj3q6R77sGLucCb"
headers = {
    "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)
params = algod_client.suggested_params() # Get network params for transactions before every transaction.

params.fee = 1000
params.flat_fee = True
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
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print(scrutinized_asset['index'])
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
            print(scrutinized_asset['asset-id'])
            break
    return

# parse JSON
def parseJSON(inp, val):
    import json
    y = json.loads(inp)
    if (val == 'method'):
        return y[0]
    elif (val == 'doc-id'):
        return y[1]
    elif (val == 'doc-name'):
        return y[2]
    elif (val == 'hashed-doc'):
        return y[3]
    elif (val == 'passphrase'):
        return y[4]

def checkAssets(key, val, account_info):
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx += 1        
        if (scrutinized_asset[key] == val):
            return True
    return False

########## SUBROUTINES ##########

def wrapDocument(doc):
    import hashlib
    return (hashlib.sha256(doc.encode()).digest())

def createDocument(pk, doc_hash, doc_id, doc_name):
    from codecs import decode
    try:
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
                metadata_hash = (decode(doc_hash, "hex")),
                decimals = 0 )

        print (txn)
    except:
        print("wtf")

    return txn

def revokeDocument(pk, asset_id):
    txn = AssetConfigTxn(
        sender = pk,
        sp = params,
        index = asset_id,
        strict_empty_address_check = False
        )
    return txn

from algosdk.v2client import indexer    
from base64 import b64decode
from codecs import decode
indexer_client = indexer.IndexerClient("", algod_address, headers)
def verifyDocument(doc_name, owner_address, hashed_doc):
    
    response = indexer_client.search_assets(name=doc_name)
    print("ara")
    print("Asset search: " + json.dumps(response, indent=2, sort_keys=True)) #<<< FYI
    # I can check (1) existence (2) uniqueness (3) authenticity (4) integrity
    # "assets": [], => non-existence
    doc_info = response["assets"]
    if len(doc_info) <= 0:
        print("This document does not exist!")
    # "deleted": false => existence
    elif doc_info[0]["deleted"] == "true":
        print("This document has been revoked!")
    # "assets": a_list, if len(a_list) == 1 && total == 1, then the doc was uniquely created
    elif len(doc_info) != 1:
        print("WARNING > This document was not uniquely created!")
    # "creator": a_pk == pk => authenticity
    elif doc_info[0]["params"]["creator"] != owner_address:
        print("The input address is wrong! The document owner should be", doc_info[0]["params"]["creator"],"instead!")
    # "metadata-hash": some_hash, if some_hash == hashed_doc, then the hashed_doc is not tampered
    elif b64decode(doc_info[0]["params"]["metadata-hash"]) != decode(hashed_doc, "hex"):
        print("WARNING > You input document has been tampered!")
    else:
        print("The document is successfully verified!")
    return None

def optinDocument(algod_client, pk, asset_id):

    account_info = algod_client.account_info(pk)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            print(holding)
            break
    #print(holding)
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        try:
            txn = AssetTransferTxn(
                sender = pk,
                sp = params,
                receiver = pk,
                amt = 0,
                index = asset_id)
            print("yes")
        except:
            print("aaa")
        return txn
        
    return None

def singleTransfer(pk, receiver, asset_id):
    txn = AssetTransferTxn(
        sender = pk, 
        sp = params,
        receiver = receiver, 
        amt = 1,
        index = asset_id)    
    return txn 

def atomicTransfer(algod_client, txn1, txn2, buyer_sk, carrier_sk):
    
    #txn1: Buyer send letter of credit to Seller
    # txn2: Shipper send bill of lading to Buyer 
    
    # group transactions
    print("Grouping transactions...")
    group_id = transaction.calculate_group_id([txn1, txn2])
    print("... computed groupId: ", group_id)
    txn1.group = group_id
    txn2.group = group_id

    # sign transactions
    print("Signing transactions ...")
    stxn1 = txn1.sign(buyer_sk)
    print(" ... buyer signed txn 1, i.e. to transfer Letter of Credit to seller")
    stxn2 = txn2.sign(carrier_sk)
    print(" ... carrier signed txn 2, i.e. to transfer Bill of Lading to buyer")
    
    # assemble transaction group 
    print("Assembling transaction group ...")
    signedtxns = [stxn1, stxn2]

    # send transaction 
    print("Sending transaction group...")
    tx_id = algod_client.send_transactions(signedtxns)

    #wat for confirmation
    wait_for_confirmation(algod_client, tx_id)
    
    # display confirmed transaction group
    # tx1
    confirmed_txn = algod_client.pending_transaction_info(txn1.get_txid())
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

    # tx2
    confirmed_txn = algod_client.pending_transaction_info(txn2.get_txid())
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    return

def transferDocument(algod_client, loc_id, bol_id, seller_pk, buyer_mnemonic, carrier_mnemonic):
    buyer_sk = mnemonic.to_private_key(buyer_mnemonic)
    buyer_pk = mnemonic.to_public_key(buyer_mnemonic)
    carrier_sk = mnemonic.to_private_key(carrier_mnemonic)
    carrier_sk = mnemonic.to_pubic_key(carrier_mnemonic)
    txn1 = singleTransfer(buyer_pk, seller_pk, loc_id) #some params
    txn2 = singleTransfer(carrier_sk, buyer_pk, bol_id) #some params
    atomicTransfer(algod_client, txn1, txn2, buyer_sk, carrier_sk) #some params
    return None

########## SWITCHES ##########

def txn_switch(pk, txn_type):
    txn = None
    
    if txn_type == 'create':
        doc_id = y['doc-id']
        doc_name = y['doc-name']
        hashed_doc = y['hashed-doc']
        txn = createDocument(pk, hashed_doc, doc_id, doc_name)
    elif txn_type == 'revoke':
        doc_id = y['doc-id']
        txn = revokeDocument(pk, doc_id)
    elif txn_type == 'verify':
        hashed_doc = y['hashed-doc']
        doc_name = y['doc-name']
        txn = verifyDocument(doc_name, pk, hashed_doc)
    elif txn_type == 'opt-in':
        asset_id = y['asset-id']
        txn = optinDocument(algod_client, pk, asset_id)
    elif txn_type == 'transfer':
        asset_id = y['asset-id']
        destination_pk = y['other_public_key']
        txn = singleTransfer(pk, destination_pk, asset_id)
    #elif txn_type == 'transfer':
        #txn = transferDocument(algod_client, info[2], info[3], info[4], info[5], info[6])
    return txn


########## READ USER INPUT ##########

import sys
# by jacky, as my php code something wrong, this can give the correct inp 
html_file=""
html_file+=sys.argv[1]
inp = html_file[1:] #get txn type from user input

y = json.loads(inp)

txn_type = y['method']
#opt-in checking , need classified var
doc_id = ""
doc_name = ""
hashed_doc = ""
asset_id = ""
destination_pk = ""
#inp = sys.argv[1] #get txn type from user input
try:
    passphrase = y['passphrase']
    m = passphrase
    pk = mnemonic.to_public_key(m)
    sk = mnemonic.to_private_key(m)
    #print (sk)
except:
    pk = y['pk']
########## MAKE A TRANSACTION ##########

txn = txn_switch(pk, txn_type) #from userinput

# program come here, bring the txn here
if txn != None:
    stxn = txn.sign(sk) # Sign with secret key of transaction creator
    txid = algod_client.send_transaction(stxn) # Send the transaction to the network and retrieve the txid
    print(txid)
    #add fund then pass this error 
    #print(txid) #print transaction id
    
    txn_info = wait_for_confirmation(algod_client,txid) # Wait for the transaction to be confirmed
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        if txn_type == 'create': print_created_asset(algod_client, pk, asset_id) 
        print_asset_holding(algod_client, pk, asset_id)
        
    except Exception as e:
         print(e)

