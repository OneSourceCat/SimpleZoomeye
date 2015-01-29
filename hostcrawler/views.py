#coding=utf-8
import json,sys,requests,time,re,threading,os
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from hostcrawler.models import *
from django.template import Context,RequestContext
from django.core.paginator import Paginator
from elasticsearch import Elasticsearch
from safecat.settings import ATTACK_CLI_PATH
from libs.db.sqlhelper import DBHelper

'''主页面显示'''
def index(request):

	print request.user.has_perm("polls.use_attack")
	if request.user.is_authenticated():
		return render_to_response('active.html',{'user':request.user})
	else:
		return render_to_response('index.html',context_instance=RequestContext(request))

'''用户登录'''
def account_login(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	print "----%s %s-----" % (username,password)
	user = auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/active/')
	else:
		return render_to_response('index.html',{'login_err':'Wrong username or password'},context_instance=RequestContext(request))

'''
用户注册:使用的系统自带User对象(username,password,email)
权限控制：使用is_staff(是否有网站管理权限)和is_supperuser(是否有超级管理员权限)
使用攻击模块权限：user.has_perm("polls.use_attack")
'''
def account_register(request):
	#注册条件
	condition = request.POST.has_key('username') and request.POST.has_key('password') and request.POST.has_key('repassword') and request.POST.has_key('email')
	print request.POST
	if condition:
		#判断数据
		#两次密码不相同
		if request.POST['password'] != request.POST['repassword']:
			return render_to_response('register.html',
			{'err_pass_not_equal':'Please check your password'},
			context_instance=RequestContext(request))
		#用户名已经存在
		elif (User.objects.filter(username=request.POST['username'])) is None:
			print 'hello:%s' % request.POST['username']
			return render_to_response('register.html', 
			{'err_user_exists':'This Username has already used by others'},
			context_instance=RequestContext(request))
		#邮箱格式不正确
		elif str(request.POST['email']).count('@') == 0:
			return render_to_response('register.html',
			{'err_email_invalid':'Email invalid'},
			context_instance=RequestContext(request))
		#开始注册
		else:
			user = User(
					username=request.POST['username'],
					email=request.POST['email'],
				)
			user.set_password(request.POST['password'])
			user.save()
			return render_to_response('index.html',
				{'register_success_info':'Register Success! Please Login!'},
				context_instance=RequestContext(request))
	else:
		#表单不完整
		return render_to_response('register.html',
			context_instance=RequestContext(request))


'''用户退出'''
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')


'''中间页面'''
def active(request):
	return render_to_response('active.html',{'user':request.user})



'''语法解析功能'''
def queryParser(query):
	tmp = query.split(' ')
	print tmp
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
	return res_list


'''搜索主页面'''
def search(request):
	#仅对认证用户开放
	if request.user.is_authenticated():
		#查询字段
		start = time.time()
		if request.GET.has_key('q'):
			query = request.GET['q']
		else:
			return HttpResponseRedirect('/index/')
		pagenum = 1
		if request.GET.has_key('pageid'):
			pagenum = request.GET['pageid']
		
		#解析字符串  discuz country:"United States" ip:1.1.1.1
		res_list = queryParser(query)
		#print res_list
		#查询字符串
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
			}
		}

		print query_dsl


		es = Elasticsearch('127.0.0.1:9200')
		res = es.search(body=query_dsl,index="safecat",doc_type="hostcrawler",size=1000)

		#print res
		info_list = []
		print '--------------------'
		print res['hits']['total']
		print '--------------------'
		for host in res[u'hits']['hits']:
			obj = host['_source']
			info_list.append(obj)


		#分页代码
		p = Paginator(info_list,8)
		#控制显示5页
		if p.num_pages < 5:
			prange = range(1,p.num_pages+1)
		elif int(pagenum) in (1,2,3):
			prange = range(1,6)
		else:
			prange = range(int(pagenum)-2,int(pagenum)+2+1)
		page = p.page(pagenum)  #当前页
		end = time.time()
		cost = end - start
		cost  = "%.3f" % cost
		return render_to_response('search.html',
			{'info_list':info_list,'user':request.user,'p':p,'page':page,
			'query':query,'prange':prange,'info_list':info_list,'cost':cost},
			context_instance=RequestContext(request))

	#没有登录的用户转到登录页面
	else:
		return render_to_response('index.html')



'''攻击模块的实现'''
def attack_module(request):
	res = ()
	path = ''
	#如果用户已经登录
	if request.user.is_authenticated():
		#如果登录的用户没有权限
		if not request.user.has_perm("polls.use_attack"):
			print 'Can use attack_module'
			return render_to_response('attack.html',{'info':'Non-permission','user':request.user},context_instance=RequestContext(request))
		else:
			#如果登录用户有使用攻击模块的权限
			if not request.POST.has_key('cmd'):
				render_to_response('attack.html',{'user':request.user},context_instance=RequestContext(request))
			else:
				#执行命令
				db = DBHelper()
				cmd = request.POST['cmd']
				cmd = 'python %s %s' % (ATTACK_CLI_PATH,cmd) 
				print 'in attack_module:',cmd
				os.system(cmd)
				res = db.execute_dql_sql('safecat_jobs','select path,content from job_status order by id desc limit 1')
				print 'res======>',res
				if res:
					path = os.path.basename(res[0])
					path = "/static/reports/" + path
					res = str(res[1]).split(' ')
				res = [str(x).replace('\t',' ') for x in res]

			return render_to_response('attack.html',
				{'user':request.user,'results':res,'download_path':path},
				context_instance=RequestContext(request))
	else:
		#没有登录
		return render_to_response('index.html',context_instance=RequestContext(request))



def test(request):
	#仅对认证用户开放
	if request.user.is_authenticated():
		#查询字段
		start = time.time()
		if request.GET.has_key('q'):
			query = request.GET['q']
		else:
			return HttpResponseRedirect('/index/')
		pagenum = 1
		if request.GET.has_key('pageid'):
			pagenum = request.GET['pageid']
		
		#解析字符串  discuz country:"United States" ip:1.1.1.1
		res_list = queryParser(query)
		#print res_list
		#查询字符串
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
			}
		}

		print query_dsl


		es = Elasticsearch('127.0.0.1:9200')
		res = es.search(body=query_dsl,index="safecat",doc_type="hostcrawler",size=1000)

		print res
		info_list = []
		print '--------------------'
		print res['hits']['total']
		print '--------------------'
		for host in res[u'hits']['hits']:
			obj = host['_source']
			# obj = WebComponent(ip=item['ip'],domain=item['domain'],
			# serverinfo=item['serverinfo'],country=item['country'],city=item['city'],
			# flag=item['flag'],version=item['version'],http_response=item['http_response'])
			info_list.append(obj)


		#分页代码
		p = Paginator(info_list,8)
		#控制显示5页
		if p.num_pages < 5:
			prange = range(1,p.num_pages+1)
		elif int(pagenum) in (1,2,3):
			prange = range(1,6)
		else:
			prange = range(int(pagenum)-2,int(pagenum)+2+1)
		page = p.page(pagenum)  #当前页
		end = time.time()
		cost = end - start
		cost  = "%.3f" % cost
		return render_to_response('search.html',
			{'info_list':info_list,'user':request.user,'p':p,'page':page,
			'query':query,'prange':prange,'info_list':info_list,'cost':cost},
			context_instance=RequestContext(request))

	#没有登录的用户转到登录页面
	else:
		return render_to_response('index.html')
