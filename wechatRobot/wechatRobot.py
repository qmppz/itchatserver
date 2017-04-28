# -*- coding: utf-8 -*-
# @Time  : 2017/03/29 14:54
# @Author   : RenjiaLu

import os
from os import path
#from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import locale

from genWordCloud import genWordCloud
from utils_parseString import *	
from utilssqlite import *
from myException import myException
import json
import re
import ConfigParser
import codecs
import itchat, time
import requests
import random
import json
import sys
from classMsg import *
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)


#全局变量
global myVersion
global db_name
global msgdatatable
global splitwordtable
myVersion = "beta2.01"
db_name = "wechatdata.db"
msgdatatable = "msgdata"
splitwordtable = "splitword"

global pauseNum
global robotNmbr
# global list_chatRoom
# global list_chatRoomValue
global list_randomReplyMsg
global dict_especialFriendName_Value #特别标识 朋友
global dict_chatroomName_Value#特别标识 群聊
# global outputfile
# global strtm
global SPLITWORD

global dict_group_model
global sendToWhere
global whoSend
global theMsg
global myName
global myValue

global dict_GroupAndMem #{群值: dict_MemAndListMsg[发言数]}
# global dict_MemAndListMsg # {NickName: list_classMsgText}
# global list_classMsgText #[classMsgText]

dict_group_model = {}
dict_GroupAndMem={}
sendToWhere=""
whoSend=""
theMsg=""
myName=""
myValue=""

SPLITWORD = "="
# strtm = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
# outputfile = open("log_%s.txt"%strtm, "a+")

dict_especialFriendName_Value = {}
dict_chatroomName_Value ={}
list_randomReplyMsg = ["额","e..","。。","[捂脸]","...","--"]
# list_chatRoom = []
# list_chatRoomValue =[]
robotNmbr = 1 #0 suiji
pauseNum = 0 #bu zanting
###################################函数模块##############################################
# #异常处理
# def myException(whichStep,log,e):
# 	global outputfile
# 	strtm = time.strftime('%Y_%m_%d__%H_%M_%S',time.localtime(time.time()))
# 	str = "###%s[Exception]:%s [Log]:%s [e]:%s \n"%(strtm,whichStep,log,e)
# 	print str
# 	try:
# 		outputfile.write(str)
# 		#sendtomyself
# 	except Exception as e:
# 		print e
#dict转json保存
def dict2json():
	# str_time = time.strftime('%Y_%m_%d',time.localtime(time.time()))
	# thefile = open(str_time+'.json','w+')
	# json.dump(dict_GroupAndMem,thefile,ensure_ascii=False)  
	# outfile.write('\n')
	# print 'dict2json success'
	return 1


#单人词云
def myCloud(v_p):
	global dict_chatroomName_Value,dict_Instructions_dict
	global SPLITWORD,db_name
	global sendToWhere,whoSend,SPLITWORD
	print 'myCloud'
	#def genWordCloud(dict_data,rootPath = path.dirname(__file__),imgName="ico1.jpg",saveFileName="wordcloud_init.png"):
	#构造 词-词频字典
	try:
		dict_mycloud={}
		conn = sqlite3.connect(db_name)
		sqlsttmnt_p = "SELECT theword,COUNT(theword) FROM %s WHERE sendtowhere LIKE \'%s\' AND fromwho LIKE \'%s\'  GROUP BY theword ;"\
			%(splitwordtable,sendToWhere,whoSend)
		cursor = executeSqlSttmnt(conn,sqlsttmnt_p)
		for row in cursor:
			print row[0],'-',row[1],
			dict_mycloud[row[0]] = row[1]

		#调用genWordCloud
		filename = "mycloud_%s.png"%(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())))
		genWordCloud(dict_mycloud,path.dirname(__file__),imgName="ico1.png",saveFileName=filename)
		#2.'@fil@文件地址'将会被识别为传送文件，'@img@图片地址'将会被识别为传送图片，'@vid@视频地址'将会被识别为小视频
		itchat.send(u'@%s\u2005 your wordcloud as follow'%whoSend,sendToWhere)
		itchat.send('@img@%s' %filename,sendToWhere)
		print 'genWordCloud-mycloud success'
		return 1
	except Exception as e:
		myException("STEP OF func:myCloud-genWordCloud and send img","genWordCloud or send img error; dict_mycloud=[%s]"%dict_mycloud,e)
	else:
		conn.close()
	finally:
		pass

