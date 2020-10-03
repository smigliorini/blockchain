import psycopg2
from myAppConfig import myHost , myDatabase , myUser , myPasswd , myPort
connessione = psycopg2 . connect ( host = myHost , database = myDatabase , user = myUser , password = myPasswd , port=myPort)

def isleap(i):
    if i==2012 or i==2016 or i==2020:
        return True
    return False

def days(j, i):
    if j==1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
        return 31
    if j==4 or j==6 or j==9 or j==11:
        return 30
    if j==2:
        if isleap(i):
            return 29
        else:
            return 28

with connessione as con:
    con.autocommit=True
    with con.cursor() as cur:
        ep=1262304000
        for i in range(2010, 2021):
            for j in range(1, 13):
                ep2=ep+60*60*24*days(j,i)
                cur.execute("insert into year_month values ('%s', '%s', '%s', '%s')", (i,j,ep,ep2))
                ep=ep2
            
            
            

