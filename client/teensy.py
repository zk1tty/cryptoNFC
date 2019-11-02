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
# GET /Ledger/
resp1 = requests.get('https://lens.perlin.net/ledger/')
if resp.status_code != 200
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for todo_item in resp.json():
    print('GET /Ledger/')
    print('{} {}'.format(todo_item['id'], todo_item['summary']))

# POST /tx/send/
## make payload

post_json = {
                "sender": "[hex-encoded sender ID, must be 32 bytes long]",
                "tag": "[possible values: 0 = nop, 1 = transfer, 2 = contract, 3 = stake, 4 = batch",
                "payload": "[hex-encoded payload, empty for nop]",
                "signature": "[hex-encoded edwards25519 signature, which consists of private key, nonce, tag, and payload]"
            }
resp = requests.post('https://lens.perlin.net/tx/send/', json=post_json)
if resp.status_code !=201:
    raise ApiError('POST /tx/send/ {}'.format(resp.status_code)
print('Send transaction: {}'.format(resp.json()["tx_id"]))
