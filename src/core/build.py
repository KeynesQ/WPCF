import sys, os, inspect, re, urllib, random
#coding: UTF-8
#
'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.15
 Last update 2013.01.15
 Version 0.9.0 beta
 Description A new program to build

'''
from logs import *


'''The forder need to create'''
def fordersList():
	caller_file = inspect.stack()[1][1]
	path = os.path.abspath(os.path.dirname(caller_file))
	print path
	global __configJSON__
	if sys.platform == "win32":
		config = open(path + '\..\configure.conf')
		_config = [L for L in config]
		__configJSON__ = eval(''.join(_config))
		#_config = [L.rstrip('\n') for L in config if L[0] != '#']
	else:
		config = open(path + '/../configure.conf')
		#_config = [re.sub(r'\\', '/', L) for L in config]
		#_config = [re.sub(r'\\', '/', L) for L in config]
		_config = [re.sub(r'\\', '/', re.sub(r'\r', '', L)) for L in config]
		__configJSON__ = eval(''.join(_config))
	config.close()
	if str(type(__configJSON__)) != "<type 'dict'>" :
		Logger('SyntaxError in configure.conf:Can not be compile')
		return
	#远程读取
	if __configJSON__['compile']['build']['jssdk'] == True:
		
		__jdkcontent__ = urllib.urlopen('http://fe.baidu.com/~qukuilin/tools/compress/build/jssdk/jssdk.js?{0}'.format(random.random())).read()
		
		def writeFile(_file_, cnt):
			files = open(r'{0}'.format(_file_), 'w')
			files.writelines( cnt )
			files.close()
		if sys.platform == "win32":
			writeFile(path + r'\..\..\jssdk.js', __jdkcontent__)
		else:
			writeFile(path + r'/../../jssdk.js', __jdkcontent__)
		

	return __configJSON__['compile']['build']['forder']

'''Action Create'''
def mkdir(list, __Forder__='', path=os.path.abspath(os.path.dirname(inspect.stack()[1][1]))):
	for forder in list:

		if (str(type(forder)) == "<type 'str'>")|(str(type(forder)) == "<type 'dict'>") :
			
			
			#如果是dict类型则取出key
			recursion = []
			if str(type(forder)) == "<type 'dict'>":
				for _f_ in forder:
					#递归调用需要的对象
					recursion = forder[_f_]
					forder = _f_

			Logger( 'Create forder (' + re.sub(r'[.\\\/]*', '', forder) + ')' )

			try:
				if sys.platform == "win32":	
					
					#需要建立的文件夹
					__need2buildForder__ = path + "\..\..\src\\" + __Forder__ + r"{0}".format(forder)
					os.makedirs(__need2buildForder__)

					#判断是否需要jssdk
					if (forder == 'jssdk') & (__configJSON__['compile']['build']['jssdk'] == True):
						#print 'xcopy ' + path + r'\..\..\jssdk.js ' + r'{0}\\*'.format(__need2buildForder__) + ' /r/y/i '
						os.system('xcopy ' + path + r'\..\..\jssdk.js ' + r'{0}\\*'.format(__need2buildForder__) + ' /r/y/i ' )
						os.system('del ' + path + r'\..\..\jssdk.js /f/q')
					
					#递归建立子文件夹
					if len(recursion) > 0:
						mkdir(recursion, __Forder__ + forder + '\\')

					Logger( "Your forder of program is " + os.path.abspath(path + "\..\..\\") )

				else:

					#需要建立的文件夹
					__need2buildForder__ = path + "/../../src/" + __Forder__ + r"{0}".format(forder)

					os.makedirs(__need2buildForder__)

					if (forder == 'jssdk') & (__configJSON__['compile']['build']['jssdk'] == True):
						os.system('cp ' + path + '/../../jssdk.js ' +  r'{0}/jssdk.js'.format(__need2buildForder__) + ' -Rf ')
						os.system('rm -rf ' + path + '/../../jssdk.js')
					
					#递归建立子文件夹
					if len(recursion) > 0:
						mkdir(recursion, __Forder__ + forder + '/')

					Logger( "Your forder of program is " + os.path.abspath(path + "/../../") )

			except TypeError:
				pass
			except :
				Logger( "Forder (" + re.sub(r'[.\\\/]*', '', forder) + ") is exist" )
		else :
			Logger( "TypeError of configure.conf in build" )




'''Action Remove'''
def rd(list):
	for forder in list:
		caller_file = inspect.stack()[1][1]
		path = os.path.abspath(os.path.dirname(caller_file))
		Logger( 'Remove forder (' + re.sub(r'[.\\\/]*', '', forder) + ')' )
		try:
			if sys.platform == "win32":
				os.system('rd ' + path + "\..\..\src\\" + r"{0}".format(forder) + '/s/q')
			else:
				os.system('rm -rf ' + path + "/../../src/" + r"{0}".format(forder))
		except TypeError:
			pass
		except:
			Logger( "Forder (" + re.sub(r'[.\\\/]*', '', forder) + ") is exist" )