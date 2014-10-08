#!/usr/bin/python

import os

def dosmth(filename):
	f = open(filename, "rb")
	text = f.read()
	tmp = text.replace(b'\r\n',b'\n')
	f.close()
	f = open(filename, "wb")
	f.write(tmp)
	f.close()

def find(dir):
	names = os.listdir(dir)
	for name in names:
		fullname = os.path.join(dir, name)
		if os.path.isfile(fullname):
			dosmth(fullname)
		elif (name!=".") & (name !=".."):
			find(fullname)
			
			
if __name__ == "__main__":
	find(os.getcwd() + '\\')