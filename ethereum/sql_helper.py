from datetime import datetime as dt
from getPrice import *

#inizializza il file sql  con create table e gli index  
def create_sql():
    file1 = open("database.sql","w")
    file1.write(    """
    CREATE TABLE IF NOT EXISTS block ( 
     blockNumber BIGINT PRIMARY KEY,
     blockGasUsed NUMERIC, 
     blockHash TEXT, 
     blockLogsBloom TEXT, 
     blockNonce TEXT, 
     difficulty TEXT, 
     extraData TEXT, 
     gasLimit BIGINT, 
     miner TEXT, 
     mixHash TEXT,
     parentHash TEXT, 
     receiptsRoot TEXT, 
     sha3Uncles TEXT, 
     size BIGINT, 
     stateRoot TEXT, 
     timestamp BIGINT, 
     totalDifficulty TEXT, 
     transactionsRoot TEXT, 
     uncles TEXT,
     dollarquote DECIMAL(12,6),
     totalFee NUMERIC DEFAULT null
     );"""
    """
    \n
    CREATE TABLE IF NOT EXISTS Quick (
     txHash TEXT PRIMARY KEY,
     balanceFrom TEXT,
     balanceTo TEXT,
     blockNumber BIGINT REFERENCES block(blockNumber), 
     sender TEXT,
     nonce BIGINT, 
     recipient TEXT,
     value TEXT);"""
    """
    \n
    CREATE TABLE IF NOT EXISTS TX (
     txHash TEXT PRIMARY KEY,    
     blockNumber BIGINT REFERENCES block(blockNumber),
     contractAddress TEXT,
     cumulativeGasUsed NUMERIC, 
     gas NUMERIC, 
     gasPrice NUMERIC, 
     gasUsed NUMERIC,
     input TEXT, 
     logs TEXT, 
     logsBloom TEXT, 
     r TEXT, 
     s TEXT, 
     status BIGINT, 
     transactionIndex BIGINT, 
     v INTEGER ,
     fee NUMERIC);"""
                    

    "\n"
                
    """           
    CREATE TABLE IF NOT EXISTS account(
     address TEXT PRIMARY KEY,
     balance DECIMAL,
     txCount INTEGER);
    \n
    
    CREATE TABLE IF NOT EXISTS contract(
     address TEXT PRIMARY KEY);
    """
    "\n"            
                
    "CREATE INDEX index_quick ON Quick(value, sender, recipient);\n"
    "CREATE INDEX index_TX ON TX(blockNumber, status);\n"
    "CREATE INDEX index_block ON block(timestamp);\n"
    "CREATE INDEX index_account ON account(address);\n"
    "CREATE INDEX index_contract ON contract(address);\n\n"                
    
    )
    file1.close()

#scambia 2 caratteri in una stringa        
def swap(s, i, j):
    return ''.join((s[:i], s[j], s[i+1:j], s[i], s[j+1:]))

#scrive la stringa insert per una tupla di block s
def replace_wordb(dictionary):
    uncles=dictionary.get("uncles")
    dictionary.update(uncles=removechar(uncles))
    
    #modifiche sulla data
    intTimeStamp =  dictionary.get("timestamp") 
    timestamp = dt.fromtimestamp(intTimeStamp)

    
    
    s = """\nINSERT INTO block VALUES ( blockNumber , blockGasUsed ,\' blockHash \',\' blockLogsBloom \',\' blockNonce \',\' difficulty \',\' extraData \', gasLimit ,\' miner \',\' mixHash \',\' parentHash \',\' receiptsRoot \',\' sha3Uncles \', size ,\' stateRoot \', timestamp ,\' totalDifficulty \',\' transactionsRoot \',\' uncles \',"""
    s+=getPriceAtDate(timestamp.strftime('%Y-%m-%d'))+");\n"    
    s = ' '.join([str(dictionary.get(i, i)) for i in s.split()])
    
    i=0
    pair=0
    while i < len(s):
        char=s[i]
        if (char == "'" and pair == 0):
            s=swap(s, i, i+1)
            i+=1
            pair=1
        elif (char == "'" and pair == 1):
            s=swap(s, i-1, i)
            pair=0
        i+=1
    s=s+"\n"
    return s

#scrive la stringa insert per una tupla di transactions
def replace_wordt(dictionary):
    log=dictionary.get("logs")
    dictionary.update(logs=removechar(log))
    s = """\n INSERT INTO TX VALUES (\' txHash \', blockNumber ,\' contractAddress \', cumulativeGasUsed , gas , gasPrice , gasUsed ,\' input \',\' logs \',\' logsBloom \',\' r \',\' s \', status , transactionIndex , v ,"""
    s += str(dictionary.get("gasUsed") * dictionary.get("gasPrice")) + ");\n"
    s = ' '.join([str(dictionary.get(i, i)) for i in s.split()])
    i=0
    pair=0
    while i < len(s):
        char=s[i]
        if (char == "'" and pair == 0):
            s=swap(s, i, i+1)
            i+=1
            pair=1
        elif (char == "'" and pair == 1):
            s=swap(s, i-1, i)
            pair=0
        i+=1
    s=s+"\n"
    return s

# scrive la stringa insert per una tupla di quick 
def replace_wordq(dictionary):
    s ="""\n INSERT INTO Quick VALUES (\' txHash \',\' balanceFrom \',\' balanceTo \', blockNumber ,\' from \', nonce ,\' to \',\' value \'); \n"""
    s = ' '.join([str(dictionary.get(i, i)) for i in s.split()])
    i=0
    pair=0
    while i < len(s):
        char=s[i]
        if (char == "'" and pair == 0):
            s=swap(s, i, i+1)
            i+=1
            pair=1
        elif (char == "'" and pair == 1):
            s=swap(s, i-1, i)
            pair=0
        i+=1
    s=s+"\n"
    return s

#scrive la stringa insert per una tupla di accounts
def replace_worda(dictionary,web3,user):
    
    stringInsert = ""

    if  dictionary[user] == None :
        stringInsert = "\n"
    elif web3.toHex(web3.eth.getCode(dictionary[user])) == "0x":
        stringInsert = insertAccount(dictionary,web3,user)
    else :
        stringInsert = insertContract(dictionary,web3,user)
        #print(  web3.toHex(web3.eth.getCode(dictionary[user]))  )

        #print("\n\n")
        
        
    return stringInsert 
    
def replace_wordFeeBlock(totFee,block):
   return "UPDATE block \n SET totalFee ="+str(totFee)+"\n WHERE blockNumber = "+str(block)+";\n\n"

                
    
 
def insertAccount(dictionary,web3,user):
    accountAdd = dictionary[user]
    accountInsert = "INSERT INTO account VALUES(\'" + accountAdd +"\',"+ str(web3.eth.getBalance(accountAdd)) + ","+str(web3.eth.getTransactionCount(accountAdd))+") "+\
            "ON CONFLICT(address)  DO UPDATE SET (address,balance,txcount) = "+\
            "(\'"+accountAdd+"\',"+str(web3.eth.getBalance(accountAdd))+","+  str(web3.eth.getTransactionCount(accountAdd)) +");\n\n"
    return accountInsert
    
def insertContract(dictionary,web3,user):
    contractAdd = dictionary[user]
    contractInsert = "INSERT INTO contract VALUES(\'" + contractAdd +"\') "+\
        "ON CONFLICT(address)  DO UPDATE SET address = "+\
        "\'"+contractAdd+"\';\n\n"
    return contractInsert
    
    
def removechar(string):
    return string.replace("\'", "")
    
