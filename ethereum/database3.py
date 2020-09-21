""" 
Sript per spostare i dati della blockchain da un nodo Infura a PostgreSql
"""

#vengono importate le librerie time e os
from web3 import Web3
from organize import *
import time
from sql_helper import *
import os

import psycopg2


# 1. connection via Infura
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/6484d4add39247bb8a0da7e8ae5ce08a"))

# 2. or connection via local node 
#web3 = Web3(Web3.IPCProvider('/your-path-to/geth.ipc'))


#numero dei blocchi che volgio caricare
Nblocks =  10000
start_time = time.time()
#apro lastblock.txt per vedere da quale blocco partire , altrimenti parto dal blocco start
try:
    with open('lastblock.txt', 'r') as f:
        start = int(f.read())+1
except FileNotFoundError:
    start =  0 

#se il Database non esiste lo creo e lo inizializzo
file_name="database.sql"
file_new= not os.path.exists(file_name)

if file_new:
    print("creazione sql")
    create_sql()
else:
   file1 = open("database.sql","r+")
   file1.truncate(0)
   file1.close()
    
    
count = 0
#loop over all blocks
for block in range(start, start+Nblocks):
    
    #scrivo il blocco nel database
    block_table, block_data = order_table_block(block,web3)
    file1 = open("database.sql","a")
    file1.write(replace_wordb(block_table))
    file1.write(replace_worda(block_table,web3,"miner"))
    
    #calcolo il valore statico di ricompensa 
    totFee = 0
    if block < 4370000 : 
        totFee = 5
    elif block < 7280000 :
         totFee = 3
    else :
        totFee = 2
    #itero su ogni transazione del blocco
    for hashh in block_data['transactions']:    
        quick_table, tx_data = order_table_quick(hashh,block, web3)
        
        #list of tx data that will go to the DB
        TX_table = order_table_tx(tx_data,hashh, web3)
        #scrivo nel file ogni transazione sulla tabella quick e tx
        #e ogni account sulla tabella account
        file1.write(replace_wordt(TX_table))
        file1.write(replace_wordq(quick_table))
        
        #sommo le fee da scrivere nel blocco
        totFee = totFee + web3.fromWei((TX_table.get("gasUsed") * TX_table.get("gasPrice")),'ether')

        file1.write(replace_worda(quick_table,web3,"from"))
        file1.write(replace_worda(quick_table,web3,"to"))
        
    #aggiungo fee totali al blocco
    file1.write(replace_wordFeeBlock(totFee,block))    
    file1.close()
        
    count = count + 1
    print(count)
    #dump output every 2 blocks
    
        
    #update the current block number to a file
    if (count % 1000) == 0:
        connection = psycopg2.connect(user = "deboni", password = "eth2004", host = "localhost" , port = "5437 ", database = "ethdb")
        with connection:
            with connection.cursor() as cursore:
                cursore.execute(open("database.sql", "r").read())
        connection.close()
        with open('lastblock.txt', 'w') as f:
            f.write("%d" % block)
        file1 = open("database.sql","r+")
        file1.truncate(0)
        file1.close()
            
    #aggiungo al file timeperXblocks alcuni dati riguardanti il tempo di esecuzione         
    if (count % 10) == 0:
        end = time.time()
        with open('timeperXblocks.txt', 'a') as f:
            f.write("%d %f \n" % (block, end-start_time))

connection = psycopg2.connect(user = "deboni", password = "eth2004", host = "localhost" , port = "5437 ", database = "ethdb")
with connection:
    with connection.cursor() as cursore:
        cursore.execute(open("database.sql", "r").read())
connection.close()
with open('lastblock.txt', 'w') as f:
    f.write("%d" % block)

