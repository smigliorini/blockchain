import binascii
import struct
import datetime
import hashlib
import base58
import array
import Bitcoin
import bitcoin
import psycopg2
import createDatabase as data

blocks = []
transactions = []
inputs = []
outputs = []
addresses = []

def readShortLittleEndian(blockFile):
    return struct.pack(">H", struct.unpack("<H", blockFile.read(2))[0])

def readIntLittleEndian(blockFile):
    return struct.pack(">I", struct.unpack("<I", blockFile.read(4))[0])

def readLongLittleEndian(blockFile):
    return struct.pack(">Q", struct.unpack("<Q", blockFile.read(8))[0])

def hexToInt(value):
    return int(binascii.hexlify(value), 16)

def hexToStr(value):
    return binascii.hexlify(value)

def readVarInt(blockFile):
    varInt = ord(blockFile.read(1))
    returnInt = 0
    if varInt < 0xfd:
        return varInt
    if varInt == 0xfd:
        returnInt = readShortLittleEndian(blockFile)
    if varInt == 0xfe:
        returnInt = readIntLittleEndian(blockFile)
    if varInt == 0xff:
        returnInt = readLongLittleEndian(blockFile)
    return int(binascii.hexlify(returnInt), 16)

def deleteDuplicate(listOFduplicate, ad):
    for address in listOFduplicate:
        if address == ad:
            return True
    return False

def readInput(blockFile, inputIndex):
    previousHash = binascii.hexlify(blockFile.read(32)[::-1])
    outId = binascii.hexlify(readIntLittleEndian(blockFile))
    scriptLength = readVarInt(blockFile)
    scriptSignature = hexToStr(blockFile.read(scriptLength))
    seqNo = binascii.hexlify(readIntLittleEndian(blockFile))
    address = publicKeyDecode(scriptSignature)

    if deleteDuplicate(addresses, address):
        pass
    else:
        addresses.append((str(address)))

    return (Bitcoin.InputTransaction(str(previousHash), int(outId, 16), str(scriptLength), str(scriptSignature), str(seqNo), str(address), str(inputIndex)))

def startsWithOpNCode(pub):
    try:
        intValue = int(pub[0:2], 16)
        if intValue >= 1 and intValue <= 75:
            return True
    except:
        pass
    return False

def publicKeyDecode(pub):
    if pub.lower().startswith('76a914'):
        pub = pub[6:-4]
        result = (b'\x00') + binascii.unhexlify(pub)
        h5 = hashlib.sha256(result)
        h6 = hashlib.sha256(h5.digest())
        result += h6.digest()[:4]
        return base58.b58encode(result)
    elif pub.lower().startswith('a9'):
        return ""
    elif startsWithOpNCode(pub):
        pub = pub[2:-2]
        h3 = hashlib.sha256(binascii.unhexlify(pub))
        h4 = hashlib.new('ripemd160', h3.digest())
        result = (b'\x00') + h4.digest()
        h5 = hashlib.sha256(result)
        h6 = hashlib.sha256(h5.digest())
        result += h6.digest()[:4]
        return base58.b58encode(result)
    return ""

def readOutput(blockFile, outputIndex):
    value = hexToInt(readLongLittleEndian(blockFile)) / 100000000.0
    scriptLength = readVarInt(blockFile)
    scriptSignature = hexToStr(blockFile.read(scriptLength))
    address = ''

    try:
        address = publicKeyDecode(scriptSignature)
        if deleteDuplicate(addresses, address):
            pass
        else:
            addresses.append((str(address)))
    except:
        print('publicKeyDecode error')
        address = ''

    return (Bitcoin.OutputTransaction(str(value), str(scriptLength), str(scriptSignature), str(address), str(outputIndex)))


def stringLittleEndianToBigEndian(string):
    string = binascii.hexlify(string)
    n = len(string) / 2
    fmt = '%dh' % n
    return struct.pack(fmt, *reversed(struct.unpack(fmt, string)))  

def readTransaction(blockFile, hash_block):
    extendedFormat = False
    beginByte = blockFile.tell()
    inputIds = []
    outputIds = []
    version = hexToInt(readIntLittleEndian(blockFile))
    cutStart1 = blockFile.tell()
    cutEnd1 = 0
    inputCount = readVarInt(blockFile)
    if inputCount == 0:
        extendedFormat = True
        flags = ord(blockFile.read(1))
        cutEnd1 = blockFile.tell()
        if flags != 0:
            inputCount = readVarInt(blockFile)
            for inputIndex in range(0, inputCount):
                inputIds.append(readInput(blockFile, inputIndex))
            outputCount = readVarInt(blockFile)
            for outputIndex in range(0, outputCount):
                outputIds.append(readOutput(blockFile, outputIndex))
    else:
        cutStart1 = 0
        cutEnd1 = 0
        for inputIndex in range(0, inputCount):
            inputIds.append(readInput(blockFile, inputIndex))
        outputCount = readVarInt(blockFile)
        for outputIndex in range(0, outputCount):
            outputIds.append(readOutput(blockFile, outputIndex))

    cutStart2 = 0
    cutEnd2 = 0
    if extendedFormat:
        if flags & 1:
            cutStart2 = blockFile.tell()
            for inputIndex in range(0, inputCount):
                countOfStackItems = readVarInt(blockFile)
                for stackItemIndex in range(0, countOfStackItems):
                    stackLength = readVarInt(blockFile)
                    stackItem = blockFile.read(stackItem)
            cutEnd2 = blockFile.tell()
    
    lockTime = hexToInt(readIntLittleEndian(blockFile))
    endByte = blockFile.tell()
    blockFile.seek(beginByte)
    lengthToRead = endByte - beginByte
    dataToHashForTransactionId = blockFile.read(lengthToRead)
    if extendedFormat and cutEnd1 != 0 and cutEnd1 != 0 and cutStart2 != 0 and cutEnd2 != 0:
        dataToHashForTransactionId = dataToHashForTransactionId[:(cutStart1 - beginByte)] + dataToHashForTransactionId[(cutEnd1 - beginByte):(cutStart2 - beginByte)] + dataToHashForTransactionId[(cutEnd2 - beginByte):]
    elif extendedFormat:
        print(cutStart1, cutEnd1, cutStart2, cutEnd2)
        quit()
    firstHash = hashlib.sha256(dataToHashForTransactionId)
    secondHash = hashlib.sha256(firstHash.digest())
    hashLittleEndian = secondHash.hexdigest()
    hashTransaction = stringLittleEndianToBigEndian(binascii.unhexlify(hashLittleEndian))
    if extendedFormat:
        print(hashTransaction)

    for input in inputIds:
        input.setHashTransaction(hashTransaction)
        inputs.append(input)

    for output in outputIds:
        output.setHashTransaction(hashTransaction)
        outputs.append(output)

    transactions.append(Bitcoin.Transaction(str(version), str(inputCount), str(outputCount), str(lockTime), str(hashTransaction), str(hash_block)))

