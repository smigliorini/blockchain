class Block:
    def __init__(self, magicNumber, blockSize, version, previousHash, merkleRoot, time, bits, nonce, countOfTransactions, hash):
        self.hash = hash
        self.magicNumber = magicNumber
        self.blockSize = blockSize
        self.version = version
        self.previousHash = previousHash
        self.merkleRoot = merkleRoot
        self.time = time
        self.bits = bits
        self.nonce = nonce
        self.countOfTransactions = countOfTransactions

    def insertINTOvalues(self):
        return "('" + self.hash + "','" + self.magicNumber + "'," + self.blockSize + "," + self.version + ",'" + self.previousHash + "','" + self.merkleRoot + "','" + self.time + "'," + self.bits + "," + self.nonce + "," + self.countOfTransactions + ")"

class Transaction:
    def __init__(self, version, inputCount, outputCount, locktime, hash, hash_block, outputs, inputs):
        self.hash = hash
        self.hash_block = hash_block
        self.locktime = locktime
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.version = version
        self.outputs = outputs
        self.inputs = inputs

    def inputsToString(self):
        text = ""
        for input in self.inputs:
            text += "\n\n" + input.toString()
        return text

    def outputsToString(self):
        text = ""
        for output in self.outputs:
            text += "\n\n" + output.toString()
        return text

    def toString(self):
        return "hash: " + self.hash + "\n\ninputs:" + self.inputsToString() + "\n\noutputs:" + self.outputsToString() + "\n"

    def getHash(self):
        return self.hash

    def getOutputs(self):
        return self.outputs

    def insertINTOvalues(self):
        return "('" + self.hash + "', '" + self.hash_block + "', " + self.locktime + ", " + self.inputCount + ", " + self.outputCount + ", " + self.version + ")"

class InputTransaction:
    def __init__(self, previousHash, outID, scriptLength, scriptSignature, seqNo, inputIndex, address):
        self.hash_transaction = ''
        self.previousHash = previousHash
        self.outID = outID
        self.scriptLength = scriptLength
        self.scriptSignature = scriptSignature
        self.seqNo = seqNo
        self.inputIndex = inputIndex
        self.address = address
    
    def toString(self):
        return "previous hash: " + self.previousHash + "\nout id: " + str(self.outID)

    def getHashTransaction(self):
        return self.hash_transaction

    def getPreviousHash(self):
        return self.previousHash
    
    def getOutId(self):
        return self.outID

    def setHashTransaction(self, hash):
        self.hash_transaction = hash

    def insertINTOvalues(self):
        return "('" + self.address + "','" + self.hash_transaction + "'," + self.inputIndex + ",'" + self.previousHash + "'," + str(self.outID) + "," + self.scriptLength + ",'" + self.scriptSignature + "','" + self.seqNo + "')"
    

class OutputTransaction:
    def __init__(self, value, scriptLength, scriptSignature, address, outputIndex):
        self.address = address
        self.hash_transaction = ''
        self.value = value
        self.scriptLength = scriptLength
        self.scriptSignature = scriptSignature
        self.outputIndex = outputIndex

    def toString(self):
        return "address: " + self.address + "\nvalue: " + self.value + "\nout id: " + self.outputIndex

    def setHashTransaction(self, hash):
        self.hash_transaction = hash

    def getIndex(self):
        return self.outputIndex

    def getAddress(self):
        return self.address

    def insertINTOvalues(self):
        return "('" + self.address + "','" + self.hash_transaction + "'," + self.outputIndex + "," + self.value + "," + self.scriptLength + ",'" + self.scriptSignature + "')"