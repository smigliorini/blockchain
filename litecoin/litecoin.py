import hashlib
import base58
import bech32
import binascii
import blockcypher
from decimal import *

def sha256(hexstr):
    """sha256 hash algorithm
    """
    return hashlib.new('sha256', bytes.fromhex(hexstr)).hexdigest()

def rip160(hexstr):
    """ripemd160 hash algorithm
    """
    return hashlib.new('ripemd160', bytes.fromhex(hexstr)).hexdigest()

def getAddress(pubkey, pr):
    p=pubkey
    p=p.upper()
    p=sha256(p)
    p=p.upper()
    p=rip160(p)
    print(addr_funct(p, pr))

def addr_funct(hashpubkey, pr):
    if pr is None:
        return
    dic={'L':'30', 'm':'6f', 'M':'32', '3':'05', '2':'c4', 'Q':'3a', '4':'08', 'l':True, 't':False}
    if pr in dic:
        pr=dic[pr]
    prs=['30', '6f', '32', '05', 'c4', '3a', '08', True, False]
    if pr not in prs:
        return None
    if isinstance(pr, int):
        try:
            spk = binascii.unhexlify(hashpubkey)
            if spk[0]:
                version = spk[0] - 0x30
            else:
                version = 0
            program = spk[2:]
            if pr:
                return bech32.encode('ltc', version, program)
            else:
                return bech32.encode('tltc', version, program)
        except:
            return
    p=hashpubkey
    p=p.upper()
    p=pr+p
    p2=p.upper()
    p2=sha256(p2)
    p2=p2.upper()
    p2=sha256(p2)
    p2=p2.upper()
    p3=p+p2[0:8]
    p3=bytes.fromhex(p3)
    p3=base58.b58encode(p3)
    return str(p3)[2:-1]

def find_hpub(cur, address, isMS=False):
    pref=address[0]
    dic={'L':'30', 'm':'6f', 'M':'32', '3':'05', '2':'c4', 'Q':'3a', '4':'08', 'l':True, 't':False}
    if not isinstance(dic[pref], int):
        if isMS:
            cur.execute("select pubkey_hash from pubkey join multisig_pubkey on pubkey.pubkey_id=multisig_pubkey.multisig_id")
        else:
            cur.execute("select pubkey_hash from pubkey")
        pubkey_hash=None
        for record in cur:
            if address==addr_funct(record[0], dic[pref]):
                pubkey_hash=record[0]
                break
        return (pubkey_hash, False)
    else:
        cur.execute("select scriptpubkey from script_pub_key")
        scriptpubkey=None
        for record in cur:
            if address==addr_funct(record[0], dic[pref]):
                scriptpubkey=record[0]
                break
        return (scriptpubkey, True)
    return None, None
           
def getLTCcount(cur, address):
    cur.execute("select count_LTC from balance where address like %s", (address,))
    res=cur.fetchone()
    if res is not None:
        count=round(((Decimal(res[0]))/100000000), 8)
        #print("Address: "+ address +"\nLTC balance: " + str(count))
        return count
    if res is None:
        (pubkey_hash, isSW)=find_hpub(cur, address)
        if pubkey_hash is None:
            #print("Indirizzo sbagliato!")
            return
        if isSW:
            cur.execute("select count_LTC from balance where scriptpubkey like %s", (pubkey_hash,))
        else:
            cur.execute("select count_LTC from balance where pubkey_hash like %s", (pubkey_hash,))
        res=cur.fetchone()
        if res is not None:
            count=round(((Decimal(res[0]))/100000000), 8)
        else:
            count=countLTC(cur, pubkey_hash, address, isSW, False)
        #print("Address: "+ address +"\nLTC balance: " + str(count))
        return count

