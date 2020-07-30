from csv import DictReader

def getPriceAtDate(Date):
    dataEnd = "2020-06-15"
    fileToOpen = "ETH_USD_2015-08-09_" + dataEnd + "-CoinDesk.csv"
    with open( fileToOpen , "r" ) as read_obj :
        csv_reader = DictReader(read_obj)
        for row in csv_reader:
            if row['Date'] == Date  :
                return row['Closing Price (USD)']
        return "0"    
   
