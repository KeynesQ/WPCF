import sys, os
#coding: UTF-8


'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.14
 Last update 2013.01.15
 Version 0.9.0 beta
 Description Program of FE to package & compile in a multi-platform environment

'''

from build import *
from make import *
from logs import *
import help


_splitStartDesc = []
for i in range(70):
	_splitStartDesc.append('-')

Logger('\n\r' + ''.join(_splitStartDesc) + '\n\r')
Logger("  Copyright (c) 2013, Baidu Inc. All rights reserved." + '\n\r')
Logger("  Author KeynesQu <qukuilin@baidu.com>" + '\n\r')
Logger("  Pro. Client-FE , Dept. Client Software" + '\n\r')
Logger("  Version:0.9.0 beta")
Logger('\n\r' + ''.join(_splitStartDesc) + '\n\r')
print 'Your system is ' + sys.platform
print 'Your current forder is ' + os.path.abspath('.')

def returnFalse():
	return False
def returnTrue():
	return True
if len(sys.argv) == 1:
	Logger( 'Nothing in arguments' )
	help.helpinfo('')
	print 'Please input H or help to see help of this tool again'

else:
	if len(sys.argv) > 1:
		run = {
			'make':make,
			'maketest':make,
			'build':mkdir,
			'help':help.helpinfo,
			'H':help.helpinfo
		}[sys.argv[1]]

		arg = {
			'make':returnTrue,
			'maketest':returnFalse,
			'build':fordersList,
			'help':lambda:'',
			'H':lambda:''
		}[sys.argv[1]]()
		#print arg
		run(arg)