# -*- coding: utf-8 -*-
# @Time  : 2017/04/19 12:54
# @Author   : RenjiaLu

from os import path
from time import ctime,sleep
from itchat.content import *
import ConfigParser
import itchat
import sys
import threading
import locale
import time
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

################################################全局变量
global G_UserNameValue
global threads
global splitstr
global parameter
global picDir
global outputfile
global strtm
#主线程 实例
global mainInstance
#global value
# 步骤的提示语
global  dict_stepinfo
# 启动脚本前的提示语
global helpinfo
# 客户列表
global list_customer
# 用户数量id
global cnt
# 客户线程
global client_list

mutex = threading.Lock()
picDir = 'qr_test.png'
G_UserNameValue =None
mainInstance = itchat.new_instance()
threads = []
splitstr='_'
parameter='[parameter]'
helpinfo=''
dict_stepinfo = {}
list_customer = []
cnt = 0
client_list = []
strtm = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
outputfile = open("log/log_%s.txt"%strtm, "a+")

################################################类
#客户线程类
class itchat_client (threading.Thread):
	#初始化函数
	def __init__(self, threadID, name,UserNameValue,friendsnum=100):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.UserNameValue = UserNameValue
		self.friendsnum = friendsnum

		self.picDir = 'qr/%s.png'%(UserNameValue.replace('@','qr')[0:7])
		self.step = 0 #0-初始化   1-完成 向客户发送二维码  
		self.newInstance = itchat.new_instance()

	#qrCallBack 函数
	def qrsendtouser(self,uuid, status, qrcode):
		global mainInstance
		strtm = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
		print 'qrsendtouser'
		with open(self.picDir, 'wb') as f:
			f.write(qrcode)
		print 'write success'
		if self.step < 1:
			if mutex.acquire():
				#print "Starting " + self.name
				print 'c send QR G_UserNameValue=',self.UserNameValue
				mainInstance.send('@img@%s' %(self.picDir),self.UserNameValue)
				mainInstance.send('记得是一个手机扫另一个手机才有效哦~',self.UserNameValue)
				print 'c send QR end'
				self.step = 1
				mutex.release()
			else:
				print 'mutex error'
			print 'send success'

	#run 函数
	def run(self):
		global mainInstance
		print ''
		print 'Welcome using [ wechatRobot ] version: beta1.2 -only for learning-'
		print '[Announce]: If you learn more about this program, search \'itchat\' on Github or contact me by wheee9527@163.com'
		print ''
		# ###################################开始程序###########################################
		try:

			self.newInstance.auto_login(picDir=self.picDir,qrCallback=self.qrsendtouser)
			list_dict_friends = self.newInstance.get_friends()
			# print type(list_dict_friends),list_dict_friends[0]
			# print list_dict_friends[0]['UserName']
			# print ''
			friendsnum = len(list_dict_friends)
			i=0
			for x in xrange(0,friendsnum):
				NickName = list_dict_friends[x]['NickName']
				UserNameValue = list_dict_friends[x]['UserName']
				self.newInstance.send('@img@qr/turing.png',UserNameValue)
				time.sleep(0.2) 
				print x,'OK'
				i+=1

			# @self.newInstance.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
			# def text_reply(msg):
			# 	self.newInstance.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

			#self.newInstance.run()
			if mutex.acquire():
				print 'c thread end G_UserNameValue=',self.UserNameValue
				mainInstance.send('完成!共检测【%d】个好友'%i,self.UserNameValue)
				print 'c thread end '
				self.step = 1
				mutex.release()
			else:
				print 'thread end mutex error'

		except Exception as e:
			myException("STEP OF startdelete mainprocess","startdelete",e)
		else:
			pass
		print 'thread end'

# 没有下单的客户信息 Customer类
class Customer(object):
	"""docstring for customer"""
	def __init__(self,nickname,namevalue,friendsnum,step):
		global cnt
		self.id = cnt
		self.nickname = nickname
		self.namevalue = namevalue
		self.friendsnum = friendsnum
		self.step = step
		self.shouldpay = 1.0
		cnt += 1

################################################公共函数
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
# 初始化
def init():
	global helpinfo,dict_stepinfo
	cp = ConfigParser.SafeConfigParser()
	cp.read('config.conf')
	helpinfo = cp.get('helpinfo','main')
	dict_stepinfo[0] = cp.get('step','0')
	dict_stepinfo[1] = cp.get('step','1')
	dict_stepinfo[2] = cp.get('step','2')
	dict_stepinfo[3] = cp.get('step','3')	
	dict_stepinfo[4] = cp.get('step','4')


