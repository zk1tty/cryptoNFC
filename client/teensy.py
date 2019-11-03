from time import sleep
import serial
import random
import transaction
import requests
import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

ser = serial.Serial(os.getenv("SERIAL_DEVICE"), 9600)
UID = ser.readline()
# check
print("-----------------------")
print(UID)
print("-----------------------")

# convert ser to 32byte
random.seed(UID)
ser_byte = random.getrandbits(256)
private_key = Ed25519PrivateKey.from_private_bytes(
    bytearray.fromhex('{:064x}'.format(ser_byte)))
print("private_key: ", private_key.private_bytes(serialization.Encoding.Raw,
                                                 serialization.PrivateFormat.Raw, serialization.NoEncryption()))
signature = private_key.sign(b"my authenticated test message")  # TODO
print("signature: ", signature)
public_key = private_key.public_key()
print("puclic_key: ", public_key)
# Raises InvalidSignature if verification fails
public_key.verify(signature, b"my authenticated test message")

# REST API exception class


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)


def GetLedger():
    ##############
    # GET /Ledger/
    ##############
    resp1 = requests.get('https://testnet.perlin.net/ledger/')
    if resp1.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /ledger/ {}'.format(resp1.status_code))

    print('-------- GET /Ledger/ --------')
    print(resp1.json())


###############
# POST /tx/send/
################
# make payload

# Payload
def MakePayload(accountID, recipientID):
    numPERLSSent = 0
    gasLimit = 0.75
    gasDeposit = 0
    functionName = "ic_transaction"
    functionPayload = transaction.ICTransactionPayload(
        b"\x03", private_key.sign(b"\x03"))  # TODO

    # Transaction
    tag = 0x01
    payload = transaction.Payload(
        recipientID, numPERLSSent, gasLimit, gasDeposit, functionName, functionPayload)
    return transaction.Transaction(accountID, tag, payload)


my_private_key = Ed25519PrivateKey.from_private_bytes(
    bytearray.fromhex(os.getenv("MY_PRIVATE_KEY")))
resp2 = requests.post('https://testnet.perlin.net/tx/send/',
                      MakePayload(os.getenv("ACCOUNT_ID"), os.getenv("RECIPIENT_ID")).Sign(my_private_key).Build())
print('Send transaction: {}'.format(resp2.content))
if resp2.status_code != 200:
    raise ApiError('POST /tx/send/ {}'.format(resp2.status_code))
