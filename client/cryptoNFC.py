import serial
import random
import os
import requests
import transaction
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)


class CryptoNFC:
    def __init__(self):
        pass

    def ReadUID(self):
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

    def MakePayload(self, accountID, recipientID, amount):
        numPERLSSent = 0
        gasLimit = 0.75
        gasDeposit = 0
        functionName = "ic_transaction"
        functionPayload = transaction.ICTransactionPayload(
            amount, self.private_key.sign(amount))  # TODO

        # Transaction
        tag = 0x01
        payload = transaction.Payload(
            recipientID, numPERLSSent, gasLimit, gasDeposit, functionName,
            functionPayload)
        return transaction.Transaction(accountID, tag, payload)

    def PerformTransaction(self):
        my_private_key = Ed25519PrivateKey.from_private_bytes(
            bytearray.fromhex(os.getenv("MY_PRIVATE_KEY")))
        req = self.MakePayload(
            os.getenv("ACCOUNT_ID"),
            os.getenv("RECIPIENT_ID"),
            b"\x03").Sign(my_private_key).Build()
        print('Req: ', req)

        resp2 = requests.post('https://testnet.perlin.net/tx/send/', req)
        print('Send transaction: {}'.format(resp2.content))
        if resp2.status_code != 200:
            raise ApiError('POST /tx/send/ {}'.format(resp2.status_code))


if __name__ == "__main__":
    CryptoNFC().ReadUID().GeneratePrivateKey().PerformTransaction()