#群聊词云
def ourCloud(v_p):
	global dict_chatroomName_Value,dict_Instructions_dict
	global SPLITWORD
	global sendToWhere,whoSend,SPLITWORD
	print 'ourCloud'
	#def genWordCloud(dict_data,rootPath = path.dirname(__file__),imgName="ico1.jpg",saveFileName="wordcloud_init.png"):
	#构造 词-词频字典
	try:
		dict_ourcloud={}
		conn = sqlite3.connect(db_name)
		sqlsttmnt_p = "SELECT theword,COUNT(theword) FROM %s WHERE sendtowhere LIKE \'%s\'  GROUP BY theword ;"\
			%(splitwordtable,sendToWhere)
		cursor = executeSqlSttmnt(conn,sqlsttmnt_p)
		for row in cursor:
			print row[0],'-',row[1],
			dict_ourcloud[row[0]] = row[1]

		#调用genWordCloud
		filename = "ourcloud_%s.png"%(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())))
		genWordCloud(dict_ourcloud,path.dirname(__file__),imgName="ico1.png",saveFileName=filename)
		#2.'@fil@文件地址'将会被识别为传送文件，'@img@图片地址'将会被识别为传送图片，'@vid@视频地址'将会被识别为小视频
		itchat.send(u'@%s\u2005 our wordcloud as follow'%whoSend,sendToWhere)
		itchat.send('@img@%s' %filename,sendToWhere)
		print 'genWordCloud-ourcloud success'
		return 1
	except Exception as e:
		myException("STEP OF func:ourCloud-genWordCloud and send img","genWordCloud or send img error; dict_ourcloud=[%s]"%dict_ourcloud,e)
	else:
		cnn.close()
	finally:
		pass

#指令对应函数:切换模式
def changeModel(v_p):	
	#CHANGEMODEL_[%d]
	global dict_chatroomName_Value,dict_Instructions_dict
	global SPLITWORD
	global sendToWhere,whoSend,SPLITWORD
	global robotNmbr,dict_group_model
	v = int(v_p)
	print '#changeModel from %s to %s'%(robotNmbr,v)
	dict_group_model[sendToWhere] = v
	robotNmbr=v
	return 1

#指令对应函数:暂停回复消息
def pauseOnce(v_p):
	#PAUSEONCE_[%d]
	global pauseNum
	#防止过大无法控制，过滤了指令
	if v_p > 9 :
		v_p = 9
	v = int(v_p)
	print '#pauseOnce %s times'%(v)
	pauseNum = v
	return 1

#管理员指令 增加或删除 【需要开启的'群聊名称-对应的值'】-管理员指令
def addOrdelDictNV(v_p):
	#ADDORDELDICTNV_[%s dictname]_ADD|OR_[%sname]
	global dict_chatroomName_Value,dict_Instructions_dict
	global SPLITWORD
	global sendToWhere,whoSend,SPLITWORD
	if whoSend != myValue:
		print 'No permission'
		return -1
	try:
		listtmp = v_p.split(SPLITWORD)
		dictname = listtmp[0]
		addOrdel = listtmp[1]
		Nametemp = listtmp[2]
		#删除数据项指令
		print dict_Instructions_dict.keys()
		if "DEL" == addOrdel and dictname in dict_Instructions_dict.keys():
			del (dict_Instructions_dict[dictname])[Nametemp]
			return 1
		#增加数据项指令
		list_dict_tmpvalue = []
		if "*dictCR" == dictname and "ADD" == addOrdel:
			list_dict_tmpvalue = (itchat.search_chatrooms(name=Nametemp))[0]

		elif "*dictEF" == dictname and "ADD" == addOrdel:
			list_dict_tmpvalue = itchat.search_friends(name=Nametemp)[0]	
		if 1 < len(list_dict_tmpvalue):
			valuetemp = list_dict_tmpvalue["UserName"]
			(dict_Instructions_dict[dictname])[Nametemp] = valuetemp
			return 1
		else:
			myException("STEP OF addOrdel","addOrdel [%s] is unknown,please check your instruction"%(addOrdel),"-")

	except Exception as e:
		myException("STEP OF func:addOrdelChatRoomNV()","v_p=%s"%(v_p),e)
	else:
		pass
	finally:
		pass

