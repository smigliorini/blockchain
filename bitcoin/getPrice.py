import requests
import json
import psycopg2
import createDatabase as data
from json import JSONEncoder

coins = []
date = []
price = []
tmp = []

class Coin:
    def __init__(self, date, value):
        self.source = "coindesk"
        self.startDate = date[1:-1] + " 00:00"
        self.endDate = date[1:-1] + " 23:59"
        self.value = value
    def toString(self):
        return "Data: " +self.startDate+ " -  Valore: " +self.value
    def insertINTOvalues(self):
        return "('" + self.source + "','" + self.startDate + "','" + self.endDate + "'," + self.value + ")"

class CoinEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def formatINTO(listINTO, query, i):
    if i == len(listINTO) - 1:
        query = query + ";"
    else:
        query = query + ","
    return query

def Quotation_insertINTO():
    i = 0
    quotation_query = data.insertQuotationINTO()
    for coin in coins:
        quotation_query = quotation_query + " " + coin.insertINTOvalues()
        quotation_query = formatINTO(coins, quotation_query, i)
        i += 1
    return quotation_query

def main():
    r = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2010-07-17&end=2020-05-29')
    values = str(r.json()).split('u')

    print(values)

    i = 0
    for value in values:
        if i >= 2 and i <= len(values) - 14:
            date = value.split(":")
            price = date[1].split(",")
            coins.append(Coin(date[0], price[0][1:]))
        elif i == len(values) - 13:
            date = value.split(":")
            tmp = date[1].split(",")
            price = tmp[0].split("}")
            coins.append(Coin(date[0], price[0][1:]))
        i += 1

    with open("coindesk.json", "w") as outfile:
        transactionJSONData = json.dumps(coins, indent=4, cls=CoinEncoder)
        outfile.write(transactionJSONData)

    for coin in coins:
        print(coin.toString())

    try:
        connection = psycopg2.connect(host = "localhost", user = "postgres", password = "Gialloblu98", port = "5433", dbname = "bitcoin", connect_timeout = 3)
        cursor = connection.cursor()

        """cursor.execute(data.dropQuotationTable())
        connection.commit()"""

        cursor.execute(data.createQuotationTable())
        connection.commit()

        cursor.execute(Quotation_insertINTO())
        connection.commit()

        cursor.close()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        connection.close()
        print("PostgreSQL connection is closed")



if __name__ == "__main__":
    main()