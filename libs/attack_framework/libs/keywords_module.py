#coding=utf-8
import os
import sys
import time
import imp
from sqlhelper import DBHelper
from elasticsearch import Elasticsearch
from exploit_http import EXPHttp
from conf.safecat import *

#生成的报告名称
file_name = REPORT_FOLD + str(time.time()) + '.cat'

class KEYModule():
	def __init__(self,flag):
		self.es = Elasticsearch('127.0.0.1:9200')
		self.flag = flag
		self.file = open(file_name,'a')
		self.httptools = EXPHttp()
		
	'''载入相应模块的exp对象'''
	def loadExploit(self):
		expfile_list = []
		expobj_list = []
		path = "%s/exploit/%s" % (ROOT_PATH,self.flag)
		sys.path.append(path)
		print path,ROOT_PATH
		for x in os.walk(path):
			for y in x[2]:
				if str(y).endswith('pyc') or str(y).startswith('__init__'):
					continue
				expfile_list.append(str(y).replace('.py',''))
		for x in expfile_list:
			fp, pathname, description = imp.find_module(x)
			obj = imp.load_module(x, fp, pathname, description)
			expobj_list.append(obj.SafecatExploit())
		return expobj_list


	'''语法解析功能'''
	def queryParser(self,query):
		tmp = query.split(' ')
		meta = []
		query_dict = {}
		res_list = []
		for x in tmp:
			if x.count(':') == 0:
				res_list.append(x)
			else:
				x = x.replace('+',' ')
				meta = x.split(':')
				res_list.append({meta[0]:meta[1]})
		should_list = []
		must_list = []
		tmp = []
		for x in res_list:
			if str(x).count(':') == 0:
				tmp = [
					{'match':{'ip':x}},
					{'match':{'country':x}},
					{'match':{'city':x}},
					{'match':{'domain':x}},
					{'match':{'serverinfo':x}},
					{'match':{'flag':x}},
					{'match':{'http_response':x}}
				]
				should_list.extend(tmp)
					
			else:
				must_list.append({'match':x})

		query_dsl = {
			'query':{
				'bool':{
				    'should':should_list,
				    'must':must_list
				}
			},
			'_source':['domain']
		}

		return query_dsl

	'''根据用户搜索进行exp'''
	def scanByQuery(self,query):
		content = ''
		#数据库记录
		db = DBHelper()
		sql = "insert into job_status (status,path) values(%s,'%s')" % ('0',file_name)
		db.execute_ddl_sql('safecat_jobs',sql)

		#生成报告头
		self.exp_list = self.loadExploit()
		self.file.write('domain\t\t\tattack_results\n')
		query_dsl = self.queryParser(query)
		query_res = self.es.search(body=query_dsl,index='safecat',doc_type='hostcrawler',size=100000)
		domain_list = [ x['_source']['domain'] for x in query_res['hits']['hits'] ]
		for target in domain_list:
			target = self.httptools.get_standard_url(target)
			print '[+]TargetHOST:%s' % target
			for obj in self.exp_list:
				res = obj.exploit(target)
				if not res:
					record = '%s\t\t\tFailed\n' % target
					content += record
					print record
				else:
					record = '%s\t\t\t%s\n' % (target,res)
					content += record
					print record
				self.file.write(record)
		content = content.replace('\n',' ')
		sql = '''update job_status set status=%s,content='%s' where id=(select tmp.id from (select id from job_status order by id desc limit 1)tmp)''' % ('1',content)
		print sql
		db.execute_ddl_sql("safecat_jobs",sql)

		self.file.close()

	'''攻击一个域名'''
	def scanByDomain(self,domain):
		#数据库记录
		content = ''
		db = DBHelper()
		sql = "insert into job_status (status) values(%s)" % '0'
		db.execute_ddl_sql('safecat_jobs',sql)

		self.exp_list = self.loadExploit()
		self.file.write('domain\t\tattack_results')
		domain = self.httptools.get_standard_url(domain)
		for obj in self.exp_list:
			res = obj.exploit(domain)
			if not res:
				print '%s Exploit Failed:Unknown' % domain
				content += '%s\tExploit\tFailed:Unknown' % domain
			else:
				print 'Exploit Success:%s\t\t%s' % (x,str(res))
				content = '%sExploit\tSuccess:%s\t\t%s' % (domain,x,str(res))
		sql = '''update job_status set status=%s,content='%s' where id=(select tmp.id from (select id from job_status order by id desc limit 1)tmp)''' % ('1',content)
		print sql
		db.execute_ddl_sql("safecat_jobs",sql)

if __name__ == '__main__':
	# a = KEYModule('discuz')
	# print a.loadExploit()


	print STATIC_ROOT