def readBlock(block):
    magicNumber = binascii.hexlify(block.read(4))
    blockSize = hexToInt(readIntLittleEndian(block))

    # le variabili con _ davanti le utilizzo per calcolare l'hash del blocco
    _version = block.read(4)
    version = hexToInt(struct.pack(">I", struct.unpack("<I", _version)[0]))
    previousHash = binascii.hexlify(block.read(32))
    merkleHash = binascii.hexlify(block.read(32))

    _time = block.read(4)
    creationTimeTimestamp = hexToInt(struct.pack(">I", struct.unpack("<I", _time)[0]))
    creationTime = datetime.datetime.fromtimestamp(creationTimeTimestamp).strftime('%Y-%m-%d %H:%M')

    _bits = block.read(4)
    bits = hexToInt(struct.pack(">I", struct.unpack("<I", _bits)[0]))

    _nonce = block.read(4)
    nonce = hexToInt(struct.pack(">I", struct.unpack("<I", _nonce)[0]))
    countOfTransaction = readVarInt(block)

    header_hex = binascii.hexlify(_version) + previousHash + merkleHash + binascii.hexlify(_time) + binascii.hexlify(_bits) + binascii.hexlify(_nonce)
    header_bin = header_hex.decode('hex')
    hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()

    print("Magic Number: " + str(magicNumber))
    print("Blocksize: " + str(blockSize))
    print("Version: " + str(version))
    print("Previous Hash: " + str(previousHash))
    print("Merkle Hash: " + str(merkleHash))
    print("Time: " + str(creationTime))
    print("Bits: " + str(bits))
    print("Nonce: " + str(nonce))
    print("Hash: " + str(hash.encode('hex_codec')))
    print("Count of Transactions: " + str(countOfTransaction))

    for transaction in range(0, countOfTransaction):
        readTransaction(block, str(hash.encode('hex_codec')))

    blocks.append(Bitcoin.Block(str(magicNumber), str(blockSize), str(version), str(previousHash), str(merkleHash), str(creationTime), str(bits), str(nonce), str(countOfTransaction), str(hash.encode('hex_codec'))))

def formatINTO(listINTO, query, i):
    if i == len(listINTO) - 1:
        query = query + ";"
    else:
        query = query + ","
    return query

def query_insertINTO(query, objects):
    i = 0
    for obj in objects:
        query = query + obj.insertINTOvalues()
        query = formatINTO(objects, query, i)
        i += 1
    return query

def Address_insertINTO():
    i = 0
    address_query = data.insertAddressINTO()
    for add in addresses:
        address_query = address_query + " " + "('" + add + "')"
        address_query = formatINTO(addresses, address_query, i)
        i += 1
    return address_query

def deleteTable():
    return data.dropOutputTable() + data.dropInputTable() + data.dropAddressTable() + data.dropTransactionTable() + data.dropBlockTable()

def createTable():
    return data.createBlockTable() + data.createTransactionTable() + data.createAddressTable() + data.createInputTable() + data.createOutputTable()

def main():
    blockFilename = '../../bitcoin/blocks/blk00000.dat'

    with open(blockFilename, 'rb') as blockFile:
        for block in range(0, 50):
            readBlock(blockFile)

    try:
        connection = psycopg2.connect(host = "localhost", user = "postgres", password = "Gialloblu98", port = "5433", dbname = "bitcoin", connect_timeout = 3)
        cursor = connection.cursor()

        """cursor.execute(deleteTable())
        connection.commit()"""

        cursor.execute(createTable())
        connection.commit()

        cursor.execute(query_insertINTO(data.insertBlockINTO(), blocks))
        connection.commit()

        cursor.execute(query_insertINTO(data.insertTransactionINTO(), transactions))
        connection.commit()

        cursor.execute(Address_insertINTO())
        connection.commit()

        cursor.execute(query_insertINTO(data.insertInputINTO(), inputs))
        connection.commit()

        cursor.execute(query_insertINTO(data.insertOutputINTO(), outputs))
        connection.commit()

        cursor.close()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        connection.close()
        print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()
