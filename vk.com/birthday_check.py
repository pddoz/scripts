#!/usr/bin/python3

#																						#
#	Helps to know the birth date of person using information from vk.com even it's		#
#	hidden																				#
#																						#
#	USAGE:																				#
#		"birthday_check.py <user_id> <year> <month> <day>								#
#			<user_id> is necessary. Look for it: "http://vk.com/<user_id>"				#									
#			<year>, <month> & <day> can be skipped. This is additional information      #
#				about user we know. 0 means we don't know this info.					#
#	EXAMPLES:																			#
#		birthday_check.py durov 1984 0 10												#
#		birthday_check.py durov															#
#		birthday_check.py durov 1984													#
#																						#

import sys
import os.path
import http.client
import re
import urllib.parse
from datetime import date

MAX_REQUEST_ATTEMPTS = 5
days = [31,29,31,30,31,30,31,31,30,31,30,31]

def getName(user_id):
	count = 0
	while count < MAX_REQUEST_ATTEMPTS:
		
		try:
			conn = http.client.HTTPConnection("m.vk.com", 80, timeout=10)
			conn.request("GET","/{}".format(user_id))
			
			r1 = conn.getresponse()
			if r1.status == 200:
				ans = r1.read().decode("utf-8")
				m = re.search("(<title>)(.+)(<\/title>)".format(user_id), ans)
				if m != None:
					return m.group(2)
				return user_id
			else:
				count = count + 1
		except:
			count = count + 1
			
	
	print (MAX_REQUEST_ATTEMPTS, " attempts to connect the server are failed. Try later")
	sys.exit(0)

def check(user_id, name, year=0, month=0, day=0):
	count = 0
	while count < MAX_REQUEST_ATTEMPTS:
		#print(count)
		try:
			conn = http.client.HTTPConnection("vk.com", 80, timeout=10)
			request = {'c[section]':'people', 'c[q]':name, 'c[name]': 1}
			if year > 0:
				request['c[byear]'] = year
			if month > 0:
				request['c[bmonth]'] = month
			if day > 0:
				request['c[bday]'] = day
			conn.request("POST","/al_search.php", urllib.parse.urlencode(request))
			#print(urllib.parse.urlencode(request))
			
			r1 = conn.getresponse()
			if r1.status == 200:
				ans = r1.read().decode("cp1251")
				m = re.search("(vk\.com)*(\/)({})".format(user_id), ans)

				return m != None
			else:
				count = count + 1
		except:
			count = count + 1
	
	print (MAX_REQUEST_ATTEMPTS, " attempts to connect the server are failed. Try later")
	sys.exit(0)
	

def findDay(user_id, name, year, month):
	found = False
	day = 0
	while (found == False) & (day < days[month]):
		day = day + 1
		found = check(user_id, name, year, month, day)
		print ("{}/{}/{}".format(day, month, year), found)
	if found == False:
		return 0
	return day

def findMonth(user_id, name, year):
	found = False
	month = 0
	while (found == False) & (month < 12):
		month = month + 1
		found = check(user_id, name, year, month)
		print ("{}/{}".format(month, year), found)
	if found == False:
		return 0
	return month


def findYear(user_id, name, f, u):
	found = False
	year = f
	while (found == False) & (year <= u):
		found = check(user_id, name, year)
		print (year, found)
		year = year + 1
	if found == False:
		return 0
	return year - 1

if __name__ == '__main__':
	user_id = sys.argv[1]
	name = user_id
	if user_id.startswith("id"):
		name = getName(user_id)
		print (name)
		#sys.exit(0)
	size = len(sys.argv)
	year = 0
	month = 0
	day = 0
	if size >= 3:
		year = int(sys.argv[2])
	if size >= 4:
		month = int(sys.argv[3])
	else:
		month = 0
	if size >= 5:
		day = int(sys.argv[4])
	
	if year == 0:
		f = 0
		u =0
		while (f < 1900) | (f > date.today().year - 4):
			f = int(input("search from: "))
		while (u < f) | (u > date.today().year - 4):
			u = int(input("search until: "))
		year = findYear(user_id, name, f, u)
		
	if (month == 0) & (year > 0):
		month = findMonth(user_id, name, year)
		
	if (day == 0) & (month > 0) & (year > 0):
		day = findDay(user_id, name, year, month)
		
	if day*month*year == 0:
		print("Not found :(")
		sys.exit(0)
		
	if (month < 13) & (day <= days[month]) & (check(user_id, name, year, month, day)):
		print("Found: {}/{}/{}".format(day,month,year))
	else:
		print("Not found :(")
	