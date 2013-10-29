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

from build import *
from logs import *
from core2.template import *

__configJSON__ = {}
__need2makePath__ = ''


		



'''
转换模板文件的函数
@param content {string|buffer} 需要替换模板的文件内容
@param path {string|buffer} 打开模板的路径
@since 20130116
@update 20130116
@return {string} 替换后的内容
'''
def tpl(content, path):
	reg = re.compile(r'<tpl([\s\S]*?)>([\s\S]*?)<\/tpl>')
	srcreg = re.compile(r'[\S\s]*src *= *"([\s\S]*?)"')
	idreg = re.compile(r'[\S\s]*id *= *"([\s\S]*?)"')
	array = re.match(reg,content)
	scripttext = '<script type="text/template" id="#{id}">#{template}</script>'
	def replaceTemp(match):
		a = match.group(0)
		b = match.group(1)
		template = match.group(2)
		#print template
		#return match.group(0)
		srcarray = re.match(srcreg, b)
		if srcarray :
			src = srcarray.group(1)
			if sys.platform == "win32" :
				filename = path + "\..\..\src\\"+src.replace(r'\/',"\\")
			else :
				filename = path + '/../../src/' + src
			if os.path.exists(filename) :
				template = open(filename, 'r').read()
			else :
				Logger( 'IOError : No such file or directory in make.py def<tpl>:' + filename )
		idarray = re.match('[\s\S]*id *= *"([\s\S]*?)"', b)
		_id = ''
		if idarray :
			_id = idarray.group(1)

		print re.sub(r"#{template}", template, re.sub(r"#{id}", _id, scripttext))
		
	return reg.sub(replaceTemp, content)
