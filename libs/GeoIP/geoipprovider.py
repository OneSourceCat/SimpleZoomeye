#coding=utf-8
'''
{u'city': u'Kunming', 
u'continent_code': u'AS',   时区
u'region': u'29', 
u'area_code': None, 
u'longitude': 102.7183, 
u'metro_code': None, 
u'country_code3': u'CHN',
u'latitude': 25.0389, 
u'postal_code': None, 
u'dma_code': None, 
u'country_code': u'CN', 
u'country_name': u'China'}
'''
import json
import os
import subprocess
class GeoIPProvider():
	def getIPInfos(self,ip):
		command = "php E:/School_of_software/information_security/holiday-learning/python/django/safecat/libs/GeoIP/getInfoByPHP.php {ip_str}".format(ip_str=ip)
		res = os.popen(command)
		infos = res.read()
		res.close()
		if res == str(-1):
			return None
		else:
			return infos


if __name__ == '__main__':
	'''Demo:获取IP信息'''
	provider = GeoIPProvider()
	results = provider.getIPInfos("202.203.208.8")
	#print 'city:%s\ncountry_name:%s\ncountry_code:%s\njingdu：%s\nweidu:%s' % (results['city'],results['country_name'],results['country_code'],results['longitude'],results['latitude'])
	print results