#管理员指令 显示当前配置信息
def showConfig(v_p):
	#SHOWCONFIG_[%d]
	global myName,dict_group_model,robotNmbr
	global myValue,myVersion,pauseNum
	global sendToWhere,whoSend,SPLITWORD
	#dict_group_model[sendToWhere] = robotNmbr if !(dict_group_model.has_key(sendToWhere)) else dict_group_model[sendToWhere]

	strtitle = "[%s]"%(time.strftime('%Y_%m_%d__%H_%M_%S',time.localtime(time.time())))
	strsplit = "[SPLITWORD is %s]"%SPLITWORD
	dictdata = {"[especialFriend]":",".join(dict_especialFriendName_Value.keys()),
			"[chatroomName]":",".join(dict_chatroomName_Value.keys())}
	themodel = '[model is %s]'%robotNmbr
	#sendtomyself
	itchat.send(" ",sendToWhere)
	itchat.send("----[Config %s]----"%myVersion,sendToWhere)
	itchat.send('%s\n%s\n%s\n[pause left is %s times]\n'%(strtitle,strsplit,themodel,pauseNum),sendToWhere)
	if whoSend != myValue:
		print 'No permission'
	else:
		itchat.send('[especialFriend]\n%s\n'%(dictdata["[especialFriend]"]),sendToWhere)
		itchat.send('[chatroomName]\n%s\n'%(dictdata["[chatroomName]"]),sendToWhere)

	itchat.send('---Config send over---',sendToWhere)
	itchat.send(" ",sendToWhere)

	return 1

#群聊指令-帮助信息
def helpInfo(v_p):
	global sendToWhere,whoSend,SPLITWORD,myVersion
	#sendToWhere 群聊的群的地址
	#whoSend 私聊的对方地址
	#v_p 1-私聊  2-群聊
	if whoSend != myValue:
		print 'No permission'
		strhelp = "---Help %s---\n[分隔符]\n%s\n\n[指令集]\n%s\n\n用法:[指令][分隔符][参数]\n示例:#CHANGEMODEL%s1 表示切换到模式1" \
			%(myVersion,SPLITWORD,"\n/help【帮助信息】\n/mycloud【我的词云】\n/ourcloud【群的词云】\n#CHANGEMODEL【切换模式1(图灵机器人)/2(小黄鸡机器人)/404(休眠)】\n#PAUSEONCE【暂停应答%d(次数)】\n#SHOWCONFIG【当前配置】\n",SPLITWORD)
	else:
		strhelp = "------Help------\n[分隔符]\n%s\n\n[指令集]\n%s\n\n用法:[指令][分隔符][参数]\n示例:#CHANGEMODEL%s1 表示切换到模式1" \
			%(SPLITWORD,"\n".join(dict_Instructions_func.keys()),SPLITWORD)
	itchat.send(u'@%s\u2005 \n%s'%(whoSend,strhelp),(sendToWhere if 2 == v_p else whoSend))
	return 1

#判断指令
def isIstructions(stri,isgroupchat):
	global SPLITWORD
	try:
		list_str = stri.split(SPLITWORD,1)
		print list_str
		stri = list_str[0]
		if dict_Instructions_func.has_key(stri):
			#没有带参数时 默认为 isgroupchat的值
			value_p = list_str[1] if 1<len(list_str) else isgroupchat
			if 1 == (dict_Instructions_func.get(stri)(value_p)):
				return 1
		return -1
	except Exception as e:
		myException("STEP OF func:isIstructions()","instruction [%s] parse error,please check your instruction"%stri,e)
		# print 'warning -zhilingshibie'
		# print e
		return -1
	else:
		pass
	finally:
		pass

