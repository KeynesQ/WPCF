import sublime, sublime_plugin
#coding: UTF-8
'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.30
 Last update 2013.01.30
 Version 0.9.0 beta
 Description Helpfull

'''
class helpfullCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.message_dialog('''Program: WPC\nVersion: 0.9.0.beta\nAuthor:KeynesQu <qukuilin@baidu.com>\nWeibo:KeynesQ\nLast update:20130220''')

