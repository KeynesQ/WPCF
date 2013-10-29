import sublime, sublime_plugin, sys, os, datetime, re
#coding: UTF-8

'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.15
 Last update 2013.01.15
 Version 0.9.0 beta
 Description Program to compile

'''
from logs import *
'''
压缩PNG图片
__configJSON__ 存储了configuer里的配置
@param option {boolean} 是否进行
@void
@since 20130113
@update 20130117
'''
class pngcompressCommand(sublime_plugin.TextCommand):
	'''
	返回扩展名
	@param name {string|buffer} 文件名
	@return {string|buffer} 文件扩展名
	@since 20130120
	@lastupdate 20130120
	'''

	def __getFileExtName(self, name):
			#print name
			try :
				len = name.rindex(".")
				#print len
				if len >= 0 :
					return name[len + 1:]
				else :
					return ''
			except:
				return ''
	'''
	检查src目录是否存在
	@author KeynesQu
	create on 20130115
	@return {boolean} 是否存在目录
	'''
	def checkDir(self, path):
		#check the forder that named src
		if re.sub(r'[ \t\f\r\n]*', '', path) == '':
			sublime.error_message('The program not exist!\nPlease click [Choose Program] to choose one!')
			raise

		if sys.platform == "win32":
			if os.path.exists(path + '\dev') & os.path.isdir(path + '\dev'):
				return path + '\dev\\'
			elif os.path.exists(path + '\src') & os.path.isdir(path + '\src') :
				return path + '\\'
			else:
				sublime.error_message('The program can not compiled!\nPlease rechoose!')
				raise
		else:
			if os.path.exists(path + '/dev') & os.path.isdir(path + '/dev'):
				return path + '/dev/'
			elif os.path.exists(path + '/src') & os.path.isdir(path + '/src') :
				return path + '/'
			else:
				sublime.error_message('The program can not compiled!\nPlease rechoose!')
				raise
	def run(self, edit, **args):
		if sublime.platform() == 'windows':
			self.__CurrentPackPath__ = sublime.packages_path() + r'\FE-Package\\'
			self.__need2makePath__ = self.checkDir(''.join([L for L in open(self.__CurrentPackPath__ + 'make.path')]))
		else:
			self.__CurrentPackPath__ = sublime.packages_path() + r'/FE-Package/'
			self.__need2makePath__ = self.checkDir(''.join([L for L in open(self.__CurrentPackPath__ + 'make.path')]))
		#print self.__CurrentPackPath__
		
		#print self.__need2makePath__
		self.__configJSON__ = eval(''.join([L for L in open(self.__need2makePath__ + 'configure.conf')]))
		#print self.__configJSON__
		
		if str(type(self.__configJSON__)) != "<type 'dict'>" :
			Logger(self.__CurrentPackPath__, 'SyntaxError in configure.conf:Can not be compile')
			return
		needCompressPath = self.__configJSON__['compile']['pngcompress']
		if len(needCompressPath) > 0:
			pass
		else :
			needCompressPath = self.__need2makePath__
		if sys.platform == "win32":
			for __curr,__forder,__file in os.walk(needCompressPath):
				if len(__file) > 0:
					for __compressfile in __file:
						if self.__getFileExtName(__compressfile).lower() == 'png' :
							__currFile = os.path.abspath(__curr) + '\\' + __compressfile
							try:
								#print 'java -jar "' + self.__CurrentPackPath__ + 'tools\yuicompressor-2.4.6.jar" --type js --charset utf-8 -o ' + __currFile + ' ' + __currFile
								print '"' + self.__CurrentPackPath__ + 'tools\pngcrush" -rem alla -brute -reduce ' + __currFile + ' ' + __currFile
								os.system('"' + self.__CurrentPackPath__ + 'tools\pngcrush"  -rem alla -brute -reduce ' + __currFile + ' ' + __currFile + '.png')
								os.system('xcopy "' + __currFile + '.png" "' + __currFile + '" /y')
								Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
							except:
								Logger(self.__CurrentPackPath__,' Execute pngcompress error on file ' + __currFile)
		else:
			for __curr,__forder,__file in os.walk(needCompressPath):
				if len(__file) > 0:
					for __compressfile in __file:
						if self.__getFileExtName(__compressfile).lower() == 'png' :
							__currFile = os.path.abspath(__curr) + '\\' + __compressfile
							try:
								#print 'java -jar "' + self.__CurrentPackPath__ + 'tools\yuicompressor-2.4.6.jar" --type js --charset utf-8 -o ' + __currFile + ' ' + __currFile
								os.system('pngcrush -rem alla -brute -reduce ' + __currFile + ' ' + __currFile + '.png')
								os.system('cp "' + __currFile + '.png" "' + __currFile + '" -f')
								Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
							except:
								Logger(self.__CurrentPackPath__,' Execute pngcompress error on file ' + __currFile)
