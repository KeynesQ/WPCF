import sublime, sublime_plugin, sys, os, inspect, re, urllib, random
#coding: UTF-8
from logs import *
'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.15
 Last update 2013.01.15
 Version 0.9.0 beta
 Description A new program to build

'''
__configJSON__ = {}

class fepackagebuildCommand(sublime_plugin.TextCommand):
	'''
	检查src目录是否存在
	@author KeynesQu
	create on 20130115
	@return {boolean} 是否存在目录
	'''
	def checkDir(self, path):
		#check the forder that named src
		if sys.platform == "win32":
			if len(os.listdir(path)) == 0 :
				os.makedirs(path + '\dev')
				return path + '\dev\\'
			elif os.path.exists(path + '\dev') & os.path.isdir(path + '\dev'):
				return path + '\dev\\'
			else :
				return path + '\\'
		else:
			if len(os.listdir(path)) == 0 :
				os.makedirs(path + '/dev')
				return path + '/dev/'
			elif os.path.exists(path + '/dev') & os.path.isdir(path + '/dev'):
				return path + '/dev/'
			else :
				return path + '/'
	def run(self, edit, **args):

		if sublime.platform() == 'windows':
			self.path = sublime.packages_path() + r'\FE-Package\\'
		else:
			self.path = sublime.packages_path() + r'/FE-Package/'
		self.__need2makePath__ = self.checkDir(''.join([L for L in open(self.path + 'make.path')]))
		self.cmd = {}
		#判断来源
		if len(args) > 0 :
			for arg in args:
				self.cmd[arg] = args[arg]
				if str(type(args[arg])) == "<type 'unicode'>":
					#print str(arg)
					#print type(self.cmd[arg])
					#print self.cmd[arg].decode('UTF-8')
					if (str(arg) == 'func') & (self.cmd[arg] == u'rd'.encode('UTF-8')):
						self.rd(args['path'])
					elif (str(arg) == 'func') & (self.cmd[arg] == u'mkdir'.encode('UTF-8')):
						self.mkdir(args['path'])
		else :
			self.mkdir(self.fordersList())


	'''The forder need to create'''
	def fordersList(self):
		path = self.path
		global __configJSON__
		if sys.platform == "win32":
			config = open(self.__need2makePath__ + 'configure.conf')
			_config = [L for L in config]
			__configJSON__ = eval(''.join(_config))
			#_config = [L.rstrip('\n') for L in config if L[0] != '#']
		else:
			config = open(self.__need2makePath__ + 'configure.conf')
			#_config = [re.sub(r'\\', '/', L) for L in config]
			#_config = [re.sub(r'\\', '/', L) for L in config]
			_config = [re.sub(r'\\', '/', re.sub(r'\r', '', L)) for L in config]
			__configJSON__ = eval(''.join(_config))
		config.close()
		if str(type(__configJSON__)) != "<type 'dict'>" :
			Logger('SyntaxError in configure.conf:Can not be compile')
			return			

		return __configJSON__['compile']['build']['forder']

	'''Action Create'''
	def mkdir(self, list, __Forder__=''):
		path = self.path
		__need2makePath__ = self.__need2makePath__
		for forder in list:

			if ((str(type(forder)) == "<type 'str'>")|(str(type(forder)) == "<type 'unicode'>"))|(str(type(forder)) == "<type 'dict'>") :
				
				
				#如果是dict类型则取出key
				recursion = []
				if str(type(forder)) == "<type 'dict'>":
					for _f_ in forder:
						#递归调用需要的对象
						recursion = forder[_f_]
						forder = _f_

				Logger(path, 'Create forder (' + re.sub(r'[.\\\/]*', '', forder) + ')' )

				try:
					if sys.platform == "win32":	
						
						#需要建立的文件夹
						__need2buildForder__ = __need2makePath__ + "src\\" + __Forder__ + r"{0}".format(forder)
						os.makedirs(__need2buildForder__)
						
						#递归建立子文件夹
						if len(recursion) > 0:
							self.mkdir(recursion, __Forder__ + forder + '\\')

						Logger(path, "Your forder of program is " + __need2makePath__ )

					else:

						#需要建立的文件夹
						__need2buildForder__ = __need2makePath__ + "src/" + __Forder__ + r"{0}".format(forder)

						os.makedirs(__need2buildForder__)
						
						#递归建立子文件夹
						if len(recursion) > 0:
							self.mkdir(recursion, __Forder__ + forder + '/')

						Logger(path, "Your forder of program is " + __need2makePath__ )

				except TypeError:
					pass
				except :
					Logger(path, "Forder (" + re.sub(r'[.\\\/]*', '', forder) + ") is exist" )
			else :
				Logger(path, "TypeError of configure.conf in build" )




	'''Action Remove'''
	def rd(self, list):
		path = self.path
		__need2makePath__ = self.__need2makePath__
		for forder in list:
			Logger(path, 'Remove forder (' + re.sub(r'[.\\\/]*', '', forder) + ')' )
			try:
				if sys.platform == "win32":
					os.system('rd ' + __need2makePath__ + "src\\" + r"{0}".format(forder) + '/s/q')
				else:
					os.system('rm -rf ' + __need2makePath__ + "src/" + r"{0}".format(forder))
			except TypeError:
				pass
			except:
				Logger(path, "Forder (" + re.sub(r'[.\\\/]*', '', forder) + ") remove failed" )