# -*- coding: utf-8 -*-
# @Time  : 2017/03/29 14:54
# @Author   : RenjiaLu

from myException import myException
import sqlite3
import re
import time
import itchat, time
import requests
import random
import json
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)
from classMsg import *

################################################################################
#创建表 msgdata splitword
def create_table(db_name):  
	conn = sqlite3.connect(db_name)  
	try:  
		create_tb_msgdata=''' 
		CREATE TABLE IF NOT EXISTS msgdata 
		(id INT PRIMARY KEY,
		msgtype TEXT,
		msgtext TEXT, 
		whosend TEXT, 
		sendtowhere TEXT,
		senddate TEXT
		); 
		'''  
		create_tb_splitword=''' 
		CREATE TABLE IF NOT EXISTS splitword 
		(id INT PRIMARY KEY,
		wordpos TEXT,
		theword TEXT, 
		fromwho TEXT, 
		sendtowhere TEXT,
		senddate TEXT
		); 
		'''  
		#主要就是上面的语句  
		conn.execute(create_tb_msgdata)  
		conn.execute(create_tb_splitword)  
	except Exception as e: 
		myException("STEP OF func:create_table","Create table failed db_name=[%s]"%db_name,e)
		return False  
	else:
		print 'success'

#执行 sqlsttmnt 语句
def executeSqlSttmnt(conn,sqlsttmnt):
	try:
		cursor = conn.execute(sqlsttmnt)
		conn.commit()
		return cursor
	except Exception as e:
		myException("STEP OF func:executeSqlSttmnt","sqlsttmnt=[%s]"%sqlsttmnt,e)
		return -1
	else:
		pass
	finally:
		pass

###############################################################################
