import binascii
import serial
import random
import os
import requests
import sys
import transaction
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)


class CryptoNFC:
    def __init__(self):
        self.amount = sys.argv[1]

    def ReadUID(self):
        print("Sending: {} tokens".format(self.amount))
        print("to account: {}".format(os.getenv("RECIPIENT_ID")))
        print("Please tap the NFC card.....")
        ser = serial.Serial(os.getenv("SERIAL_DEVICE"), 9600)
        self.uid = ser.readline()
        return self

    def GeneratePrivateKey(self):
        random.seed(self.uid)
        ser_byte = random.getrandbits(256)
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            bytearray.fromhex('{:064x}'.format(ser_byte)))
        return self

    def GetLedger(self):
        ##############
        # GET /Ledger/
        ##############
        resp1 = requests.get('https://testnet.perlin.net/ledger/')
        if resp1.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /ledger/ {}'.format(resp1.status_code))

        print('-------- GET /Ledger/ --------')
        print(resp1.json())

    def MakePayload(self, accountID, amount):
        numPERLSSent = 0
        gasLimit = 75000000
        gasDeposit = 0
        functionName = "ic_transaction"
        functionPayload = transaction.ICTransactionPayload(
            os.getenv("RECIPIENT_ID"), self.amount)

        # Transaction
        tag = 0x01
        payload = transaction.Payload(
            os.getenv(
                "CONTRACT_ID"), numPERLSSent, gasLimit, gasDeposit,
            functionName, functionPayload)
        return transaction.Transaction(accountID, tag, payload)

    def PerformTransaction(self):
        req = self.MakePayload(
            binascii.hexlify(
                self.private_key.public_key().public_bytes(
                    serialization.Encoding.Raw, serialization.PublicFormat.Raw))
            .decode("ascii"),
            3).Sign(self.private_key).Build()
        print('Performing transaction....')

        resp2 = requests.post('https://testnet.perlin.net/tx/send/', req)
        print(resp2.content)
        if resp2.status_code != 200:
            raise ApiError('POST /tx/send/ {}'.format(resp2.status_code))
        print('Complete!')


if __name__ == "__main__":
    CryptoNFC().ReadUID().GeneratePrivateKey().PerformTransaction()