'''
转换合并html、js、css等文件
@param _namespace {string|buffer} 命名空间
@param csspath {string|buffer} 样式文件的路径
@param path {string|buffer} 文件执行的绝对路径
@param _files {string|buffer}
@void
@since 20130115
@update 20130116
'''
def translate(_namespace, csspath, path, _files=''):
	'''
	这里要增加可配置的信息
	'''
	if _files != '':
		_fileTuple = _files.split('|')
		if len(_fileTuple) != 4 :
			sublime.error_message('Your files can not translate!About :' + _files)
			raise
			#return
		else :
			sourceFile 	= path + _fileTuple[0]
			destFile	= path + _fileTuple[1]
			jsFile		= path + _fileTuple[2]
			cssFile 	= path + _fileTuple[3]
	else :
		sourceFile 	= path + _namespace + '.html'
		destFile 	= path + _namespace + '.html'
		jsFile		= path + _namespace + '.js'
		cssFile		= path + csspath + _namespace + '.css'
	if os.path.exists(sourceFile):
		translog = '\n\r'.join(["Processing:", sourceFile, destFile, jsFile, cssFile])
		#Logger( translog )
		#读取源文件
		
		sourceFileOperate = open(sourceFile, 'r')
		content = sourceFileOperate.read()
		sourceFileOperate.close()
		if sys.platform == "win32":
			sourceDir = re.match(r"(.*\\)[^\\]*", sourceFile)
			sourceDir = sourceDir.group(1)
		else :
			sourceDir = re.match(r"(.*/)[^/]*", sourceFile)
			sourceDir = sourceDir.group(1)
		#print sourceDir
		styleContent = []
		jsContent = []

		'''
		写入文件
		@param containfile {string|buffer} 被写入的文件
		@param cnt {string|buffer} 要写入的内容
		'''
		def writeFile(containfile, cnt):
			files = open(r''+containfile+'', 'w')
			files.writelines( cnt )
			files.close()

		#替换的回调函数
		def replaceCSS(match):
			#print match.group(0)
			filename = sourceDir + ( match.group(1).replace(r'/', "\\") if sys.platform == "win32" else match.group(1) )
			#print filename
			
			files = open(filename, 'r')
			filecontent = files.read()
			files.close()
			styleContent.append(filecontent)

			return ''.join(['\t\t<link rel="stylesheet" type="text/css" href="resources/themes/default/styles/', re.sub(r'(.*?)\\(?=[^\\]+)', "" , cssFile), '" />']) if len(styleContent) == 1 else ""
			
		def replaceJS(match):
			#print match.group(1)
			filename = sourceDir + ( match.group(1).replace(r'/', "\\") if sys.platform == "win32" else match.group(1) )

			files = open(filename, 'r')
			filecontent = files.read()
			files.close()
			jsContent.append(filecontent)

			return ''.join(['\t\t<script src="', re.sub(r'(.*?)\\(?=[^\\]+)', "" , jsFile), '"></script>']) if len(jsContent) == 1 else ""


		#先替换出整体要分开合并的
		combine_pattern = re.compile(r'[ \f\t\v]*<!--\s*\[([^\]]*)\]\s+combinestart\s*-->([\s\S]*?)<!--\s*combineend\s*-->')
		css_pattern = re.compile(r'[ \f\t\v]*<link\s+[^>]*?href="(?!https?:)(?!components)(?!.*_ie6\.css)([^"]+\.css)"[^>]*?>[ \f\t\v]*')
		js_pattern	= re.compile(r'[ \f\t\v]*<script\s+[^>]*?src="(?!https?:)([^"]+\.js)"[^>]*?>[\s\S]*?<\/script>[ \f\t\v]*')
		#print content
		'''先将需要合并的文件替换成标识位'''
		_replaceIdentifer = [] #要替换的标识
		def combineFile(match):
			if match.group(1):
				_RuleTuple 		= match.group(1).split('|')
				_combineName 	= path + _RuleTuple[0] + '.js'#合并之后的文件名
				_async 			= _RuleTuple[1]#文件的异步请求
				_combineContent = []#合并内容
				_combinedFiles	= []#合并文件
				def _cbcnt(mat):
					_combinedFile = mat.group(1).replace(r'/', "\\") if sys.platform == "win32" else mat.group(1)
					filename = sourceDir + _combinedFile
					files = open(filename, 'r')
					filecontent = files.read()
					files.close()
					_combinedFiles.append(_combinedFile)
					_combineContent.append(filecontent)
					return ''.join(['\t\t<script src="', re.sub(r'(.*?)\\(?=[^\\]+)', "" , _combineName), '"></script>']) if len(_combineContent) == 1 else ""
				#将要合并的文件合并
				_importURL = js_pattern.sub(_cbcnt, match.group(2))
				Logger('Combine files ' + ','.join(_combinedFiles) + ' in file ' + _RuleTuple[0] + '.js')
				writeFile(_combineName, '\n'.join(_combineContent))
				_repTemp = {}
				_repTemp['_compile'] = re.compile(r'{cb%' + _RuleTuple[0] + '%}')
				_repTemp['_url'] = _importURL
				_replaceIdentifer.append(_repTemp)
				if _async == 'true':
					return ''
				else :
					return '{cb%' + _RuleTuple[0] + '%}'
			else :
				return ''
		content = combine_pattern.sub(combineFile, content)
		'''替换并将内容填充到元组'''
		content = css_pattern.sub(replaceCSS, content)
		#print content
		content = js_pattern.sub(replaceJS, content)
		#print content
		content = re.sub(r'\s*\n(?=\s*\n)', '', content)
		'''
		替换标识位
		'''
		if len(_replaceIdentifer) > 0 :
			for _req in _replaceIdentifer:
				def _repurl(mat):
					if mat.group(0):
						return _req['_url']
				content = _req['_compile'].sub(_repurl, content)

		writeFile(cssFile, '\n'.join(styleContent))

		writeFile(jsFile, '\n'.join(jsContent))

		content = tpl(content, path)
		
		writeFile(destFile, content)

		
		
	else :
		Logger( 'File ' + sourceFile + ' not exists' )


'''
替换manifest文件
@param _dir {string|buffer} 输出目录
@param listFile {string|buffer} 命令行生成的文件列表
@param path {string|buffer} 文件执行路径
@void
@since 20130116
@update 20130117
'''
def manifest(_dir, listFile, path):
	template = __configJSON__['compile']['make']['base']['manifest']['template']
	config = __configJSON__['compile']['make']['base']['manifest']['data']
	__dataLen__ = len(config)
	_list = open(listFile).read()
	array = _list.split("\n")
	result = []
	configarray = {}
	for key in config :
		value = config[key]
		tempa = []
		for k in value :
			_temp = re.sub(r'&', '[^\/]*', re.sub(r'\*', '.*', re.sub(r'\.', '\\.', re.sub(r'\/', "\\/", k))))
			tempa.append(_temp)
		Logger(path, 'Files need to cached :' + "|".join(tempa) )
		_obj = {"reg":re.compile( "|".join(tempa) ), "array":[]}
		configarray[key] = _obj
		Logger(path, 'Running in manifest, please wait!' )
	for i in array :
		i = re.sub(r'\\', '/', i.replace(_dir,''))
		for j in configarray:
			item = configarray[j]
			#如果数据配置为空则遍历文件
			if __dataLen__ > 0:
				if item['reg'].search(i) :
					#print i
					item['array'].append(i)
			else :
				item['array'].append(i)
	print configarray

	date = timegm(time.gmtime(time.time()))
	#print date
	for key in configarray :
		content = YayaTemplate(template).render({
			'time':date,
			'array':configarray[key]['array']
		})
		Logger(path, 'Cache file ====> ' + _dir + key )
		_openfile = open(_dir + key, 'w')
		_openfile.writelines(re.sub(r'[\f\t]*', '', content))
		_openfile.close()


