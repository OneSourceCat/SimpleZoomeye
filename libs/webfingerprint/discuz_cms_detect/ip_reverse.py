#coding=utf-8
'''
IP反查域名类
demo:
获取与202.20.2.1绑定的域名列表
ipre = IPReverse();
ipre.getDomainsList('202.20.2.1')
'''
import requests
import json
import urllib
import sys
import os
import socket
import time
import re
from bs4 import BeautifulSoup
class IPReverse():
	#获取页面内容
	def getPage(self,ip,page):
	    r = requests.get("http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=%d" % (ip,page))
	    return r

	#获取最大的页数
	def getMaxPage(self,ip):
	    r = self.getPage(ip,1)
	    json_data = {}
	    json_data = r.json()
	    if json_data == None:
	    	return None
	    maxcount = json_data[u'conut']
	    maxpage = int(int(maxcount)/20) + 1    
	    return maxpage

	#获取域名列表
	def getDomainsList(self,ip):
	    maxpage = self.getMaxPage(ip)
	    if maxpage == None:
	    	return None
	    result = []
	    for x in xrange(1,maxpage+1):
	        r = self.getPage(ip,x)
	        result.append(r.json()[u"domains"])
	    return result



