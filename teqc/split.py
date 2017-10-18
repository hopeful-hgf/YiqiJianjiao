import os
from datetime import datetime,timedelta

def main():

	dirlist=os.listdir("../")
	ofile=[it for it in dirlist if not (it=="teqc" or it[0]=='.') or it[-1]=='/']

######### CHANGE THE START TIME NEXT LINE ###############
#	sttime= 

	sttime=datetime(2017,10,12,10,00,00)
	for it in ofile:
		print(it)
		os.mkdir('../'+it[0])
		print(it[0])
		print(int (it[0])%2)
		if int(it[0])%2 ==0:
			even_station(it,sttime)
		else:
			odd_station(it,sttime)

	exitchar=input('Any char to quit:')


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


def odd_station(fname,stt):
	num=fname[0]
	endt=stt+timedelta(minutes=40)
	os.system(pre_scr(stt,endt) +num+'N1 ' + ' ../'+fname + ' > ../'+fname[0]+'/1.17o')
	print(pre_scr(stt,endt)+num+'N1 ' + ' ../'+fname + ' > ../'+fname[0]+'/1.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt)  +num+'E1 '+ ' ../'+ fname + ' > ../'+fname[0]+'/2.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt)  +num+'S1 '+ ' ../'+ fname + ' > ../'+fname[0]+'/3.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt) +num+'W1 ' + ' ../'+ fname + ' > ../'+fname[0]+'/4.17o')

	stt=endt
	endt=stt+timedelta(minutes=40)
	os.system(pre_scr(stt,endt)  +num+'N2 '+ ' ../'+ fname + ' > ../'+fname[0]+'/5.17o')

	stt=endt
	endt=stt+timedelta(minutes=60)
	os.system(pre_scr(stt,endt) +num+'N3 ' + ' ../'+ fname + ' > ../'+fname[0]+'/6.17o')


def even_station(fname,stt):
	num=fname[0]
	endt=stt+timedelta(minutes=40)
	os.system(pre_scr(stt,endt) +num+'N1 ' + ' ../'+fname + ' > ../'+fname[0]+'/1.17o')
	print(pre_scr(stt,endt)+num+'N1 ' + ' ../'+fname + ' > ../'+fname[0]+'/1.17o')

	stt=endt
	endt=stt+timedelta(minutes=60)
	os.system(pre_scr(stt,endt)  +num+'N2 '+ ' ../'+ fname + ' > ../'+fname[0]+'/2.17o')

	stt=endt
	endt=stt+timedelta(minutes=40)
	os.system(pre_scr(stt,endt)  +num+'N3 '+ ' ../'+ fname + ' > ../'+fname[0]+'/3.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt) +num+'E1 ' + ' ../'+ fname + ' > ../'+fname[0]+'/4.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt)  +num+'S1 '+ ' ../'+ fname + ' > ../'+fname[0]+'/5.17o')

	stt=endt
	endt=stt+timedelta(minutes=20)
	os.system(pre_scr(stt,endt) +num+'W1 ' + ' ../'+ fname + ' > ../'+fname[0]+'/6.17o')


def pre_scr(stt,endt):
	strs=stt.strftime('%Y,%m,%d,%H,%M,%S')
	stre=endt.strftime('%Y,%m,%d,%H,%M,%S')
	return 'teqc -st ' + strs + ' -e ' +stre+ ' -O.mo 0'

if __name__=='__main__':
	main()