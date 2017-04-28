# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
#import matplotlib.pyplot as plt
from os import path
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import locale

def genWordCloud(dict_data,rootPath = path.dirname(__file__),imgName="ico1.png",saveFileName="wordcloud_init.png"):
	
	#设置语言
	locale.setlocale(locale.LC_ALL, 'chs')

	#字体文件路径
	fontPath = "msyh.ttc"

	#当前工程文件目录
	d = rootPath 

	# 设置背景图片
	alice_coloring = imread(path.join(d, imgName))

	#构建词云框架 并载入数据
	wc = WordCloud(font_path = fontPath,#字体
			background_color="white", #背景颜色
			max_words=10000,# 词云显示的最大词数
			mask=alice_coloring,#设置背景图片
			#stopwords=STOPWORDS.add("said"),
			width=900,
			height=600,
			scale=2.0,
			max_font_size=100, #字体最大值
			random_state=22).fit_words(dict_data)

	#载入 DICT 数据
	#wc.generate_from_frequencies(dict_data)

	#从背景图片生成颜色值
	image_colors = ImageColorGenerator(alice_coloring)

	# 以下代码显示图片
	# plt.imshow(wc)
	# plt.axis("off")
	#plt.show()

	#保存图片
	wc.to_file(path.join(d,saveFileName))
	pass
