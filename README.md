WPCF
====

Web-App Package And Compress Fast
====

Copyright (c) 2013, KeynesQu. All rights reserved.

Author KeynesQu <qukuilin@gmail.com>

Description: 本工具能帮助你快速建立一套基于Web-App形式的前端目录、并且帮助你实现压缩打包的过程

Create on 2013/01/24

Last Update 2013/01/30

====

*** 使用说明：
	* 1、只需要配置一次configure.conf文件就能帮助你实现这些功能。* 为必填项
		compile属性里分两个属性分别为make和build属性
		make属性里主要配置编译打包需要的选项
			-base {dict} 基本配置
				-output {string} 输出目录 *
				-program {string} 项目名称 *
				-csspath {string} 默认CSS样式目录 *
				-manifest {dict} manifest文件配置
					-template {string} manifest文件模板
					-data {dict} manifest文件数据 如果数据为空则自动遍历目录下所有文件 key为要生成的文件 *
				-callback 回调文件
			-extend 扩展配置
				-excute {boolean} 是否运行扩展项
				-translate {string} 另外需要translate的文件以竖线分隔 DEMO:sourcefile|destFile|jsFile|cssFile
		build属性里目前只包含两个属性
			-jssdk {boolean} 是否需要jssdk文件
			-forder {tuple} 需要建立的文件目录结构 包含子目录的目录节点以字典表示
		注：dict类型类似于JavaScript里的JSON对象，tuple类型类似于JavaScript里的array数组
	* 2、工具使用方法（目前采用命令行下运行）
		1) 首先将目录从svn上down下来或者在我的FE站点上down下来,然后解压或拷贝到你的项目目录与[src]目录同级
			SVN:
			URL:
		2) win32：
			运行-cmd-'python {YourProgramPath}\\{ToolsPath}\core\run.py {argv}'
		   linux2:
		   	'python {YourProgramPath}/{ToolsPath}/core/run.py {argv}'
		   HelpInfo:
		   	============================================
			Arguments option:
			[maketest]      : Make the program to test
			[make]          : Make the program of online
			                [xxx]   : Callback "xxx.bat"
			[build]         : Build new program.
			[H or help]     : Help of this tool.
			============================================
	* 3、文件合并方法
		如果需要在代码中做局部文件合并，可将需要合并的文件代码写在如下的代码区块内
		ex:
			<!-- Rule:[name|async] identification -->
			<!-- [action|false] combinestart -->
			<script src="modules/datamodel.js"></script>
			<script src="modules/controller.js"></script>
			<!-- combineend -->
		demo中action是合并之后的文件名，用竖线分隔的后面为是否异步加载的选项（false则为同步，合并之后会嵌入合并的文件代码）。

*** 更新说明：
	[2013/01/28]
	1、增加统一配置文件
	2、增加是否需要jssdk文件 [需要访问内网]
	[2013/01/29]
	1、修改manifest为可配置是否自动遍历
	[2013/02/04]
	1、增加了configure通用
	[2013/03/03]
	1、增加了PNG图片压缩
