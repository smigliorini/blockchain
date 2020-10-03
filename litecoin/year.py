import psycopg2
from myAppConfig import myHost , myDatabase , myUser , myPasswd , myPort
connessione = psycopg2 . connect ( host = myHost , database = myDatabase , user = myUser , password = myPasswd , port=myPort)

def isleap(i):
    if i==2012 or i==2016 or i==2020:
        return True
    return False

with connessione as con:
    con.autocommit=True
    with con.cursor() as cur:
        ep=1262304000
        for i in range(2010, 2020):
            if isleap(i):
                ep2=ep+31622400
            else:
                ep2=ep+31536000
            cur.execute("insert into year values ('%s', '%s', '%s')", (i,ep,ep2))
            ep=ep2
            
            
            

