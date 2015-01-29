#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from discuz_feature import matches
'''
Discuz 指纹识别
1.meta数据元识别
2.intext识别
3.robots.txt识别
'''
class DiscuzDetector():
	'''构造方法'''
	def __init__(self,url):
		if url.startswith("http://"):
			self.url = url
		else:
			self.url = "http://%s" % url
		try:
			self.r = requests.get(self.url,timeout=8)
			self.page_content = self.r.content
		except Exception, e:
			print e
			self.r = None
			self.page_content = None
		
	'''识别meta标签'''
	def meta_detect(self):
		if not self.r:
			return False
		pattern = re.compile(r'<meta name=".*?" content="(.+)" />')
		infos = pattern.findall(self.page_content)
		conditions = matches['meta'][0] or matches['meta'][1]
		if infos:
			for x in infos:
				if x.count(conditions) != 0:
					return True
					break
		else:
			return False


	'''discuz 版本识别 xx-->7.0  Xx---->X2.5'''
	def robots_dz_xx_detect(self):
		if not self.r:
			return (False,None)
		robots_url = "%s%s" % (self.url,"/robots.txt")
		robots_content = requests.get(robots_url).content
		if not robots_content:
			return (False,None)
		robots_feature_xx = matches['robots_for_xx']
		robots_feature_Xx = matches['robots_for_Xx']
		robots_list = robots_content.split("\r\n")
		pattern = re.compile(r'# robots\.txt for (.+)')
		version_info = []
		for x in robots_list:
			#如果robots.txt中含有# robots.txt for Discuz! X3 行  则直接判断版本
			version_info = pattern.findall(x)
			if version_info != [] and robots_content.count("Version" and "Discuz!"):
				if robots_content.count("Version" and "Discuz!"):
					pattern = re.compile(r'# Version (.+)')
					version_number = pattern.findall(str(robots_content))
					if version_number:
						version_info.append(version_number)
				return (True,version_info)
			else:
				#若版本信息被删除则识别出版本
				is_xx = (x in robots_feature_xx)
				is_Xx = (x in robots_feature_Xx)
				if is_Xx or is_xx:
					#判断为discuz
					#判断版本
					if is_Xx == True:
						version_info = 'Discuz Xx'
						return (True,version_info)
					else:
						version_info = 'Discuz xx'
						return (True,version_info)
		#不是discuz
		return (False,None)



	'''检测网页中的discuz字样'''
	def detect_intext(self):
		if not self.r:
			return False
		text_feature = matches['intext'][0] or matches['intext'][1]
		if self.page_content.count(text_feature) != 0:
			return True
		else:
			return False


	'''判别方法'''
	def get_result(self):
		if not self.r:
			return (False,'Not Discuz!')
		is_meta = self.meta_detect()
		res = self.robots_dz_xx_detect()
		is_dz_robots = res[0]
		version_info = res[1]
		print version_info
		is_intext = self.detect_intext()

		if is_meta or is_dz_robots or is_intext:
			#print 'Find Discuz!'
			if version_info:
				# return (True,'Find! Version:%s' % (version_info[0]))
				return (True,'%s' % (version_info[0]))
			else:
				return (True,'Version:Unknown') 
		else:
			return (False,'Not Discuz!')
    	

if __name__ == '__main__':
	#url = 'http://www.waterok.com/bbs/'
	# url = "bbs.rainmeter.cn"
	# #url = "bbs.lengxiaohua.com"
	# detector = DiscuzDetector(url)
	# print detector.get_result()
	# f = open('data1.txt','rb')
	# dz_list = []
	# for x in f:
	# 	dz_list.append(x.replace('\r\n',''))
	# f.close()

	# for x in dz_list:
	# 	url = x
	# 	print '-'*60
	# 	print url
	# 	detector = DiscuzDetector(url)
	# 	res = detector.get_result()
	# 	print res
	'''读文件识别'''
	f = open('discuz.txt','r')
	wf = open('results2.txt','a')
	file_content = f.read()
	dz_url_list = file_content.split('\n')
	for url in dz_url_list:
		print url
		detector = DiscuzDetector(url)
		ret = detector.get_result()
		print ret
		if ret[0]:
			wf.write("%s\t%s\n" % (url,ret[1]))
		else:
			continue
	wf.close()
	f.close()


	



