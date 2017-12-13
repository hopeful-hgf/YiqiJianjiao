#! /bin/python3

import os
import datetime as dt
import sys

GPSepochdt=dt.datetime(1980,1,6,0,0,0,0,dt.timezone.utc)
year_now=dt.datetime(2017,1,1,0,0,0,0,dt.timezone.utc)

def main():
    if len(sys.argv)>1:
        y,m,d = sys.argv[1:4]
        week,dow,doy=gpsweek(dt.datetime(int(y),int(m),int(d)))
    else:
        week,dow,doy=gpsweek()
    print('GPSWEEK %d,   day of week %d,   doy %d \r\n',week,dow,doy)
    os.system('wget ftp://igs.gnsswhu.cn/pub/gps/products/'+str(week)+'/igs' + str(week)+str(dow)+'.sp3.Z')
    os.system('wget ftp://igs.gnsswhu.cn/pub/gps/data/daily/2017/' + str(doy)+'/17n/brdc'+str(doy)+'0.17n.Z')
    #os.system('wget ftp://igs.gnsswhu.cn/pub/gps/data/daily/2017/340/' + str(week)+str(dow)+'sp3.Z')
    os.system('wget ftp://igs.gnsswhu.cn/pub/gps/data/daily/2017/' + str(doy)+'/17o/shao'+str(doy)+'0.17o.Z')
    
    os.system("uncompress *.Z")
    os.system("mkdir brdc igs rinex")
    os.system("mv *o rinex")
    os.system("mv *n brdc")
    os.system("mv *.sp3 igs")

def gpsweek(Date=dt.datetime.utcnow()):
	Date=Date.replace(tzinfo=dt.timezone.utc)
	week= int ((Date - GPSepochdt)/dt.timedelta(weeks=1))
	dow=int((Date-GPSepochdt)/dt.timedelta(days=1)-7*week)
	doy=int((Date-year_now)/dt.timedelta(days=1))+1
	return week,dow,doy


if __name__=='__main__':
	main()
	