'''
原syntax.js文件
@param listFile {string|buffer} 命令行生成的文件列表
@param path {string|buffer} 文件执行路径
@void
@since 20130117
@update 20130117
'''
def syntax(listFile, path):
	content = open(listFile).read();
	_flist	= content.split('\n')
	def getFileExtName(name):
		#print name
		len = name.rindex(".")
		#print len
		if len >= 0 :
			return name[len + 1:]
		return ""
	def patternJS(content):
		return re.sub(r'[ \f\t\v]*\/\*\s*debug\s+start\s*\*\/[\s\S]*?\/\*\s*debug\s+end\s*\*\/[ \f\t\v]*', '', content)
	def patternHTML(content):
		return re.sub(r'[ \f\t\v]*<!--\s*debug\s+start\s*-->[\s\S]*?<!--\s*debug\s+end\s*-->[ \f\t\v]*', '', content)
	def patternHTM(content):
		return re.sub(r'[ \f\t\v]*<!--\s*debug\s+start\s*-->[\s\S]*?<!--\s*debug\s+end\s*-->[ \f\t\v]*', '', content)
	def patternCSS(content):
		return re.sub(r'[ \f\t\v]*\/\*\s*debug\s+start\s*\*\/[\s\S]*?\/\*\s*debug\s+end\s*\*\/[ \f\t\v]*', '', content)
	_map = {
		"JS":patternJS,
		"HTML":patternHTML,
		"HTM":patternHTM,
		"CSS":patternCSS
	}
	#print _flist
	for fileIndex in _flist:
		#print fileIndex
		_filename = fileIndex
		#print _filename
		try :
			extname = getFileExtName(_filename).upper()
			#print extname
			if _map.get(extname) :
				content = open(_filename).read()
				content = _map[extname](content)
				#print _filename
				_writeFile = open(_filename, 'w')
				_writeFile.writelines(content)
				_writeFile.close()
			else :
				Logger('IgnoreWarning : ' + extname + ' not in map')
		except ValueError:
			Logger('Tempfile has no content in last line')
		except KeyError:
			Logger('Type of ' + _filename + ' not in map')
		else :
			Logger('Unknown')

'''
原compile.js文件
@param listFile {string|buffer} 命令行生成的文件列表
@param path {string|buffer} 文件执行路径
@since 20130117
@update 20130117
'''
def _Compile(listFile, path):
	content = open(listFile).read();
	_flist	= content.split('\n')
	def getFileExtName(name):
		#print name
		len = name.rindex(".")
		#print len
		if len >= 0 :
			return name[len + 1:]
		return ""
	def _template(tempBuf, _data):
		return YayaTemplate(tempBuf).render(_data)
	_compile = {
		"Template":_template
	}
	if sys.platform == 'win32':
		_ver = open(path + '\..\pro-conf\\version.ini').read()
	else :
		_ver = open(path + '/../pro-conf/version.ini').read()


	data = {
		"HDSpaceInfo":{
			"extension_api_version":_ver,
			"compile_date":str(datetime.date.today()) + ' ' + getHMS(time.gmtime(time.time())),
			"hudson_code":"{%hudson_code%}"
		}
	}

	def patternJS(content):
		def rep(match):
			a = match.group(0)
			b = match.group(1)
			c = match.group(2)
			d = match.group(3)
			if _compile.get(b) :
				return _compile[b](d,data[c])
			else:
				return a
		content = re.sub(r'[ \f\t\v]*\/\*\s*Compile:(\S*)\s*id="(\S*)"([\s\S]*?)\s*\*\/', rep, content)
		return content
	def patternHTML(content):
		def rep(match):
			a = match.group(0)
			b = match.group(1)
			c = match.group(2)
			d = match.group(3)
			if _compile.get(b) :
				return _compile[b](d,data[c])
			else:
				return a
		content = re.sub(r'[ \f\t\v]*<!--\s*Compile:(\S*)\s*id="(\S*)"([\s\S]*?)\s*-->', rep, content)
		return content
	def patternHTM(content):
		return _map["HTML"](content)
	def patternCSS(content):
		return _map["JS"](content)
	_map = {
		"JS":patternJS,
		"HTML":patternHTML,
		"HTM":patternHTM,
		"CSS":patternCSS
	}
	#print _flist
	for fileIndex in _flist:
		#print fileIndex
		_filename = fileIndex
		#print _filename
		try :
			extname = getFileExtName(_filename).upper()
			#print extname
			if _map.get(extname) :
				content = open(_filename).read()
				content = _map[extname](content)
				#print _filename
				_writeFile = open(_filename, 'w')
				_writeFile.writelines(content)
				_writeFile.close()
			else :
				Logger('IgnoreWarning : ' + extname + ' not in map')
		except ValueError:
			Logger('Tempfile has no content in last line')
		except KeyError:
			Logger('Type of ' + _filename + ' not in map')
		else :
			Logger('Unknown')



