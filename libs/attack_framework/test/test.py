#coding=utf-8
import os`
import urllib
import urllib2
import requests
url = 'http://www.baidu.com'
data = {
	'q':'fhdsajk jfaskd,[]'
}
headers = {
	'User-agent':'xxxx'
}
# req = urllib2.Request(url)
# r = urllib2.urlopen(req)
# print r.geturl()

# data = urllib.urlencode(data)
# url = 'http://www.baidu.com/?q=FDASFAS+[]FASDF,'
# r = requests.get(url)
# print r.url

# url = 'http://zhalong.9i5c.com/forum.php'
# url = 'http://www.xxoo.com/'
# url = 'http://www.hejiong.com/bbs/forum.php'
# count = 0
# sort = []
# for x in url:
# 	if x == '/':
# 		sort.append(count)
# 	count += 1

# print sort
# # ret = url.find('/',len(url)-1)
# # print ret
# # print url[:ret+1]
# print url[:sort[-1]+1]

path = 'c:/test/1.txt'
print os.path.basename(path)
	