# Stages
1. Create a wallet
1. Deploy document store
1. Configure DNS
1. Create raw document
1. Wrap document
1. Issue document
  - documentStore
  - merkleRoot
1. Read document

# Prototypes
## V1 - Verifiable Document: Proof of Authenticity and Provenance
Definition:
- aka a non-transferable document
- not used to transfer title
- the ownership to goods
- a document for which its authenticity and source can be verified

Examples:
- Sales invoices
- Certificates
- Permits

## V2 - Transferable Records: Title Transfer
Definition:
- deals with titles
- confers the __right to possession__ of the asset
- __presenting__ the document entitles the title holder to __claim possession__ of the asset

Examples:
- Cash Cheques
- Negotiable Bills of Lading

# GitHub Repo
## [Document CLI tool](https://github.com/TradeTrust/tradetrust-cli)
- CLI tool to create tradetrust documents
- This CLI tool turns .json documents into .tt verifiable documents. It applies the OpenAttestation algorithm to produce a hash of the json document and then creates a .tt file with the data and proof of integrity.
### Functions
#### [Batching Documents](https://github.com/TradeTrust/tradetrust-cli#batching-documents)
This command process all documents in the input directory and issue all of them in a single batch. It will then add the signature to the individual documents.
#### [Verifying All Signed Document in a Directory](https://github.com/TradeTrust/tradetrust-cli#verifying-all-signed-document-in-a-directory)
This command verifies that the document (and all it's evidence) is valid and is part of the document batch. However, it does not verify that the batch's merkle root is stored on the blockchain. User will need to verify that the document has indeed been issued by checking with the issuer's smart contract.
#### [Verifying Single Signed Document](https://github.com/TradeTrust/tradetrust-cli#verifying-single-signed-document)
This command verifies that the document (and all it's evidence) is valid and is part of the document batch. However, it does not verify that the batch's merkle root is stored on the blockchain. User will need to verify that the document has indeed been issued by checking with the issuer's smart contract.
#### [Document privacy filter](https://github.com/TradeTrust/tradetrust-cli#document-privacy-filter)
This allows document holders to generate valid documents which hides certain evidences. Useful for hiding grades lol.
