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
    def __init__(self, version, inputCount, outputCount, locktime, hash, hash_block):
        self.hash = hash
        self.hash_block = hash_block
        self.locktime = locktime
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.version = version

    def insertINTOvalues(self):
        return "('" + self.hash + "', '" + self.hash_block + "', " + self.locktime + ", " + self.inputCount + ", " + self.outputCount + ", " + self.version + ")"

class InputTransaction:
    def __init__(self, previousHash, outID, scriptLength, scriptSignature, seqNo, address, inputIndex):
        self.address = address
        self.hash_transaction = ''
        self.previousHash = previousHash
        self.outID = outID
        self.scriptLength = scriptLength
        self.scriptSignature = scriptSignature
        self.seqNo = seqNo
        self.inputIndex = inputIndex

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

    def setHashTransaction(self, hash):
        self.hash_transaction = hash

    def insertINTOvalues(self):
        return "('" + self.address + "','" + self.hash_transaction + "'," + self.outputIndex + "," + self.value + "," + self.scriptLength + ",'" + self.scriptSignature + "')"