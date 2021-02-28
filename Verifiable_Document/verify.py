import hashlib
import json
from BeautifulSoup import BeautifulSoup

from algosdk.v2client import indexer

def indexer():

    myindexer = indexer.IndexerClient(indexer_token="", indexer_address="http://localhost:8980")

    response = myindexer.search_transactions(min_amount=10, limit=5) 

    # Pretty Printing JSON string
    print(json.dumps(response, indent=2, sort_keys=True))

    # /indexer/python/search_transactions_paging.py

    nexttoken = ""
    numtx = 1

    # loop using next_page to paginate until there are no more transactions in the response
    # for the limit (max is 1000  per request)

    while (numtx > 0):

        response = myindexer.search_transactions(
            min_amount=100000000000000, limit=2, next_page=nexttoken) 
        transactions = response['transactions']
        numtx = len(transactions)
        if (numtx > 0):
            nexttoken = response['next-token']
            # Pretty Printing JSON string 
            print("Tranastion Info: " + json.dumps(response, indent=2, sort_keys=True))




def parseDoc(doc):
    return BeautifulSoup(doc)

def hashDoc(doc):
    return hashlib.sha256(bytes(doc, 'utf-8')).hexdigest()

def checkAssets(key, val, account_info):
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx += 1        
        if (scrutinized_asset[key] == val):
            return True
    return False

def isIssued(doc_id, account_info):
    # check issuer
    return checkAssets('unit name', doc_id, account_info)

def isNotTampered(hashed_doc, account_info):
    # compare hash
    return checkAssets('url', hashed_doc, account_info)

def isNotRevoked(doc):
    return True
    # check LogSic

#def isValidIssuer(doc):
    #return False

def isValid(doc_id, hashed_doc, client):
    account = input() #e
    account_info = client.account_info(account)
    if isIssued(doc_id, account_info) & isNotTampered(hashed_doc, account_info) & isNotRevoked(doc): #& isValidIssuer(doc):
        return True
    return False

def main():

    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    #raw_doc = input()
    html_doc = input()
    parsed_doc = parseDoc(html_doc)
    hashed_doc = hashDoc(parsed_doc)
    doc_id = "id" #need to take out id


    return isValid(doc_id, hashed_doc, algod_client)

main()