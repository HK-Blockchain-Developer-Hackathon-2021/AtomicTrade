# Transferable Record: Title Transfer

## Introduction

### Definition:
- deals with titles
- confers the __right to possession__ of the asset
- __presenting__ the document entitles the title holder to __claim possession__ of the asset

### Examples
- Cash Cheques
- Negotiable Bills of Lading

## Implementation

For Verifiable Documents , we will implement Token Registry Smart Contract in TradeTrust by stateful smart contract in Algorand. It aims to digitalise title transfer for trade documents. The subroutines include:
1. Create Document - `createDocument()`
2. Transfer Document - `transferDocument()`
3. Revoke Document - `revokeDocument()`

Other than these subroutines, we may implement the following helper functions:
- `wrapDocument()`
- `issueDocument()`: issue asset

### Create Document
- Function Name: `createDocument()`
- [Algorand - Creating an Asset](https://developer.algorand.org/docs/features/asa/#creating-an-asset)
- Description:

### Transfer Document
- Function Name: `transferDocument()`
- [Algorand - Transferring an Asset](https://developer.algorand.org/docs/features/asa/#transferring-an-asset)
- [Algorand - Rekeying](https://developer.algorand.org/docs/features/accounts/rekey/)
- Possible Algorand Feature: Atomic Transfer
- Description:

### Revoke Document
- Function Name: `revokeDocument()`
- [TradeTrust - Revoking Documents](https://www.openattestation.com/docs/verifiable-document/revoking-document)
- [Algorand - Destroying an Asset](https://developer.algorand.org/docs/features/asa/#destroying-an-asset)

## Appendix
The Prototype V2 are enhanced with the ability to perform title transfer on trade documents electronically. This ability will be pivotal in transforming paper-based processes to digital ones for cross-border trade. The transfer capability shall be compliant to the UNCITRAL Model Law on Electronic Transferable Records (MLETR), which stipulates the conditions electronic trade documents must fulfill in order to be the functional equivalent of paper-based ones. There will therefore be only a single “transferable” document at any one time, and its ownership from creation to expiry is controlled by only a single party at any one time. The V2 release can now therefore handle the title transfer of negotiable title documents like the eBL.
