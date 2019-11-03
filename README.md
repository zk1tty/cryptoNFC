# CryptoNFC

`cryptoNFC` provides crypto-backed NFC charge and payments. It uses the
decentralized [Wavelet](https://wavelet.perlin.net/) network to send
[PERL](https://cryptowat.ch/assets/perl) tokens from user to user.

## Usage

*As the owner of the IC card*, run `python3 client/get_key.py`, and use this
credential to log into the [Wavelet testnet](https://lens.perlin.net/).

In `contract/transfer-nfc/`, run:

```
cargo build --release --target wasm32-unknown-unknown
```

and upload the `transfer-nfc.wasm` file to the [smart contract
uploader](https://lens.perlin.net/#/contracts).

*As the party who wants to receive tokens*, run:

```
$ export CONTRACT_ID=[the ID of the smart contract]
$ export RECIPIENT_ID=[the ID of the recipient of the tokens]
$ python3 client/cryptoNFC.py [number of microPERLs to send]
```

## How does it work?

By sending tokens to a smart contract associated with an IC card, a user can
effectively charge their IC card, and remit those tokens to another party using
an IC card reader.

## What's going on under the hood?

We use the UID of a ISO/IEC 14443 A/MIFARE card to generate a unique identity
for a user in the Wavelet network, which they can use to log in and upload [a
smart contract](contract/transfer-nfc/src/lib.rs) which can authorize token to
be sent to a third party. By sending tokens to the smart contract via the
`charge_ic` function of the smart contract, the user can providing another party
with the contract ID and UID, the user can authorize that party to deduct some
tokens using the `ic_transaction` function of the same contract.

![Flowchart](https://raw.githubusercontent.com/suricata3838/cryptoNFC/master/cryptoNFC.png)
