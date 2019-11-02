import numpy
import json


class Transaction:
    def __init__(self, accountID, tag, payload):
        self.flag = True
        self.accountID = accountID
        self.tag = tag
        self.payload = payload

    def Sign(self, private_key):
        signstr = str()
        for ch in self.accountID:
            signstr += hex(ord(ch)).replace('0x', '')
        signstr += "%02x" % self.tag
        signstr += self.payload.Build()
        self.signature = private_key.sign(signstr)
        return self

    def Build(self):
        txn = dict()
        txn["sender"] = self.accountID
        txn["sender"] = accountIDstr
        txn["tag"] = self.tag
        txn["payload"] = self.payload.Build()
        signaturestr = str()
        for ch in self.signature:
            signaturestr += hex(ord(ch)).replace('0x', '')
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
        ret += "%016x" % self.numPERLSSent.newbyteorder()
        ret += "%016x" % self.gasLimit.newbyteorder()
        ret += "%016x" % self.gasDeposit.newbyteorder()

        # prefix the length
        ret += "%08x" % numpy.int32(len(self.functionName)).newbyteorder()
        for ch in self.functionName:
            ret += hex(ord(ch)).replace('0x', '')
        ret += "%08x" % numpy.int32(len(self.functionPayload)).newbyteorder()
        for ch in self.functionPayload:
            ret += hex(ord(ch)).replace('0x', '')
        return ret
