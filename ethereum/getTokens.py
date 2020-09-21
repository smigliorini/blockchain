import requests
import json

def getTokenBalance(contractAddress):
    response =requests.get("https://api.etherscan.io/api?module=account&action=tokentx&address="+contractAddress+"&sort=asc&apikey=E6U7UEIQGFBCFC3PG8AUPXA2A6NWGVBDI1")
    tot = 0
    #vado a calcolare quanti token sono stati trasferiti da un account
    #tot rappresenta il bilancio di token trasferiti, aggiungo token quando l'address preso in considerazione è il ricevente mentre li tolgo quando l'address è il mittente
    for transactionNumber in range(len(response.json()["result"])) :
        tokenTransaction = response.json()["result"][transactionNumber]
        if tokenTransaction["from"] ==  contractAddress :
            #print(int(tokenTransaction["value"]))
            tot = tot - int(tokenTransaction["value"])
        elif tokenTransaction["to"] ==  contractAddress :
            #print(int(tokenTransaction["value"]))
            tot = tot + int(tokenTransaction["value"])

    return tot
