import sublime, sublime_plugin, random, datetime
#coding: UTF-8
import os, sys
from core2.template import *

'''

 Copyright (c) 2013, Baidu Inc. All rights reserved.
 Author KeynesQu <qukuilin@baidu.com>
 Pro. Client-FE , Dept. Client Software
 Since 2013.01.30
 Last update 2013.01.30
 Version 0.9.0 beta
 Description excute command of making | making test | build

'''

def __mainTemplate__():
	return '''
	[
		{
			"caption": "Choose Program",
			"id": "choosecompiledprogram",
			"children":
			[
				{ "command": "loadprogram", "caption": "Load Program"},
				{ "command": "resetprogram", "caption": "Reset"},
				{ "caption": "-", "id": "end" },
				{%programs%}
				{ "caption": "-", "id": "end" }
			]
		}
	]
	'''
'''
检查是否符合压缩规范
Since 2013.02.20
'''
def checkDir(path):
	print len(os.listdir(path))
	if sys.platform == "win32":
		if len(os.listdir(path)) == 0 :
			os.makedirs(path + '\dev')
			return path + '\dev\\'
		elif os.path.exists(path + '\dev') & os.path.isdir(path + '\dev'):
			return path + '\dev\\'
		elif os.path.exists(path + '\src') & os.path.isdir(path + '\src') :
			return path + '\\'
		else:
			sublime.error_message('The program can not compiled!\nPlease rechoose!')
			raise

	else:
		if len(os.listdir(path)) == 0 :
			os.makedirs(path + '/dev')
			return path + '/dev/'
		elif os.path.exists(path + '/dev') & os.path.isdir(path + '/dev'):
			return path + '/dev/'
		elif os.path.exists(path + '/src') & os.path.isdir(path + '/src') :
			return path + '/'
		else:
			sublime.error_message('The program can not compiled!\nPlease rechoose!')
			raise

'''
编辑配置文件命令
Since 2013.01.30
Last update 2013.01.30
'''
class fepackageconfigCommand(sublime_plugin.WindowCommand):
	def run(self):
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			path = sublime.packages_path() + r'\FE-Package\\'
		else:
			path = sublime.packages_path() + r'/FE-Package/'
		self.window.open_file(checkDir(''.join([L for L in open(path + 'make.path')])) + 'configure.conf')

'''
查看日志
Since 2013.02.02
Last update 2013.02.02
'''
class fepackagelogCommand(sublime_plugin.WindowCommand):
	def run(self):
		today = datetime.date.today()
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			path = sublime.packages_path() + r'\FE-Package\logs\\' + str(today) + '.log'
		else:
			path = sublime.packages_path() + r'/FE-Package/logs/' + str(today) + '.log'
		self.window.open_file(path)

'''
查看帮助
Since 2013.02.02
Last update 2013.02.02
'''
class fepackagehelpCommand(sublime_plugin.WindowCommand):
	def run(self):
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			path = sublime.packages_path() + r'\FE-Package\readme'
		else:
			path = sublime.packages_path() + r'/FE-Package/readme'
		self.window.open_file(path)

