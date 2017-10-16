import os
import datetime as dt

def main():
	dirlist=os.listdir("../")
	datafile=[it for it in dirlist if it!="teqc"]

	for it in datafile:
		if it[-1]=='o' or it[-1]=='O':
			getinfo(it)
#		os.system('teqc +nav ../' + name +'.17n  ../' + it + ' > ../' + name +".17o" + " 2> err.txt")

def getinfo(name):
	os.system('teqc +meta ../' + name + ' > ../' + name + '.txt' )



if __name__=='__main__':
	main()