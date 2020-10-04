from datetime import date
from decimal import *
import sys
import psycopg2
from myAppConfig import myHost , myDatabase , myUser , myPasswd , myPort
connessione = psycopg2 . connect ( host = myHost , database = myDatabase , user = myUser , password = myPasswd , port=myPort )
with connessione as con:
    con.autocommit=True
    with con.cursor() as cur:
        filename=sys.argv[1]
        price=Decimal(0)
        firstline=True
        ep=1410912000
        for line in open(filename):
            if firstline:
                firstline=False
                continue
            line=line.split(",")
            s=line[0].split("-")
            d=date(int(s[0]), int(s[1]), int(s[2]))
            price=round((Decimal(line[2])+Decimal(line[3]))/2, 3)
            ep2=ep+60*60*24
            cur.execute("insert into price values (%s, %s, %s, '%s', '%s')", (d, price, d.strftime("%A"), ep, ep2))
            ep=ep2
        
