#coding=utf-8
import db_connector
import requests
import socket
import json
import re,sys
from pyes import * 
class DataInstall():

	'''
	获取标准url
	@param url 需要转化的url
	'''
	def get_standard_url(self,url):
		#判断传入的url是否为http开头
		if url.count("http") == 0:
			return "http://%s" % url
		else: 
			return url

	'''
	数据存储
	'''
	def datahandler(self,info):
		print info['url']
		url_with_http = self.get_standard_url(info['url'])
		item = {
			'ip':'',
			'domain':'',
			'serverinfo':'',
			'country':'',
			'city':'',
			'flag':'',
			'version':'',
			'http_response':'',
			'date':''
		}
		try:
			r = requests.get(url_with_http,timeout=8)
		except Exception, e:
			print e
			return -1
		

		#域名和IP
		domain = r.url
		try:
			if str(info['url']).count("/") == 0:
				ip = socket.gethostbyname(info['url'])
			else:
				s = str(info['url'])
				ip = socket.gethostbyname(s[:s.index("/")])
		except Exception, e:
			print e
			ip = 'unknown'
		
		
		#获取http response返回头
		http_response = r.headers

		#获取web服务器和操作系统类型
		try:
			serverinfo = r.headers['server']
		except KeyError, e:
			#没有server字段--->设置为unknown
			serverinfo = 'unknown'
			print e
		try:
			#获取ip信息
			ipinfoprovider = db_connector.GeoIPProvider()
			ret = ipinfoprovider.getIPInfos(ip)
			ipinfos = json.loads(ret)
			city = ipinfos[u'city']
			country = ipinfos[u'country_name']
		except Exception, e:
			print e
			city = 'unknown'
			country = 'unknown'

		#数据存储
		item['ip'] = str(ip)
		item['domain'] = str(domain)
		item['serverinfo'] = str(serverinfo)
		item['country'] = str(country)
		item['city'] = str(city)
		item['flag'] = 'discuz'
		item['version'] = info['version']
		item['http_response'] = str(http_response)

		print '-------------',ip,domain,serverinfo,country,city

		obj = db_connector.WebComponent(ip=item['ip'],domain=item['domain'],
			serverinfo=item['serverinfo'],country=item['country'],city=item['city'],
			flag=item['flag'],version=item['version'],http_response=item['http_response'])
		obj.save()

	'''将数据存入数据库'''
	def store(self,filename):
		f = open(filename,'r')
		infos = f.read()
		item = {'url':'','version':''}
		for info in infos.split('\n'):
			info = info.split('\t')
			item['url'] = info[0]
			item['version'] = info[1]
			if self.datahandler(item) == -1:
				print 'continue?'
				continue
		f.close()

	'''
	将数据导入es中
	'http_response':'string',
    'ip':'string',
    'domain':'string',
    'flag':'string',
    'version':'string',
    'serverinfo':'string',
    'country':'string',
    'city':'string'
	'''
	def es_data(self):
		es = ES("127.0.0.1:9200")
		#创建索引
		#es.indices.create_index("safecat")
		#设置mapping
		typeMapping = {
		    	'domain':{
		    		'type':'string'
		    	},
		    	'ip':{
		    		'type':'string'
		    	},
		        'flag':{
	               'type':'string'
			    },
			    'serverinfo':{
			    	'type':'string',
			    	'null_value':'unknown'
			    },
			    'date':{
			    	'type':'date'
			    },
			    'version':{
			    	'type':'string',
			    	'null_value':'unknown'
			    },
			    'country':{
			    	'type':'string',
			    	'null_value':'unknown'
			    },
			    'city':{
			    	'type':'string',
			    	'null_value':'unknown'
			    },
			    'http_response':{
			    	'type':'string'
			    }

		}
		
		#创建type
		es.indices.put_mapping("hostcrawler",{'properties':typeMapping},["safecat"])
		es.indices.refresh("safecat") # Single index
		#导入数据
		host_list = db_connector.WebComponent.objects.all()
		count = 1
		for info in host_list:
			doc = {
				'ip':info.ip,
				'domain':info.domain,
				'flag':info.flag,
				'serverinfo':info.serverinfo,
				'date':info.date,
				'version':info.version,
				'country':info.country,
				'city':info.city,
				'http_response':info.http_response
			}

			#插入数据
			res = es.index(doc,'safecat','hostcrawler',id=count)
			print res
			count += 1


if __name__ == '__main__':
	filename = 'results2.txt'
	storehelper = DataInstall()
	#storehelper.store(filename)
	storehelper.es_data()