def getLTCcount_pubkeyhash(cur, pubkey_hash, pr):
    if pr=='l' or pr=='t':
        cur.execute("select address, count_LTC from balance where scriptpubkey like %s", (pubkey_hash,))
    else:
        cur.execute("select address, count_LTC from balance where pubkey_hash like %s", (pubkey_hash,))
    res=cur.fetchone()
    if res is not None:
        address=res[0]
        count=round(((Decimal(res[1]))/100000000), 8)
        #print("Address: "+ address +"\nLTC balance: " + str(count))
        return address,count
    if res is None:
        if pr=='l' or pr=='t':
            isSW=True
            cur.execute("select scriptpubkey from script_pub_key where scriptpubkey like %s", (pubkey_hash,))
        else:
            isSW=False
            cur.execute("select pubkey_hash from pubkey where pubkey_hash like %s", (pubkey_hash,))
        res2=cur.fetchone()
        if res2 is None:
            #print("Indirizzo sbagliato!")
            return None, None
        dic={'L':'30', 'm':'6f', 'M':'32', '3':'05', '2':'c4', 'Q':'3a', '4':'08', 'l':True, 't':False}
        address=addr_funct(res2[0], dic[pr])
        count=countLTC(cur, pubkey_hash, address, isSW, False)
        #print("Address: "+ address +"\nLTC balance: " + str(count))
        return address,count

def remake_count(cur, address):
    cur.execute("select address from balance where address like %s", (address,))
    res=cur.fetchone()
    if res is None:
        return
    pr=address[0]
    address=res[0]
    if pr=='l' or pr=='t':
        isSW=True
        cur.execute("select scriptpubkey from balance where address like %s", (address,))
    else:
        isSW=False
        cur.execute("select pubkey_hash from balance where address like %s", (address,))
    res=cur.fetchone()
    pubkey_hash=res[0]
    count=countLTC(cur, pubkey_hash, address, isSW, True)
    return count

def countLTC (cur, pubkey_hash, address, isSW, update=False):
    if not isSW:
        cur.execute("select sum(txin_value) from txin_detail where pubkey_hash like %s",(pubkey_hash,))
    else:
        cur.execute("select sum(txin_value) from txin_detail where txin_scriptpubkey like %s",(pubkey_hash,))
    res=cur.fetchone()
    if res[0] is None:
        count=Decimal(0)
    else:
        count=Decimal(res[0])
    if not isSW:
        cur.execute("select sum(txout_value) from txout_detail where pubkey_hash like %s",(pubkey_hash,))
    else:
        cur.execute("select sum(txout_value) from txout_detail where txout_scriptpubkey like %s",(pubkey_hash,))
    res=cur.fetchone()
    if res[0] is None:
        count=Decimal(0)-count
    else:
        count=Decimal(res[0])-count
    if update:
        cur.execute("update balance set count_ltc = '%s' where address like %s", (count, address))
    else:
        cur.execute("insert into balance values (%s, '%s')", (address, count))
        if not isSW:
            cur.execute("update balance set pubkey_hash = %s where address like %s", (pubkey_hash, address))
        else:
            cur.execute("update balance set scriptpubkey = %s where address like %s", (pubkey_hash, address))
    count=round((count/100000000), 8)
    return count

def find_follblock(cur, block_id):
    cur.execute("select b2.block_id from block b1, block b2 where b1.block_ntime<b2.block_ntime and b2.block_ntime in (select min(b3.block_ntime) from block b3 where b3.block_ntime>b1.block_ntime) and b1.block_id= %s", (block_id,))
    res=cur.fetchone()
    if res is None:
        return
    return res[0]

def find_prevblock(cur, block_id):
    cur.execute("select b2.block_id from block b1, block b2 where b1.block_ntime>b2.block_ntime and b2.block_ntime in (select max(b3.block_ntime) from block b3 where b3.block_ntime<b1.block_ntime) and b1.block_id= %s", (block_id,))
    res=cur.fetchone()
    if res is None:
        return
    return res[0]

def convert_blockhash(cur, block_hash):
    cur.execute("select block_id from block where block_hash like %s",(block_hash,))
    res=cur.fetchone()
    if res is None:
        return
    bid=res[0]
    fid=find_follblock(cur, bid)
    cur.execute("select block_hashprev from orphan_block where block_id= %s",(fid,))
    res=cur.fetchone()
    return res[0]

def query(cur, statem):
    cur.execute(statem)
    for record in cur:
        print(record, end='\n')
