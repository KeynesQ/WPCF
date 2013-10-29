import sublime, sublime_plugin
#coding: UTF-8
'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.30
 Last update 2013.01.30
 Version 0.9.0 beta
 Description Insert tag to combine

'''
class fepackagecombineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for s in reversed(self.view.sel()):
			if s.empty():
				self.view.insert(edit, s.b, '''
					<!-- U should modify the 'name' & 'async' that u want in this example --> 
					<!-- [name|async] combinestart -->
						<!-- Insert script tag that u want to combine -->
					<!-- combineend -->
				''')