#初始化
def init():
	global myValue,myName,db_name,dict_especialFriendName_Value,dict_chatroomName_Value
	global dict_chatroomName_Value,dict_Instructions_dict
	global SPLITWORD
	global sendToWhere,whoSend,SPLITWORD
	dict_myinfo = itchat.search_friends()
	# print dict_myinfo
	# print dict_myinfo["NickName"]
	# print dict_myinfo["UserNamef"]
	myName = dict_myinfo["NickName"]
	myValue = dict_myinfo["UserName"]
	#连接数据库建表
	#create_table(db_name)
	#获取配置信息
	cp = ConfigParser.SafeConfigParser() 
	with codecs.open('config.conf', 'r', encoding='utf-8') as f:
		cp.readfp(f)

	flg = 1#有效
	for x in xrange(1,0xFFFFFFF):
		Nametemp=""
		flg = 1#有效
		if cp.has_option('chatroomName', str(x)):
			try:
				#特别 群
				Nametemp =cp.get('chatroomName', str(x))
				list_dict_tmpvalue = (itchat.search_chatrooms(name=Nametemp))[0]
				if 1 < len(list_dict_tmpvalue):
					valuetemp = list_dict_tmpvalue["UserName"]
					(dict_Instructions_dict['*dictCR'])[Nametemp] = valuetemp
			except Exception as e:
				myException("STEP OF func:init","chatroomName get value error; Nametemp=[%s]"%Nametemp,e)
		else:
			flg -=1
		if cp.has_option('especialFriend',str(x)):
			try:
				#特别 人
				Nametemp =cp.get('especialFriend',str(x))
				list_dict_tmpvalue = itchat.search_friends(name=Nametemp)[0]
				if 1 < len(list_dict_tmpvalue):
					valuetemp = list_dict_tmpvalue["UserName"]
					(dict_Instructions_dict['*dictEF'])[Nametemp] = valuetemp
			except Exception as e:
				myException("STEP OF func:init","chatroomName get value error; Nametemp=[%s]"%Nametemp,e)
		else:
			flg -=1
		if -1 >= flg:
			#循环结束
			break
		print x,Nametemp


#储存群聊消息 sendtowhere-群聊地址   whosend-发送消息的人的nickname
def saveMsg(msgtype,whosend,sendtowhere,msgtext,sendtime,isgroupchat=2):
	#存入sqlite
		# msgtype TEXT,
		# msgtext TEXT, 
		# whosend TEXT, 
		# sendtowhere TEXT,
		# senddate TEXT

		# id INT PRIMARY KEY,
		# wordpos TEXT,
		# theword TEXT, 
		# fromwho TEXT, 
		# sendtowhere TEXT,
		# senddate TEXT
	global db_name
	sqlsttmnt=""
	returnvalue=""
	t_str=sendtime
	try:

		#t_str= time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))

		conn = sqlite3.connect(db_name)
		print "###"
		#存入 msgtext 表
		sqlsttmnt = "INSERT INTO %s VALUES (%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'); "%(msgdatatable,'NULL',msgtype,msgtext,whosend,sendtowhere,t_str)
		returnvalue =executeSqlSttmnt(conn,sqlsttmnt)

		#存入 splitword 表
		list_word = parseString(msgtext)
		for aword in list_word:
			sqlsttmnt = "INSERT INTO %s VALUES (%s,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'); "%(splitwordtable,'NULL',"pos",aword,whosend,sendtowhere,t_str)
			returnvalue =executeSqlSttmnt(conn,sqlsttmnt)
	except Exception as e:
		myException("STEP OF func:saveMsg","sqlsttmnt=[%s]"%sqlsttmnt,e)
	else:
		conn.close()
	finally:
		pass

	#sendtowhere -群 	whosend-发消息的人ActualNickName
	#储存 每个群中每个人发送的消息
	global dict_GroupAndMem
	cmsgtext =  classMsgText(msgtype,whosend,sendtowhere,msgtext,time)
	#群是否存在
	if sendtowhere not in dict_GroupAndMem.keys() :
		#群不存在 新增群、用户
			print 'no group no user'
			list_classMsgText = []
			dict_MemAndListMsg ={}

			list_classMsgText.append( cmsgtext )
			dict_MemAndListMsg[whosend] = list_classMsgText
			dict_GroupAndMem[sendtowhere] =dict_MemAndListMsg
	elif whosend not in dict_GroupAndMem[sendtowhere].keys():
		#群存在 成员不存在
			print 'have group no user'
			list_classMsgText = []

			list_classMsgText.append( cmsgtext )
			dict_GroupAndMem[sendtowhere][whosend]=list_classMsgText
	else:
		#群、成员都存在
		print 'have group have user'
		dict_GroupAndMem[sendtowhere][whosend].append(cmsgtext)

	print 'Group amount:',len(dict_GroupAndMem),'Member amount:',len(dict_GroupAndMem[sendtowhere]),\
				'Msg amount:',len(dict_GroupAndMem[sendtowhere][whosend])

	#dict2json() 
	print "--saveMsg success"	
	return 1

