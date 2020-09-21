
import requests
import json

def getTokenBalance(contractAddress):
    response = requests.get("https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress" + contractAddress  + "&apikey=E6U7UEIQGFBCFC3PG8AUPXA2A6NWGVBDI1")
    tot =  response.json()["result"]  
  
    return tot
