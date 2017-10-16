import os
import datetime as dt

GPSepochdt=dt.datetime(1980,1,6,0,0,0,0,dt.timezone.utc)

def main():
	try:
		os.remove('err.txt')
	except FileNotFoundError:
		print(22)
	finally:
		os.system("echo * > err.txt")

	week=str(gpsweek())
	dirlist=os.listdir("../")
	datafile=[it for it in dirlist if it!="teqc"]

	for it in datafile:
		os.system('echo -e \"'+r'\r\n\r\n' + it + r'\r\n" >> err.txt') 
		obs='L1+L2+C1+C2+P2'
#		print(obs)
		name=it.split('.')[0]
#		os.system('teqc -week ' + week +' +nav ../' + name +'.17n -O.obs ' + obs +' ../' + it + ' > ../' + name +".17o" + " 2>> err.txt")
		os.system('teqc -week 1970 +nav ../' + name +'.17n -O.obs ' + obs +' ../' + it + ' > ../' + name +".17o" + " 2>> err.txt")
#		os.system('teqc +nav ../' + name +'.17n  ../' + it + ' > ../' + name +".17o" + " 2> err.txt")
		getinfo(name)

#os.system("teqc > txt.txt 2> err.txt")

def getobs(filename):
	obstype='L1+L2+C1+P2'
	conf = os.popen('teqc +config ' + filename)
	conf_list=conf.readlines()
	for it in conf_list:
		if it.find('-O.obs')>=0:
			obstype=it.split()[1]
#			print(obstype)
			return obstype

	return obstype

def getinfo(name):
	os.system('teqc +meta ../' + name + '.17o > ../' + name + '.txt' )

def gpsweek(Date=dt.datetime.utcnow()):
	Date=Date.replace(tzinfo=dt.timezone.utc)
	return str( int ((Date - GPSepochdt)/dt.timedelta(weeks=1)))


if __name__=='__main__':
	main()