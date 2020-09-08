import psycopg2
import time
import calendar
import sys
from myAppConfig import myHost , myDatabase , myUser , myPasswd , myPort
connessione = psycopg2 . connect ( host = myHost , database = myDatabase , user = myUser , password = myPasswd , port=myPort)

def isleap(i):
    if i%400==0:
        return True
    if i%4==0 and not(anno%100==0):
        return True
    return False

with connessione as con:
    con.autocommit=True
    with con.cursor() as cur:
#if __name__ == '__main__':
        ai=int(sys.argv[1])
        af=int(sys.argv[2])
        cur.execute("select max(year_yr) from year")
        res=cur.fetchone()[0]
        res=int(res)
        if ai!=res+1:
            exit()
        for i in range(ai, af+1):
            pattern = '%Y-%m-%d %H:%M:%S'
            d=str(i)+'-01-01'
            ep = int(calendar.timegm(time.strptime(d +' 00:00:00', pattern)))
            #for i in range(2010, 2020):
            if isleap(i):
                ep2=ep+31622400
            else:
                ep2=ep+31536000
            cur.execute("insert into year values ('%s', '%s', '%s')", (i,ep,ep2))
            #print(str(i)+' '+str(ep)+' '+str(ep2))
            ep=ep2
