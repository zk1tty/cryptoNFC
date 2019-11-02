from time import sleep
import serial, random
import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

# ser = serial.Serial('/dev/tty.usbmodem123451', 9600)
## convert
## check
# print ser.readline()
# sleep(.1)

# convert ser to 32byte
random.seed(0)
ser_byte = random.getrandbits(256)  
private_key = Ed25519PrivateKey.from_private_bytes(bytearray.fromhex('{:064x}'.format(ser_byte)))
print("private_key: ", private_key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()))
signature = private_key.sign(b"my authenticated test message")
print("signature: ", signature)
public_key = private_key.public_key()
print("puclic_key: ", public_key)
# Raises InvalidSignature if verification fails
public_key.verify(signature, b"my authenticated test message")

# verify 
loaded_public_key = public_key
loaded_public_key.verify(signature, b"my authenticated test message")
print("success!")


# call python API
class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)

# GET /Ledger/
resp1 = requests.get('https://testnet.perlin.net/ledger/')
if resp1.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /ledger/ {}'.format(resp1.status_code))

print('-------- GET /Ledger/ --------')
print(resp1.json())

# POST /tx/send/
## make payload

post_json = { "sender": "[hex-encoded sender ID, must be 32 bytes long]", "tag": "1",
              "payload": "[hex-encoded payload, empty for nop]",
              "signature":signature}
resp2 = requests.post('https://testnet.perlin.net/tx/send/', json=post_json)
if resp2.status_code !=201:
    raise ApiError('POST /tx/send/ {}'.format(resp2.status_code))
print('Send transaction: {}'.format(resp2.json()["tx_id"]))
