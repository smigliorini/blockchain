import psycopg2

from myAppConfig import myHost , myDatabase , myUser , myPasswd
from prevhash import readBlock, readTransaction
import sys
from addrscript_hash import get_ltc_address
connessione = psycopg2 . connect ( host = myHost , database = myDatabase , user = myUser , password = myPasswd )
#blockFilename=sys.argv[1]
def printnots(cur):
    print('Esito: {:s}'. format(cur.statusmessage))
    print ('Eventuali notifiche :')
    for i in range(len(connessione.notices)):
        l=len(connessione.notices[i])+5
        s='{:>'+str(l)+'s}'
        print(s. format(connessione.notices[i]))

def getPrevHash(blockFilename, cur):
  #blockFilename = sys.argv[1]
  #cur.execute("select txin_scriptsig from txin")
  i=0
  with open(blockFilename, "rb") as blockFile:
    try:
      while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        countOfTransactions=readBlock(blockFile)
        if countOfTransactions is None:
            break
        for transactionIndex in range(0, countOfTransactions):
            (ph, ssr, txhash, outId)=readTransaction(blockFile)
            if ph is None or ssr is None:
                break
            for tr in range(len(ph)):
                if ph[tr] is not None and ssr[tr] is not None and ph!='0000000000000000000000000000000000000000000000000000000000000000':
                    cur.execute("update txin set txin_prev_hash = %s from tx where txin.tx_id=tx.tx_id and txin_scriptsig = %s and txin_prev_hash is null and tx.tx_hash = %s", (ph[tr], ssr[tr], txhash))
                    print("Prev hash: "+ str(ph[tr])+"\nScript signature raw: "+str(ssr[tr]))
                    cur.execute("update txin set txin_outid = %s from tx where txin.tx_id=tx.tx_id and txin_scriptsig = %s and txin_outid is null and tx.tx_hash = %s", (outId[tr], ssr[tr], txhash))
                i=i+1
            print(i)
    except Exception as e:
      excType, excValue, excTraceback = sys.exc_info()
      traceback.print_exception(excType, excValue, excTraceback, limit = 8, file = sys.stdout)

def countn(n):
    c=0
    while n!=0:
        n=n//10
        c=c+1
    return c

def incindex(blockFilename):
    index=blockFilename[-9:-4]
    n=int(index)+1
    c=countn(n)
    index=index[:-c]+str(n)
    blockFilename=blockFilename[:-9]+index+blockFilename[-4:]
    #print(blockFilename)
    return blockFilename

with connessione as con:
    con.autocommit=True
    with con.cursor() as cur:
        #cur.execute("drop table if exists block_txin")
        #printnots(cur)
        #cur.execute("alter table block_next rename column block_id to block_hash")
        #cur.execute("alter table block_next rename column next_block_id to next_block_hash")
        #printnots(cur)
        #cur.execute("select * from tx tx join txout b on tx.tx_id=b.tx_id where tx.tx_hash='5673343e2682bc7556d978870eb83f6bccfc001ed33797417f52b81aab4f538c'")
        #cur.execute("alter table txin add column txin_prev_hash varchar(64)")
        #print(cur.fetchmany(10))
        #cur.execute("create index txinprevh on txin (txin_prev_hash)")
        #cur.execute("alter table txin add column txin_outid varchar(64)")
        #for i in range(11):
            #print (i)
            #try:
                #print("Nome file: "+blockFilename)
                #getPrevHash(blockFilename, cur)
                #blockFilename=incindex(blockFilename)
            #except Exception as e:
                #break
                #pass
        #print("exit")
        #cur.execute("drop table if exists addr")
        #printnots(cur)
        #cur.execute("create table addr (addr_address varchar(128), pubkey_hash character(40) references pubkey(pubkey_hash))")
        #printnots(cur)
        #cur.execute("insert into addr(pubkey_hash) select pubkey_hash from pubkey")
        #cur.execute("create index addrpubkeyhash on addr (pubkey_hash)")
        #cur.execute("update addr set addr_address = null")
        #cur.execute("select pubkey_hash from addr")
        #for record in cur:
            #print(record)
            #address=record[0]
            #address=get_ltc_address(address)
            #with con.cursor() as cur2:
                #cur2.execute("update addr set addr_address = %s where pubkey_hash like %s", (address, record[0]))
        #cur.execute("update txin set txin_outid = null")
        #cur.execute("update txin set txin_prev_hash = null")
        #cur.execute("alter table txin add column addr_address varchar(128)")
        #cur.execute("alter table txout add column addr_address varchar(128)")
        #cur.execute("update txout set addr_address = addr.addr_address from pubkey, addr where txout.pubkey_id=pubkey.pubkey_id and pubkey.pubkey_hash=addr.pubkey_hash")
        #cur.execute("update txin set addr_address = txout.addr_address from tx, txout where tx.tx_id=txout.tx_id and tx.tx_hash=txin.prev_hash and txout.txout_pos=txin.txout_id")
        cur.execute("update txout set addr_address=null")
    #connessione.commit()  
con.close()
