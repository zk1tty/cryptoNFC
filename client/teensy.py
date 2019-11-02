from time import sleep
import serial, random
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
