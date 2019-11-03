import random
import serial

ser = serial.Serial(os.getenv("SERIAL_DEVICE"), 9600)
UID = ser.readline()
print("-----------------------")
print UID
print("-----------------------")

random.seed(UID)
ser_byte = random.getrandbits(256)
private_key = Ed25519PrivateKey.from_private_bytes(
    bytearray.fromhex('{:064x}'.format(ser_byte)))
print("export MY_PRIVATE_KEY=", private_key.private_bytes(
    serialization.Encoding.Raw, serialization.PrivateFormat.Raw))
print("export ACCOUNT_ID=", private_key.public_key().public_bytes(
    serialization.Encoding.Raw, serialization.PublicFormat.Raw))
