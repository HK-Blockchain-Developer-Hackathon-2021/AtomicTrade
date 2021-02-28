# Verifiable Document: Proof of Authenticity and Provenance

## Introduction

### Definition
- aka a non-transferable document
- not used to transfer title
- the ownership to goods
- a document for which its authenticity and source can be verified

### Examples
- Sales invoices
- Certificates
- Permits

## Implementation

For Verifiable Documents , we will implement Document Store Smart Contract in TradeTrust by stateless smart contract in Algorand. It aims to provide the proof of provenance and non-temper for trade documents. The subroutines include:
1. Create Document - `createDocument()`
2. Verify Document - `verifyDocument()`
3. Revoke Document - `revokeDocument()`

Other than these subroutines, we may implement the following helper functions:
- `wrapDocument()`: <input> string; <output> hash
- `compareHash`: compare hash
- `issueDocument()`: issue asset

### Create Document
- Function Name: `createDocument()`
- [Algorand - Creating an Asset](https://developer.algorand.org/docs/features/asa/#creating-an-asset)
- Description:
  - take as input a html file as string of arbitrary length
  - hash the string (wrap the document) by `wrapDocument()`
  - configure the asset
  - issue document by `issueDocument()`

### Verify Document
- Function Name: `verifyDocument()`
- Features
  - verify the provenance of a document
  - verify that the document has not been tampered
- Possible Algorand Feature: Logic Signature
- Description:
  - take as input a document id and a html file as string of arbitrary length
  - hash the string (wrap the document) by `wrapDocument()`
  - compare hash of the documents by `compareHash`

### Revoke Document
- Function Name: `revokeDocument()`
- [TradeTrust - Revoking Documents](https://www.openattestation.com/docs/verifiable-document/revoking-document)
- [Algorand - Destroying an Asset](https://developer.algorand.org/docs/features/asa/#destroying-an-asset)

## Appendix
The Prototype V1 is able to provide proof of authenticityandprovenanceoftradedocumentation by leveraging on the use of distributed ledger technology (DLT). Current forms of digital documentation are neither tamper-proof nor able to prove the source of origin resulting in trade transactions still falling back to paper documentation at some point in the supply chain. V1’s capability addresses these gaps by providing tamper-proof features, enabling documentation tracing to the source of origin. Through the use of V1 features, participants of TradeTrust are able to verify the authenticity and provenance of a digital document.
