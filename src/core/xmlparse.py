from xml.parsers import expat
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

class xmlParser:
	def __init__(self):
		self._parser = expat.ParserCreate()
		self._parser.StartElementHandler = self.start
		self._parser.EndElementHandler = self.end
		self._parser.CharacterDataHandler = self.data
		#存储对象
		self.__dataObj__ = {}
		#存储临时标签
		self.__tempTag__ = ''
		#只校验这些标签
		self.sigTag = '''
			output,program,csspath,manifest,template,data,extend,translate,make,build,jssdk
		'''
	def feed(self, data):
		self._parser.Parse(data, 0)

	def close(self):
		self._parser.Parse("", 1)
		del self._parser

	def start(self, tag, attrs):
		#self.__tempTag__ = tag
		#self.__dataObj__
		print "Start:", repr(tag), attrs

	def end(self, tag):
		print "End", repr(tag)

	def data(self, data):
		print "Data",repr(data)
