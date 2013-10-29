import sys, os, inspect, datetime, time
#coding: UTF-8

'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.15
 Last update 2013.01.15
 Version 0.9.0 beta
 Description Logs record

'''

def _d(y, m, d, days=(0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365)):
	return (((y - 1901)*1461)/4 + days[m-1] + d + ((m > 2 and not y % 4 and (y%100 or not y%400)) and 1))


def timegm(tm, epoch=_d(1970, 1, 1)):
	year, month, day, h, m, s = tm[:6]
	assert year >= 1970
	assert 1 <= month <= 12
	return (_d(year, month, day) - epoch)*86400 + h*3600 + m*60 +s

def getHMS(tm, epoch=_d(1970, 1, 1)):
	year, month, day, h, m, s = tm[:6]
	Hours = (h+8)%24
	return ('0' + str(Hours) if Hours < 10 else str(Hours)) + ':' + ('0' + str(m) if m < 10 else str(m)) + ':' + ('0' + str(s) if s < 10 else str(s))

def Logger(log):
	caller_file = inspect.stack()[1][1]
	path = os.path.abspath(os.path.dirname(caller_file))
	today = datetime.date.today()
	print log
	if type(log) == list :
		log = ','.join(log)
	if sys.platform == "win32":
		logfile = open(path + '\..\logs\\' + str(today) + '.log', 'ab')
		logfile.writelines(	getHMS(time.gmtime(time.time())) + '		' + log + '\n')
		logfile.close()
	else :
		logfile = open(path + '/../logs/' + str(today) + '.log', 'ab')
		logfile.writelines( getHMS(time.gmtime(time.time())) + '		' + log + '\n' )
		logfile.close()

