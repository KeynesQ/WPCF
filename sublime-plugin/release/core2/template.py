import sys, os, re
#coding: UTF-8

'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.17
 Last update 2013.01.17
 Version 0.9.0 beta
 Description Translate File KeyTemplate

'''
#how to use?  KeyTemplate("xxx").render({});


'''
在python中使用类达到相似的效果
@param tempBuf {string|buffer} 初始化时被处理的模板字符串
'''
class KeyTemplate:
	def __init__(self, tempBuf):
		self.text = tempBuf
	'''
	@param text {string|buffer} 初始化时被处理的模板字符串
	@param mapping {object} 需要遍历的对象
	'''
	def _analyze(self, text, mapping):
		#核心方法
		def replaceTxt(Match):
			#print Match.group(0)
			if Match :
				s = Match.group(0)
				name = Match.group(1)
				for _key in mapping:
					if name == _key:
						_value = mapping[_key]
						#print type(_value)
						if type(_value) == int:
							return str(_value)
						elif type(_value) == list:
							return '\n'.join(_value)
						elif type(_value) == str:
							return _value
						else:
							return ''
		return re.sub(r'{\%([\s\S]*?)\%}', replaceTxt, text)

	'''
	@param mapping {object} 需要遍历的对象
	'''
	def render(self, mapping):
		return self._analyze(self.text, mapping)