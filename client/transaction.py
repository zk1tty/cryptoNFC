import numpy
import json


class Transaction:
    def __init__(self, accountID, tag, payload):
        self.flag = True
        self.accountID = accountID
        self.tag = tag
        self.payload = payload

    def Sign(self, private_key):
        # the message to be signed is the uint64(0) as little endian bytes + tag + payload appended together as bytes
        signstr = bytes.fromhex("0000000000000000") + bytes.fromhex("%02x" %
                                                                    self.tag) + bytes.fromhex(self.payload.Build())
        print("payload bytes:", bytes.fromhex(self.payload.Build()))
        print("message bytes:", signstr)
        self.signature = private_key.sign(signstr)
        return self

    def Build(self):
        txn = dict()
        txn["sender"] = self.accountID
        txn["tag"] = self.tag
        txn["payload"] = self.payload.Build()
        signaturestr = str()
        for ch in self.signature:
            signaturestr += "%02x" % ch
        print("signaturestr = ", signaturestr)
        txn["signature"] = signaturestr
        return json.dumps(txn)


class Payload:
    def __init__(self, recipientID, numPERLSSent, gasLimit, gasDeposit, functionName, functionPayload):
        self.recipientID = recipientID
        self.numPERLSSent = numpy.uint64(numPERLSSent)
        self.gasLimit = numpy.uint64(gasLimit)
        self.gasDeposit = numpy.uint64(gasDeposit)
        self.functionName = functionName
        self.functionPayload = functionPayload

    def Build(self):
        ret = str()
        ret += self.recipientID
        ret += "%016x" % self.numPERLSSent
        ret += "%016x" % self.gasLimit
        ret += "%016x" % self.gasDeposit

        # prefix the length
        ret += "%08x" % numpy.int32(len(self.functionName)).newbyteorder()
        for ch in self.functionName:
            ret += "%02x" % ord(ch)
        payload = self.functionPayload.Build()
        ret += "%08x" % numpy.int32(len(payload) / 2).newbyteorder()
        ret += payload
        return ret


class ICTransactionPayload:
    def __init__(self, data, signature):
        self.data = data
        self.signature = signature

    def Build(self):
        ret = str()
        ret += "%08x" % numpy.int32(len(self.data)).newbyteorder()
        for ch in self.data:
            ret += "%02x" % ch
        ret += "%08x" % numpy.int32(len(self.signature)).newbyteorder()
        for ch in self.signature:
            ret += "%02x" % ch
        return ret
