#
# 用于处理信标机数据
import os

def main():

	dirlist=os.listdir("../")
	ofile=[it for it in dirlist if not (it=="script" or it[0]=='.') or it[-1]=='/']

	for it in ofile:
		print(it)
		getdata(it)
	exitchar=input('Any char to quit:')



def getdata(fname):
	fname='../'+fname
	count=0
	maxN=4287
	outf=fname+'.csv'
	

	with open(fname) as inf, open(outf,'w') as dataf :
		dataf.write('N,E\n')
		for i in range(9000):
			line=inf.readline()
		while count< maxN:
			line=inf.readline()
			its=line.split(',')
			if its[0]=='$GPGGA':
				if its[6]=='2':
					dataf.write(its[2]+','+its[4]+'\n')
					count=count+1
	#	dataf.write('=AVERAGE(A2,A4288),=AVERAGE(B2,B4288)\n')
	#	dataf.write('=(A4233-3117)*60,=(B4233-12129)*60\n')
	#	dataf.write("2.59537,58.58163")
	#	dataf.write('=(A4234-A4235)*30,=(B4234-B4235)*30\n')



if __name__=='__main__':
	main()