# 获得对应的回复信息
def getreply(msgstr,who):
	global list_customer,splitstr, parameter,client_list,mainInstance,G_UserNameValue
	thiscustomer=''
	#获得这个类
	try:
		tembool=0 #此用户 没有记录过
		for x in xrange(0,len(list_customer)):
			if list_customer[x].namevalue == who :
				thiscustomer = list_customer[x]
				tembool = 1 #被记录过
				break
		if tembool == 0:
			#新增用户
			thiscustomer = Customer('null',who,friendsnum=100,step=0)
			list_customer.append(thiscustomer)
	except Exception as e:
		#新增用户
		thiscustomer = Customer('null',who,friendsnum=100,step=0)
		list_customer.append(thiscustomer)
	else:
		pass
	# 0 0= 在的亲 [呲牙] 
	print '#',thiscustomer.step
	if thiscustomer.step == 0 :
		thiscustomer.step = 1
		return dict_stepinfo[0]
	# 1=请问您的好友数量多少呢？ [呲牙]
	elif thiscustomer.step == 1 :
		thiscustomer.step = 2
		return dict_stepinfo[1]
	# 2=您需要测试的好友数为[parameter],向我转账[parameter]元立刻开始测试[爱心]
	elif thiscustomer.step == 2 :
		print msgstr
		try:
			num = int(msgstr)
			if num >0 and num < 9999 :
				money = num/200
				if money == 0:
					money = 1
				elif money > 2:
					money = money + 2

				returnvalue =  dict_stepinfo[2].replace(parameter,msgstr,1).replace(parameter,str(money))
				thiscustomer.friendsnum = num
				thiscustomer.shouldpay = float(money)
				thiscustomer.step = 3
				return returnvalue
			else:
				return '发给我 你的好友数量哦~'
		except Exception as e:
			myException("STEP OF get num of friends","getreply msgstr=%s"%msgstr,e)
			return '发给我 你的好友数量哦~'
		else:
			pass

	# 3=等待付款中哦[呲牙] 转账后立即开始
	elif thiscustomer.step == 3 :
		return dict_stepinfo[3]
	#测试中，请稍等[呲牙]
	elif thiscustomer.step == 4 :
		return dict_stepinfo[4]
	elif thiscustomer.step == 2017 :
		try:
			if int(msgstr) == 1:
				#指令确认 启动脚本
				# print 'm send test1 '
				# mainInstance.send('%s' %('m robot5.jpg'),thiscustomer.namevalue)
				# mainInstance.send('@img@%s' %('robot5.jpg'),thiscustomer.namevalue)
				# print 'm send test1 end'

				G_UserNameValue = thiscustomer.namevalue
				# newclient = itchat_client(1,'client_1', 1,thiscustomer.namevalue,thiscustomer.friendsnum)
				# startrun()
				# client_list.append(newthread)

				newthread = itchat_client(1,'client_thread',thiscustomer.namevalue,thiscustomer.friendsnum)
				newthread.start()
				client_list.append(newthread)
				thiscustomer.step=0
				return '生成二维码中，请稍等...'
		except Exception as e:
			myException("STEP OF confirm  start thread","last step == 2017  msgstr =%s"%msgstr,e)
			return '等待您回复【1】哦~'
		return '等待您回复【1】哦~'

################################################主线程代码
try:
	#初始化
	init()
	#启动登陆程序
	#mainInstance = itchat.new_instance()
	mainInstance.auto_login()
	#itchat.auto_login()
	# print 'create group'
	# memberList = mainInstance.get_friends()[1:]
	# print memberList

	# chatroomUserName = mainInstance.create_chatroom(memberList, 'testgroup')
	# for x in xrange(1,len(memberList)):
	# 	print get_friend_status(memberList[x])
	# print 'create group over'

	# 监听转账信息 NOTE
	@mainInstance.msg_register([NOTE])
	def text_reply(msg):
		global list_customer,splitstr, parameter,helpinfo,mainInstance

		print 'msg_register(NOTE) ',msg['Text']
		mainInstance.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
		if  msg['Text'].find('转账') > 0:
			try:
				#匹配用户
				thiscustomer=''
				who = msg['FromUserName']
				money = float(msg['Text'].split("转账")[-1].split('元')[0])
				print money
				#获得这个类

				tembool=0 #此用户 没有记录过
				for x in xrange(0,len(list_customer)):
					if list_customer[x].namevalue == who and list_customer[x].shouldpay <= money:
						thiscustomer = list_customer[x]
						tembool = 1 #被记录过
						break
				if tembool == 1:
					#运行清理脚本 
					#发送提示信息
					thiscustomer.step = 2017
					mainInstance.send('%s' % (helpinfo), msg['FromUserName'])
				else:
					#此用户 没有记录过
					mainInstance.send('%s: %s' % ('多谢您的捐赠！',msg['Text']), msg['FromUserName'])

			except Exception as e:
				myException("STEP OF NOTE","get a note msg msgtext=%s"%msg['Text'],e)
				mainInstance.send('%s: %s' % ('操作异常，请联系人类管理员！',msg['Text']), msg['FromUserName'])
			else:
				pass

	# 回复文字信息 指导用户下单
	@mainInstance.msg_register([TEXT])
	def text_reply(msg):
		global mainInstance
		print 'msg_register(TEXT) ',msg['Text']
		replystr = getreply(msg['Text'],msg['FromUserName'])
		mainInstance.send(replystr,msg['FromUserName'])
		# if msg['Text'].find(u"朋友验证") < 0:
		# 	mainInstance.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

	# 收到好友邀请自动添加好友
	@mainInstance.msg_register([FRIENDS])
	def add_friend(msg):
		global list_customer,mainInstance

		print 'msg_register(FRIENDS)'
		mainInstance.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
		mainInstance.send_msg(u'您好，我是小薇机器人', msg['RecommendInfo']['UserName'])

		#新建一个账户信息
		newcustomer = Customer('null',msg['FromUserName'],friendsnum=100,step=0)
		list_customer.append(newcustomer)


	mainInstance.run()
except Exception as e:
	myException("STEP OF mainprocess","main",e)
	outputfile.close()
else:
	pass
finally:
	pass

print 'THE END'
