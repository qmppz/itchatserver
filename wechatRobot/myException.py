# -*- coding: utf-8 -*-
# @Time  : 2017/03/29 14:54
# @Author   : RenjiaLu

import re
import time
import itchat, time
import requests
import random
import json
import sys
global outputfile
global strtm
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

strtm = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
outputfile = open("log_%s.txt"%strtm, "a+")
#异常处理
def myException(whichStep,log,e):
	global outputfile
	strtm = time.strftime('%Y_%m_%d__%H_%M_%S',time.localtime(time.time()))
	str = "###%s[Exception]:%s [Log]:%s [e]:%s \n"%(strtm,whichStep,log,e)
	print str
	try:
		outputfile.write(str)
		#sendtomyself
	except Exception as e:
		print e
