import requests
import json


def getContractCode(contractAddress):

    response = requests.get("https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + contractAddress + "&apikey=95T2MJ6VRXRF1Q9Y4U8CK1QQ4GGRW5G3AQ.json")
    return (  ((response.json()["result"])[0])["SourceCode"]  )

