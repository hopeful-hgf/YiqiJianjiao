import os
import datetime as dt

GPSepochdt=dt.datetime(1980,1,6,0,0,0,0,dt.timezone.utc)

def main():
	print(gpsweek())

def gpsweek(Date=dt.datetime.utcnow()):
	Date=Date.replace(tzinfo=dt.timezone.utc)
	return int ((Date - GPSepochdt)/dt.timedelta(weeks=1))


if __name__=='__main__':
	main()