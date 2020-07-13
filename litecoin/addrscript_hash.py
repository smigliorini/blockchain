#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base58


def sha256(hexstr):
    """sha256 hash algorithm
    """
    return hashlib.new('sha256', bytes.fromhex(hexstr)).hexdigest()


def rip160(hexstr):
    """ripemd160 hash algorithm
    """
    return hashlib.new('ripemd160', bytes.fromhex(hexstr)).hexdigest()


def printall(pubkey):
    p=pubkey
    #print('\n')
    #p=p.upper()
    #print('\n'+p+'\n')
    #p=sha256(p)
    #print('\n'+p+'\n')
    #p=p.upper()
    #print('\n'+p+'\n')
    #p=rip160(p)
    #print('\nPubkey hash: '+p+'\n')
    p=p.upper()
    #print('\n'+p+'\n')
    p="30"+p
    #print('\n'+p+'\n')
    p2=p.upper()
    #print('\n'+p2+'\n')
    p2=sha256(p2)
    #print('\n'+p2+'\n')
    p2=p2.upper()
    #print('\n'+p2+'\n')
    p2=sha256(p2)
    #print('\n'+p2+'\n')
    p2=p2.upper()
    #print('\n'+p2+'\n')
    p3=p+p2[0:8]
    #print('\n'+p3+'\n')
    p3=bytes.fromhex(p3)
    #print('\n'+str(p3)+'\n')
    p3=base58.b58encode(p3)
    #print('\n'+str(p3)+'\n')
    return p3
    

def get_ltc_address(pubkey):
    """https://bitcoin.stackexchange.com/questions/65282/how-is-a-litecoin-address-generated
    """
    
    #rip160_hash = "30" + rip160(sha256(pubkey.upper()).upper()).upper()
    #rip160_hash=pubkey
    #sha256_hash = sha256(sha256(rip160_hash).upper()).upper()
    #sha256_hash=rip160_hash
    #return base58.b58encode(bytes.fromhex(rip160_hash + sha256_hash[0:8]))
    if pubkey=='0000000000000000000000000000000000000000':
        return "b'coinbase'"
    return str(printall(pubkey))[2:-1]

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("[*] Usage: python %s publickey")
        sys.exit(1)

    print(str(get_ltc_address(sys.argv[1]))[2:-1])

# references
# https://en.bitcoin.it/wiki/Protocol_documentation#Addresses
# https://gist.githubusercontent.com/circulosmeos/97f2c155777434081cb56886c1b608be/raw/f960b4e89e86dcdf77fb6288c1005a7cb847cc98/easy-litecoin-address-from-public-key.py
# https://bitcoin.stackexchange.com/questions/65282/how-is-a-litecoin-address-generated
# https://bitcoin.stackexchange.com/questions/56923/is-this-how-to-generate-a-bitcoin-address-with-python
# https://iancoleman.io/bip39/
