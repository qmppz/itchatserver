# -*- coding: utf-8 -*-
# @Time  : 2017/03/22 15:54
# @Author   : RenjiaLu

from myException import myException

import sys
reload(sys)
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)
import jieba
import jieba.posseg  

testtemp = jieba.posseg.cut("测试文字-为了初始化jieba")
#jieba分词分析数据
def parseString(string):
	"""parse"""
	list_word = []
	seg_list = []
	try:
		seg_list = jieba.posseg.cut(string)
	except Exception as e:
		myException("STEP OF func:parseString","string:%s"%(string),e)
		return 
	else:
		"""第一次分词成功"""
		for a_seg in seg_list:
			if 1 >= len(a_seg.word):
				continue
			else:
				list_word.append(a_seg.word)
		print list_word
		return list_word

			