'''
Core Function:Main function of compile program
__configJSON__ 存储了configuer里的配置
@param option {boolean} 是否进行
@void
@since 20130113
@update 20130117
'''
class fepackagemakeCommand(sublime_plugin.TextCommand):
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
		compress = 'false'
		if args.get('compress'):
			compress = args['compress']
		#配置信息
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
		global __configJSON__
		__configJSON__ = self.__configJSON__
		
		#self.view.run_command('fepackagebuild')
		today = datetime.date.today()
		#set namespace tempfile
		tempfile = 'tempfile'
		#下面只用到make里的对象，统一一下
		__makeConfig__ = __configJSON__['compile']['make']
		
		if sys.platform == "win32":
			self.view.run_command('fepackagebuild', {"func":"rd","path":['\..\\' + __makeConfig__['base']['output'],]})
			self.view.run_command('fepackagebuild', {"func":"mkdir","path":['\..\\' + __makeConfig__['base']['output'],]})

			
			_Output = self.__need2makePath__ + __makeConfig__['base']['output'] + '\\'
			_Tempfile = self.__need2makePath__ + tempfile
			#_cssPath = re.sub(r'\\\\', '\\', __makeConfig__['base']['program']['csspath'])			
			_cssPath = __makeConfig__['base']['csspath']

			print self.__need2makePath__
			print _Output
			print self.__CurrentPackPath__ + 'logs\\' + str(today) + '.log'

			sysinfo = os.system(r'xcopy ' + self.__need2makePath__ + 'src\* ' + _Output + '\* /e/r/y/i >> "' + self.__CurrentPackPath__ + 'logs\\' + str(today) + '.log"')
			#print sysinfo
			Logger(self.__CurrentPackPath__, 'Copy to dir : ' + __makeConfig__['base']['output'] )
			

			#判断是否需要扩展
			if __makeConfig__['extend']['excute'] == True:

				_index = len(__makeConfig__['extend']['translate']) - 1
				#设置搜索起始点为3,当存在序号3以上的内容则默认认为它符合sourcefile|destFile|jsFile|cssFile这个条件
				_st = 0
				while _st <= _index:
					#print _st
					translate(__makeConfig__['base']['program'], _cssPath, _Output + '\\', __makeConfig__['extend']['translate'][_st])
					_st += 1
			else :
				translate(__makeConfig__['base']['program'], _cssPath, _Output + '\\')


			#将文件列表输出到tempfile文件
			os.system('dir ' + _Output + ' /s/b/a:-d > ' + _Tempfile)
			#调用manifest
			manifest(_Output, _Tempfile, self.__CurrentPackPath__)
			#回调函数
			print self.__need2makePath__
			if (__makeConfig__['base']['callback'] != "") | (__makeConfig__['base']['testcallback'] != ""):
				try :
					if compress == 'true' :
						os.system('call ' + self.__need2makePath__ + '\\' + __makeConfig__['base']['callback'] + '.bat ' + self.__need2makePath__)
					else :
						os.system('call ' + self.__need2makePath__ + '\\' + __makeConfig__['base']['testcallback'] + '.bat ' + self.__need2makePath__)
				except :
					Logger(self.__CurrentPackPath__,' Execute callback error ')
			if compress == 'true' :
				for __curr,__forder,__file in os.walk(_Output):
					if len(__file) > 0:
						for __compressfile in __file:
							
							if self.__getFileExtName(__compressfile).lower() == 'js' :
								__currFile = os.path.abspath(__curr) + '\\' + __compressfile
								try:
									#print 'java -jar "' + self.__CurrentPackPath__ + 'tools\yuicompressor-2.4.6.jar" --type js --charset utf-8 -o ' + __currFile + ' ' + __currFile
									os.system('java -jar "' + self.__CurrentPackPath__ + 'tools\yuicompressor-2.4.6.jar" --type js --charset utf-8 -o ' + __currFile + ' ' + __currFile)
									Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
								except:
									Logger(self.__CurrentPackPath__,' Execute yui error on file ' + __currFile)
								
							elif self.__getFileExtName(__compressfile).lower() == 'css' :
								__currFile = os.path.abspath(__curr) + '\\' + __compressfile
								
								try :
									os.system('java -jar "' + self.__CurrentPackPath__ + 'tools\yuicompressor-2.4.6.jar" --type css --charset utf-8 -o ' + __currFile + ' ' + __currFile)
									Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
								except :
									Logger(self.__CurrentPackPath__,' Execute yui error on file ' + __currFile)
			os.system('del ' + _Tempfile + '/f/q')	


			#for root

			#调用syntax
			#syntax( _Tempfile, path )
			#调用compile
			#_Compile( _Tempfile, path)
			
		else:
			self.view.run_command('fepackagebuild', {"func":"rd","path":['/../' + __makeConfig__['base']['output'],]})
			self.view.run_command('fepackagebuild', {"func":"mkdir","path":['/../' + __makeConfig__['base']['output'],]})

			
			_Output = self.__need2makePath__ + __makeConfig__['base']['output'] + '/'
			_Tempfile = self.__need2makePath__ + tempfile
			#_cssPath = re.sub(r'\\\\', '\\', __makeConfig__['base']['program']['csspath'])			
			_cssPath = re.sub(r'\\', '/',__makeConfig__['base']['csspath'])#linux path '/'


			#linux command
			os.system('cp ' + self.__need2makePath__ + 'src/* ' + _Output + ' -Rf')
			Logger(self.__CurrentPackPath__, 'Copy to dir : ' + __makeConfig__['base']['output'] )


			#判断是否需要扩展
			if __makeConfig__['extend']['excute'] == True:

				_index = len(__makeConfig__['extend']['translate']) - 1
				#设置搜索起始点为3,当存在序号3以上的内容则默认认为它符合sourcefile|destFile|jsFile|cssFile这个条件
				_st = 0
				while _st <= _index:
					#print _st
					translate(__makeConfig__['base']['program'], _cssPath, _Output + '/', __makeConfig__['extend']['translate'][_st])
					_st += 1
			else :
				translate(__makeConfig__['base']['program'], _cssPath, _Output + '/')

			#linux 命令
			os.system('ls ' + _Output + ' -RABC1F | grep \'[.:]\'|awk \'BEGIN{dir=""}/:$/{gsub(/\:/,"/");dir=$1;}/\./{print dir$1}\' > ' + _Tempfile)
			
			#调用manifest
			manifest(_Output, _Tempfile, self.__CurrentPackPath__)
			if (__makeConfig__['base']['callback'] != "") | (__makeConfig__['base']['testcallback'] != ""):
				try:
					if compress == 'true' :
						os.system('sh ' + self.__need2makePath__ + '\\' + __makeConfig__['base']['callback'] + '.sh ' + self.__need2makePath__)
					else :
						os.system('sh ' + self.__need2makePath__ + '\\' + __makeConfig__['base']['testcallback'] + '.sh ' + self.__need2makePath__)
				except :
					Logger(self.__CurrentPackPath__,' Execute callback error ')
			#调用syntax
			#syntax( _Tempfile, path )
			#调用compile
			#_Compile( _Tempfile, path)
			if compress == True :
				for __curr,__forder,__file in os.walk(_Output):
					if len(__file) > 0:
						for __compressfile in __file:
							
							if self.__getFileExtName(__compressfile).lower() == 'js' :
								__currFile = os.path.abspath(__curr) + '/' + __compressfile
								try:
									os.system('java -jar ' + self.__CurrentPackPath__ + 'tools/yuicompressor-2.4.6.jar --type js --charset utf-8 -o ' + __currFile + ' ' + __currFile)
									Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
								except:
									Logger(self.__CurrentPackPath__,' Execute yui error on file ' + __currFile)
								
							elif self.__getFileExtName(__compressfile).lower() == 'css' :
								__currFile = os.path.abspath(__curr) + '/' + __compressfile
								
								try :
									os.system('java -jar ' + self.__CurrentPackPath__ + 'tools/yuicompressor-2.4.6.jar --type css --charset utf-8 -o ' + __currFile + ' ' + __currFile)
									Logger(self.__CurrentPackPath__,' Compress succssfull on ' + __currFile)
								except :
									Logger(self.__CurrentPackPath__,' Execute yui error on file ' + __currFile)
				os.system('rm -rf ' + _Tempfile)
		
	