'''
配置路径命令
为每个项目生成配置文件
Since 2013.01.31
Last update 2013.01.31
'''
class pathconfigCommand(sublime_plugin.TextCommand):
	def run(self, edit, **kwargs):
		#print self.window.forders()

		_sys = {}
		for __path in kwargs:
			_sys[__path] = kwargs[__path]
		
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			_packpath = sublime.packages_path() + r'\FE-Package\\'
		else:
			_packpath = sublime.packages_path() + r'/FE-Package/'
		if os.path.isfile(checkDir(_sys['path']) + 'configure.conf'):
			print 'Exist file'
		else :
			defaultConfigFile = open(_packpath + 'configure.conf', 'r')
			defaultConfigContent = [re.sub(r'{program}', r'{0}'.format(_sys['name']), L) for L in defaultConfigFile]
			defaultConfigFile.close()

			confpath = checkDir(_sys['path']) + 'configure.conf'
			_confile = open(confpath, 'w')
			_confile.writelines(''.join(defaultConfigContent))
			_confile.close()
			self.view.window().open_file(confpath)
		

		#替换Main选项
		_reg = re.compile(r'{0}'.format(_sys['id']))
		_MainFile_ = open(_packpath+'Main.sublime-menu', 'r')
		_MainRep_ = [(lambda L:re.sub(r'"caption": "{0}"'.format(_sys['name']), r'"caption": "{0}[seleted]"'.format(_sys['name']), L.rstrip('\n')) if _reg.search(L) else re.sub(r'\[seleted\]', '', L.rstrip('\n')))(L) for L in _MainFile_]
		_MainFile_.close()

		
		_MainFile_ = open(_packpath+'Main.sublime-menu', 'w')
		_MainFile_.writelines('\n'.join(_MainRep_))
		_MainFile_.close()

		#存储编译目录
		_packfile = open(_packpath+'make.path', 'w')
		_packfile.writelines(kwargs['path'])
		_packfile.close()
		


'''
读取列表
TODO:目前会存在中文出错问题
Since 2013.01.31
Last update 2013.01.31
'''
class loadprogramCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#print self.window.forders()
		_folder_ = self.view.window().folders()
		__mapping__ = {}
		__mapping__['programs'] = []
		for _path_ in _folder_:
			_random = int(random.random()*1000000)
			if sublime.platform() == 'windows':
				_caption = re.match(r".*\\([^\\]*)", _path_).group(1)
				_tempStr_ = '{ "command": "pathconfig", "caption": "' + _caption + '", "args":{"path":"' + re.sub(r'\\', r'\\\\', _path_) + '", "id":"keynes' + str(_random) + '", "name":"' + _caption + '"}},'
			else :
				_caption = re.match(r".*/([^/]*)", _path_).group(1)
				_tempStr_ = '{ "command": "pathconfig", "caption": "' + _caption + '", "args":{"path":"' + _path_ + '", "id":"keynes' + str(_random) + '", "name":"' + _caption + '"}},'
			print re.sub(r'\\', r'\\\\', _path_)
			__mapping__['programs'].append(_tempStr_)
		_MainRep_ = KeyTemplate(__mainTemplate__()).render({
			"programs":__mapping__['programs']
		})
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			_packpath = sublime.packages_path() + r'\FE-Package\Main.sublime-menu'
		else:
			_packpath = sublime.packages_path() + r'/FE-Package/Main.sublime-menu'
		_packfile = open(_packpath, 'w')
		_packfile.writelines(_MainRep_)
		_packfile.close()




'''
重置列表
Since 2013.01.31
Last update 2013.01.31
'''
class resetprogramCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		__mapping__ = {}
		__mapping__['programs'] = []
		_tempStr_ = '{ "command": "NothingUnload" },'
		__mapping__['programs'].append(_tempStr_)
		_MainRep_ = YayaTemplate(__mainTemplate__()).render({
			"programs":__mapping__['programs']
		})
		#配置文件为packages目录下FE-Package目录
		if sublime.platform() == 'windows':
			_packpath = sublime.packages_path() + r'\FE-Package\\'
		else:
			_packpath = sublime.packages_path() + r'/FE-Package/'
		_packfile = open(_packpath + 'Main.sublime-menu', 'w')
		_packfile.writelines(_MainRep_)
		_packfile.close()

		_packfile = open(_packpath + 'make.path', 'w')
		_packfile.writelines('\n')
		_packfile.close()

#-------------------------------------  side bar 命令  -----------------------------------------------

'''
拷贝jssdk文件
Since 2013.02.21
Last update 2013.02.21
'''
class copyjssdkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()
		#print self.view.sel()
		#print self.view.full_line(sel)
		#print self.view.find_by_selector(sel)
		#print self.view.substr(sel)
