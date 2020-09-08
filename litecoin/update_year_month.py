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
#if __name__ == '__main__':
        ai=int(sys.argv[1])
        af=int(sys.argv[2])
        cur.execute("select max(year_month_yr) from year_month")
        res=cur.fetchone()[0]
        res=int(res)
        if ai!=res+1:
            exit()
        for i in range(ai, af+1):
            for j in range(1, 13):
                pattern = '%Y-%m-%d %H:%M:%S'
                d=str(i)+'-'+str(j)+'-01'
                ep = int(calendar.timegm(time.strptime(d +' 00:00:00', pattern)))
                ep2=ep+60*60*24*days(j,i)
                cur.execute("insert into year_month values ('%s', '%s', '%s', '%s')", (i,j,ep,ep2))
                #print(str(i)+'-'+str(j)+' '+str(ep)+' '+str(ep2))
                ep=ep2