####################################################################################
#指令集-对应函数名
dict_Instructions_func = {'#CHANGEMODEL':changeModel,'#PAUSEONCE':pauseOnce,'#ADDORDELDICTNV':addOrdelDictNV,
				'#SHOWCONFIG':showConfig,
				'/help':helpInfo,
				'/mycloud':myCloud,
				'/ourcloud':ourCloud
				}
dict_Instructions_dict = {'*dictEF':dict_especialFriendName_Value,"*dictCR":dict_chatroomName_Value}



print ''
print 'Welcome using [ wechatRobot ] version: beta1.2 -only for learning-'
print '[Announce]: If you learn more about this program, search \'itchat\' on Github or contact me by wheee9527@163.com'
print ''
###################################开始程序###########################################
try:
	itchat.auto_login(enableCmdQR=True)
	#初始化
	init()


	#1 私聊 文字消息 类型
	@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
	def text_reply(msg):
		global pauseNum,whoSend,theMsg,sendToWhere,myValue
		print 'pauseNum is',pauseNum
		replyText = ""
		if 0 == pauseNum :
			whoSend = msg['FromUserName'] #whoSend to me
			theMsg = msg['Text']
			sendToWhere = msg['ToUserName'] #me

			if whoSend == myValue and 1 == isIstructions(msg['Text'],isgroupchat = 1):
				replyText = "-Instruction_Confirmed" 	
			else:
				replyText = talks_robot(msg['Text'])

			strtime = time.strftime('%Y_%m_%d__%H_%M_%S',time.localtime(time.time()))
			#itchat.send('%s: %s'%(msg['Type'], msg['Text']), msg['FromUserName'])
			itchat.send('%s'%( replyText ),msg['FromUserName'])
			print "-%s %s:	%s"%(strtime,msg['FromUserName'] ,msg['Text'])
			print "-%s M:	%s"%(strtime,replyText)
		else:
			pauseNum -= 1
			

	#2 私聊 非文字消息 类型
	@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
	def download_files(msg):
		global list_randomReplyMsg
		fileDir = '%s%s'%(msg['Type'], int(time.time()))
		msg['Text'](fileDir)

		msgtext = list_randomReplyMsg[random.randint(0,len(list_randomReplyMsg)-1)]
		print msg['FromUserName']
		replyText = talks_robot(msgtext)
		itchat.send('%s'%(replyText), msg['FromUserName'])
		#itchat.send('我收到了%s，但是我不能理解什么意思...%s received'%(msg['Type'],msg['Type']), msg['FromUserName'])
		#itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), msg['FromUserName'])

	@itchat.msg_register('Friends')
	def add_friend(msg):
		 itchat.add_friend(**msg['Text'])
		 itchat.get_contract()
		 itchat.send('Nice to meet you! 我是小薇机器人 输入#CHANGEMODEL=1可唤醒我', msg['RecommendInfo']['UserName'])

	#3 群聊 msg['FromUserName']是群的地址
	@itchat.msg_register(['Text','Picture', 'Recording', 'Attachment', 'Video'], isGroupChat = True)
	def text_reply(msg):
		global dict_chatroomName_Value,list_randomReplyMsg
		global sendToWhere,theMsg,whoSend
		global pauseNum
		print 'pauseNum is',pauseNum
		replyText = ""
		if 0 == pauseNum :
			#member NickName
			whoSend = msg['ActualNickName']
			#msg text
			theMsg = msg['Content']
			#group Value
			sendToWhere = msg['FromUserName']
			#print '#text_reply'
			print sendToWhere #群聊的地址
			#if sendToWhere in dict_chatroomName_Value.values():
			msgtext=""
			if 'Text' == msg['Type']:

				if 1 == isIstructions(msg['Text'],isgroupchat = 2):
					replyText = "-Instruction_Confirmed" 
					itchat.send(u'@%s\u2005 \n%s'%(whoSend,replyText), sendToWhere)
					print replyText
					return 1	
				else:
					#这条群聊消息不是 指令；继续完成【获取相应消息】【储存当前消息】操作
					msgtext = theMsg
					#储存
					strtime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
					try:

						saveMsg("Text",whoSend,sendToWhere,msgtext,strtime,1)
					except Exception as e:
						myException("STEP OF func:saveMsg","saveMsg failed msgtext[%s]"%msgtext,e)
					else:
						pass
					finally:
						pass

					replyText = talks_robot(theMsg)

			else:
				pass
				#replyText = list_randomReplyMsg[random.randint(0,len(list_randomReplyMsg)-1)]

			#itchat.send(u'@%s\u2005I received: %s'%(whoSend, theMsg), sendToWhere)
			print sendToWhere
			#replyText = talks_robot(msgtext)
			itchat.send('%s'%(replyText), sendToWhere)
			#itchat.send(u'@%s\u2005I received: %s'%(whoSend, theMsg), sendToWhere)
			#else:
			#	print '-PingBi'
		else:
			pauseNum -= 1

	#图灵机器人
	def talks_robot(info = '你叫什么名字'):
		global robotNmbr,dict_group_model
		global sendToWhere,whoSend,SPLITWORD
		n=404
		try:
			#通过群聊名称值 得到模式值
			n=dict_group_model[sendToWhere]
		except Exception as e:
			dict_group_model[sendToWhere] = n
			myException("STEP OF func:talks_robot","get robotNmbr error",e)

		if 0 == n:
			#0模式 随机选择api
			#suiji
			n=random.randint(1,3)

		if n == 1:
			#图灵机器人
			api_url = 'http://www.tuling123.com/openapi/api'
			apikey = 'APIKey'
			data = {'key': '3869ad1b82cc41ffa4757e7799c88609',
						'info': info}
			req = requests.post(api_url, data=data).text
			s = requests.session()
  			s.keep_alive = False
			replys = json.loads(req)['text']
			return replys
		elif n == 2:
			#小黄鸡机器人
			#QQ:	b026dea2-f0a8-47a3-90f2-aba9be93c219
			#163key 	b4461336-b04e-4e9a-9d3a-33328a81e0ed
			api_url = 'http://sandbox.api.simsimi.com/request.p?'
			key ="b026dea2-f0a8-47a3-90f2-aba9be93c219"
			lc = "zh"
			ft = "0.0"
			text = info
			api_url = 'http://sandbox.api.simsimi.com/request.p?key=%s&lc=%s&ft=%s&text=%s'%( \
						key,lc,ft,text)
			req = requests.get(api_url).text
			s = requests.session()
  			s.keep_alive = False
			replys = json.loads(req)['response']
			return replys
		elif n == 3:
			#微软小冰
			api_url = 'https://westus.api.cognitive.microsoft.com/qnamaker/v1.0'
			apikey = 'APIKey'
			headers = {'Host': 'https://westus.api.cognitive.microsoft.com/qnamaker/v1.0','Ocp-Apim-Subscription-Key':'<Your Subscription key>',\
				'Content-Type': 'application/json','Cache-Control': 'no-cache'}
			data = {'question': info}
			req = requests.post(api_url, data=data).text
			print req
			s = requests.session()
  			s.keep_alive = False
			replys = json.loads(req)['text']
			return replys
		elif n == 404:
			#跳过回答
			raise Exception
			api_url = 'https://westus.api.cognitive.microsoft.com/qnamaker/v1.0'
			apikey = 'APIKey'
			headers = {'Host': 'https://westus.api.cognitive.microsoft.com/qnamaker/v1.0','Ocp-Apim-Subscription-Key':'<Your Subscription key>',\
				'Content-Type': 'application/json','Cache-Control': 'no-cache'}
			data = {'question': info}
			req = requests.post(api_url, data=data,timeout=1).text
			print req
			s = requests.session()
  			s.keep_alive = False
			replys = json.loads(req)['text']
			return replys

	itchat.run()
except Exception as e:
	myException("STEP OF mainprocess","main",e)
	# print 'warning -mainprocess'
	# print e
else:
	pass
finally:
	a = input("PAUSE")
