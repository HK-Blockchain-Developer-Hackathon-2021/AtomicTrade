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
    wait_for_confirmation(algodclient, tx_id)
    
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
    txn1 = singleTransfer(buyer_pk, seller, loc_id) #some params
    txn2 = singleTransfer(carrier_sk, buyer_pk, bol_id) #some params
    atomicTransfer(algod_client, txn1, txn2, buyer_sk, carrier_sk) #some params
    return none
