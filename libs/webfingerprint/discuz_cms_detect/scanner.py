#coding=utf-8
import requests
import urllib
import sys
import os
import socket
import time
import re
from ip_reverse import IPReverse
'''
网络扫描类
给定一个IP段   扫描指定端口
Demo：
给定202.203.208.8/24，扫描80端口
myscanner = Scanner()
ip_list = myscanner.WebScanner('202.203.208.0','202.203.208.255')
'''
class Scanner():
	#验证指定的IP和port是否开放
	def portScanner(self,ip,port=80):
	    server = (ip,port)
	    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	    sockfd.settimeout(0.05)
	    ret = sockfd.connect_ex(server)  #返回0则成功
	    if not ret:
	        sockfd.close()
	        print '%s:%s is opened...' % (ip,port)
	        return True
	    else:
	        sockfd.close()
	        print '%s:%s NO!' % (ip,port)
	        return False

	#字符串IP转化为数字的IP
	def ip2num(self,ip):
	    lp = [int(x) for x in ip.split('.')]
	    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 |lp[3]

	#数字的IP转化为字符串
	def num2ip(self,num):
	    ip = ['','','','']
	    ip[3] = (num & 0xff)
	    ip[2] = (num & 0xff00) >> 8
	    ip[1] = (num & 0xff0000) >> 16
	    ip[0] = (num & 0xff000000) >> 24
	    return '%s.%s.%s.%s' % (ip[0],ip[1],ip[2],ip[3])

	#计算输入的ip范围
	def iprange(self,ip1,ip2):
	    num1 = self.ip2num(ip1)
	    num2 = self.ip2num(ip2)
	    tmp = num2 - num1
	    if tmp < 0:
	        return None
	    else:
	        return num1,num2,tmp
	#扫描函数
	def WebScanner(self,startip,endip,port=80):
	    ip_list = []
	    res = ()
	    res = self.iprange(startip,endip)
	    if res < 0:
	        print 'endip must be bigger than startone'
	        return None
	        sys.exit()
	    else:
	        for x in xrange(int(res[2])+1):
	            startipnum = self.ip2num(startip)
	            startipnum = startipnum + x
	            if self.portScanner(self.num2ip(startipnum),port):
	                ip_list.append(self.num2ip(startipnum))
	        return ip_list