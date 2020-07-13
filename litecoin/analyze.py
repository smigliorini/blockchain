import binascii
import struct
import datetime
import hashlib
import base58_2
import sys
import array
import traceback
import json
import addrscript
from addrscript import get_ltc_address
def log(string):
  print (string)
  pass

def startsWithOpNCode(pub):
  try:
    intValue = int(pub[0:2], 16)
    if intValue >= 1 and intValue <= 75:
      return True
  except:
    pass
  return False

def publicKeyDecode(pub):
  #pub=pub[2:]
  #print(pub)
  return get_ltc_address(str(pub)[2:-1])

def stringLittleEndianToBigEndian(string):
  string = binascii.hexlify(string)
  n = len(string) / 2
  fmt = '%dh' % n
  return struct.pack(fmt, *reversed(struct.unpack(fmt, string)))

def readShortLittleEndian(blockFile):
  return struct.pack(">H", struct.unpack("<H", blockFile.read(2))[0])

def readLongLittleEndian(blockFile):
  return struct.pack(">Q", struct.unpack("<Q", blockFile.read(8))[0])

def readIntLittleEndian(blockFile):
  b=bytearray(blockFile.read(4))
  #print(b)
  if len(b)==4:
    return struct.pack(">I", struct.unpack("<I", b)[0])
  else:
    exit()
    #return bytearray(b'\x00\x00\x00\x00')

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

def readInput(blockFile):
  previousHash = binascii.hexlify(blockFile.read(32)[::-1])
  outId = binascii.hexlify(readIntLittleEndian(blockFile))
  scriptLength = readVarInt(blockFile)
  scriptSignatureRaw = hexToStr(blockFile.read(scriptLength))
  scriptSignature = scriptSignatureRaw
  seqNo = binascii.hexlify(readIntLittleEndian(blockFile))
  address = ''
  try:
   address = publicKeyDecode(scriptSignatureRaw)
  except Exception as e:
    print (e)
    address = ''
  log("\n" + "Input")
  log("-" * 20)
  log("> Previous Hash: " + str(previousHash)[2:-1])
  log("> Out ID: " + str(outId)[2:-1])
  log("> Script length: " + str(scriptLength))
  log("> Script Signature (PubKey) Raw: " + str(scriptSignatureRaw)[2:-1])
  log("> Script Signature (PubKey): " + str(scriptSignature)[2:-1])
  log("> Address: " + str(address)[2:-1])
  log("> Seq No: " + str(seqNo)[2:-1])

def readOutput(blockFile):
  value = hexToInt(readLongLittleEndian(blockFile)) / 100000000.0
  scriptLength = readVarInt(blockFile)
  scriptSignatureRaw = hexToStr(blockFile.read(scriptLength))
  scriptSignature = scriptSignatureRaw
  address = ''
  try:
    address = publicKeyDecode(scriptSignatureRaw)
  except Exception as e:
    print (e)
    address = ''
  log("\n" + "Output")
  log("-" * 20)
  log("> Value: " + str(value))
  log("> Script length: " + str(scriptLength))
  log("> Script Signature (PubKey) Raw: " + str(scriptSignatureRaw)[2:-1])
  log("> Script Signature (PubKey): " + str(scriptSignature)[2:-1])
  log("> Address: " + str(address)[2:-1])

