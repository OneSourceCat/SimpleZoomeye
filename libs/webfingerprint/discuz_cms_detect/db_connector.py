#coding=utf-8
import os
import sys
sys.path.append("E:/School_of_software/information_security/holiday-learning/python/django/safecat/")
os.environ['DJANGO_SETTINGS_MODULE'] = "safecat.settings"
from hostcrawler.models import *
from libs.GeoIP.geoipprovider import GeoIPProvider
