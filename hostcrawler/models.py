#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

'''Web组件模型'''
class WebComponent(models.Model):
	ip = models.IPAddressField()
	domain = models.CharField(max_length=80)
	serverinfo = models.TextField(null=True)
	country = models.CharField(max_length=30,null=True)
	city = models.CharField(max_length=30,null=True)
	flag = models.CharField(max_length=10)
	version = models.CharField(max_length=30,null=True)
	http_response = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
















