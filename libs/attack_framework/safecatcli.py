#coding=utf-8
import os
import imp
import sys
from optparse import OptionParser,OptionGroup
from conf.safecat import *
# sys.path.append('./exploit')
# sys.path.append('./exploit/discuz')
from libs.exploit_module import EXPModule
from libs.keywords_module import KEYModule
from exploit.discuz import *
from libs.exploit_http import EXPHttp
class Safecatcli():
	def __init__(self):
		self.exp_module = None
		self.keywords_module = None
		self.httptools = EXPHttp()


	def optionInit(self):

		parser = OptionParser()
		parser.add_option('-m','--module',help="Define the name of module[exp_name/flag]"
			,dest='module_name')
		parser.add_option('-n','--name',help="Define the name of exploit file",
			dest='exp_name')
		parser.add_option('-u','--url',help="Define the target url or ip addr",
			dest='thost')

		exp_module = OptionGroup(parser,'Exploit module')
		exp_module.add_option('-o','--option',help="Define Scan type",
			dest="option")
		exp_module.add_option('-s','--startip',help="Define the start ip addr in your range",
			dest='startip')
		exp_module.add_option('-e','--endip',help="Define the end ip addr in your range",
			dest='endip')
		parser.add_option_group(exp_module)

		flag_module = OptionGroup(parser,'Keyword module')
		flag_module.add_option('-c','--class',help="Define the name of class",
			dest='class_name')
		flag_module.add_option('-q','--query',help="Define the query string",
			dest='query')
		parser.add_option_group(flag_module)	

		(option,args) = parser.parse_args()
		return (option,args)


	def loaddir(self):
		for x in os.walk(ROOT_PATH):
			sys.path.append(x[0].replace('\\','/'))
			

	def run(self):
		(option,args) = self.optionInit()
		print (option,args)
		self.loaddir()

		if (option.module_name == 'exp_name'):

			if (option.option == 'all'):
				print u'全网扫描模式'
				#动态获取具体的exploit对象
				sys.path.append(path)
				fp, pathname, description = imp.find_module(option.exp_name)
				exp_file = imp.load_module(option.exp_name, fp, pathname, description)
				exp_file = exp_file.SafecatExploit()
				self.exp_module = EXPModule(exp_file)
				self.exp_module.scanAll()

			elif (option.option == 'single') and (option.thost):
				print u'单个主机扫描'
				target = self.httptools.get_standard_url(option.thost)
				fp, pathname, description = imp.find_module(option.exp_name)
				exp_file = imp.load_module(option.exp_name, fp, pathname, description)
				exp_file = exp_file.SafecatExploit()
				print exp_file
				#exp_file = eval(option.exp_name) #载入相关的exploit脚本
				self.exp_module = EXPModule(exp_file)
				self.exp_module.scanOneHost(target)

			elif (option.option == 'range') and (option.startip) and (option.endip):
				print u'IP段扫描'
				startip = option.startip
				endip = option.endip
				fp, pathname, description = imp.find_module(option.exp_name)
				exp_file = imp.load_module(option.exp_name, fp, pathname, description)
				exp_file = exp_file.SafecatExploit()
				self.exp_module = EXPModule(exp_file)
				self.exp_module.scanOneRange(startip,endip)

			else:
				print u'Args invalid'

		elif (option.module_name == 'flag'):

			if option.class_name and option.query:
				print u'根据关键词从es中查找攻击'
				self.keywords_module = KEYModule(option.class_name)
				self.keywords_module.scanByQuery(option.query)
				
			elif option.class_name and option.thost:
				print u'根据es中的单个域名攻击'
				self.keywords_module = KEYModule(option.class_name)
				self.keywords_module.scanByDomain(option.thost)
			else:
				print u'Args invalid'


if __name__ == '__main__':
	cli = Safecatcli()
	cli.run()
	# for x in os.walk(ROOT_PATH):
	# 	print x[0].replace('\\','/')









