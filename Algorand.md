# Features
__Algorand Standard Assets (ASA)__, __Atomic Transfers__ and __Algorand Smart Contract__ are the most important (and unique) concepts in Algorand Blockchain.

## Algorand Standard Assets (ASA)

## Atomic Transfers
### Definition
On Algorand, atomic transfers are implemented as irreducible batch operations, where a group of transactions are submitted as a unit and all transactions in the batch either pass or fail. This also eliminates the need for more complex solutions like hashed timelock contracts that are implemented on other blockchains. An atomic transfer on Algorand is confirmed in less than 5 seconds, just like any other transaction. Transactions can contain Algos or Algorand Standard Assets and may also be governed by Algorand Smart Contracts.
### Use case examples
- __Circular trades__ - Alice pays Bob if and only if Bob pays Claire if and only if Claire pays Alice.
- __Group payments__ - Everyone pays or no one pays.
- __Decentralized exchanges__ - Trade one asset for another without going through a centralized exchange.
- __Distributed payments__ - Payments to multiple recipients.
### Useful Links
https://developer.algorand.org/docs/features/atomic_transfers/

## Algorand Smart Contract
### Overview
Operation: on layer-1
Categories: stateful, stateless
Language: [Transaction Execution Approval Language (TEAL)](https://developer.algorand.org/docs/features/asc1/#transaction-execution-approval-language-teal)
- an assembly-like language that is interpreted by each Algorand node
- TEAL programs can be written by hand or by using the Python language with the PyTEAL compiler
### [Stateless smart contracts](https://developer.algorand.org/docs/features/asc1/#stateless-smart-contracts)
Primary Use: replace signature authority for transactions
- contract accounts
- signature delegation
### [Stateful smart contracts](https://developer.algorand.org/docs/features/asc1/#stateful-smart-contracts)
Definition: contracts that live on the chain and are used to keep track of some form of global and/or local state for the contract

Example: a voting application may be implemented as a stateful smart contract, where the list of candidates and their current vote tallies would be considered global state values. When an account casts a vote, their local account may be marked by the stateful smart contract with a boolean indicating that the account has already voted. The smart contract can be combined with a voting token implemented as an Algorand ASA to create a permissioned voting application. When used in this fashion, a voter would spend a voting token at the same time they submit their vote to the stateful smart contract. These two transactions would be grouped using Algorand’s Atomic Transfers to guarantee both happen at the same time. A centralized source would be responsible for giving out the voting tokens.
