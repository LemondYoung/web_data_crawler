# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@desc: 
@author: yang li peng
@file: test3.py
@time: 2024/9/16
@info:
"""
import re

# 正则表达式解析中文名称
text_list = [
    'なあなあ',  # -> 哪啊哪啊神去村
    '瑞克和摸底 第一季 Rick and Morty 第一季',  # -> 瑞克和摸底 第一季
    '哪啊哪啊神去村 WOOD JOB！神去なあなあ日常',  # -> 哪啊哪啊神去村
    '鹿鼎记2：神龙教 鹿鼎記II 神龍教',  # -> 鹿鼎记2：神龙教
    '哈利·波特与死亡圣器(上) Harry Potter and the Deathly Hallows: Part 1',  # -> 哈利·波特与死亡圣器(上)
    '吉米·鸡毛逊毙了！马达翻身当主持 Jimmy Kimmel Sucks!',  # -> 吉米·鸡毛逊毙了！马达翻身当主持
    '每分钟120击 120 battements par minute',  # -> 每分钟120击
    '触不可及(美版) The Upside',  # -> 触不可及(美版)
    '瑞奇·热维斯现场单口喜剧第四弹 - 科学 Ricky Gervais: Live IV - Science',  # -> 瑞奇·热维斯现场单口喜剧第四弹
    '翻滾吧！蛋炒饭 翻滾吧！蛋炒飯',  # -> 翻滾吧！蛋炒饭
    '爱上查美乐 美樂。加油',  # -> 爱上查美乐
    '路易·C·K：臭不要脸 Louis C.K.: Shameless',  # -> 路易·C·K：臭不要脸
    '被嫌弃的松子的一生 嫌われ松子の一生',  # -> 被嫌弃的松子的一生
    '被嫌弃的松子N·M的一生 嫌われ松子の一生',  # -> 被嫌弃的松子N·M的一生
]
# 匹配规则：中文字符+数字、字母、特殊符号中文字符+空格+（第N季）
pattern = r'[^\s]*(?:[\u4e00-\u9fa5a-zA-Z\d!！?？@#$%^&*()_+\-={}\[\]\\|·~:：;；"\',，./<>《》【】“”‘’])+(?:\s*第(?:[一二三四五六七八九十百]+)季)?'
out_dict = {}
for text in text_list:
    matches = re.findall(pattern, text)
    if len(matches) > 0:
        movie_name = matches[0]  # 提取并去除多余的空格
        other_name = text[len(movie_name):].strip()  # 提取其余部分并去除空
    else:
        print('未匹配到中文名称，空过去')
        movie_name = None
        other_name = text
    out_dict[text] = [movie_name, other_name]

print(out_dict)