def readTransaction(blockFile):
  extendedFormat = False
  beginByte = blockFile.tell()
  inputIds = []
  outputIds = []
  version = hexToInt(readIntLittleEndian(blockFile)) 
  cutStart1 = blockFile.tell()
  cutEnd1 = 0
  inputCount = readVarInt(blockFile)
  log("\n\n" + "Transaction")
  log("-" * 100)
  log("Version: " + str(version))

  if inputCount == 0:
    extendedFormat = True
    flags = ord(blockFile.read(1))
    cutEnd1 = blockFile.tell()
    if flags != 0:
      inputCount = readVarInt(blockFile)
      log("\nInput Count: " + str(inputCount))
      for inputIndex in range(0, inputCount):
        inputIds.append(readInput(blockFile))
      outputCount = readVarInt(blockFile)
      for outputIndex in range(0, outputCount):
        outputIds.append(readOutput(blockFile))
  else:
    cutStart1 = 0
    cutEnd1 = 0
    log("\nInput Count: " + str(inputCount))
    for inputIndex in range(0, inputCount):
      inputIds.append(readInput(blockFile))
    outputCount = readVarInt(blockFile)
    log("\nOutput Count: " + str(outputCount))
    for outputIndex in range(0, outputCount):
      outputIds.append(readOutput(blockFile))

  cutStart2 = 0
  cutEnd2 = 0
  if extendedFormat:
    if flags & 1:
      cutStart2 = blockFile.tell()
      for inputIndex in range(0, inputCount):
        countOfStackItems = readVarInt(blockFile)
        for stackItemIndex in range(0, countOfStackItems):
          stackLength = readVarInt(blockFile)
          stackItem = blockFile.read(stackLength)[::-1]
          log("Witness item: " + hexToStr(stackItem))
      cutEnd2 = blockFile.tell()

  lockTime = hexToInt(readIntLittleEndian(blockFile))
  if lockTime < 500000000:
    log("\nLock Time is Block Height: " + str(lockTime))
  else:
    log("\nLock Time is Timestamp: " + datetime.datetime.fromtimestamp(lockTime).strftime('%d.%m.%Y %H:%M'))

  endByte = blockFile.tell()
  blockFile.seek(beginByte)
  lengthToRead = endByte - beginByte
  dataToHashForTransactionId = blockFile.read(lengthToRead)
  if extendedFormat and cutStart1 != 0 and cutEnd1 != 0 and cutStart2 != 0 and cutEnd2 != 0:
    dataToHashForTransactionId = dataToHashForTransactionId[:(cutStart1 - beginByte)] + dataToHashForTransactionId[(cutEnd1 - beginByte):(cutStart2 - beginByte)] + dataToHashForTransactionId[(cutEnd2 - beginByte):]
  elif extendedFormat:
    print (cutStart1, cutEnd1, cutStart2, cutEnd2)
    quit()
  firstHash = hashlib.sha256(dataToHashForTransactionId)
  secondHash = hashlib.sha256(firstHash.digest())
  hashLittleEndian = secondHash.hexdigest()
  hashTransaction = stringLittleEndianToBigEndian(binascii.unhexlify(hashLittleEndian))
  log("\nHash Transaction: " + str(hashTransaction)[2:-1]+"\n\n")
  if extendedFormat:
    print (hashTransaction)

def readBlock(blockFile):
  magicNumber = binascii.hexlify(blockFile.read(4))
  blockSize = hexToInt(readIntLittleEndian(blockFile))
  version = hexToInt(readIntLittleEndian(blockFile))
  previousHash = binascii.hexlify(blockFile.read(32))
  merkleHash = binascii.hexlify(blockFile.read(32))
  creationTimeTimestamp = hexToInt(readIntLittleEndian(blockFile))
  creationTime = datetime.datetime.fromtimestamp(creationTimeTimestamp).strftime('%d.%m.%Y %H:%M')
  bits = hexToInt(readIntLittleEndian(blockFile))
  nonce = hexToInt(readIntLittleEndian(blockFile))
  countOfTransactions = readVarInt(blockFile)
  log("Magic Number: " + str(magicNumber)[2:-1])
  log("Blocksize: " + str(blockSize))
  log("Version: " + str(version))
  log("Previous Hash: " + str(previousHash)[2:-1])
  log("Merkle Hash: " + str(merkleHash)[2:-1])
  log("Time: " + str(creationTime))
  log("Bits: " + str(bits))
  log("Nonce: " + str(nonce))
  log("Count of Transactions: " + str(countOfTransactions))
      
  for transactionIndex in range(0, countOfTransactions):
    readTransaction(blockFile)

def main():
  blockFilename = sys.argv[1]
  with open(blockFilename, "rb") as blockFile:
    try:
      while True:
        sys.stdout.write('\n.\n')
        sys.stdout.flush()
        readBlock(blockFile)
    except Exception as e:
      excType, excValue, excTraceback = sys.exc_info()
      traceback.print_exception(excType, excValue, excTraceback, limit = 8, file = sys.stdout)

if __name__ == "__main__":
  main()
