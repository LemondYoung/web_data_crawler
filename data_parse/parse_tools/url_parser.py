#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> url_parse
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/19 16:05
@Desc   ：
==================================================
"""
import os
import urllib
from urllib import parse


# 分割url
def split_url(url):
    """
    传入一个url，解析出url的构成（协议、域名、端口、路径、查询字符串）
    :param url:
    :return: 包含域名、端口、地址和
    """
    url_all = urllib.parse.urlparse(url)
    url_path = os.path.normpath(url_all.path).split(os.sep)[1:]  # 路径转为列表
    url_dict = {
        'scheme': url_all.scheme,  #
        'hostname': url_all.hostname,  #
        'port': url_all.port,  #
        'path': url_path,  #
        'query': url_all.query,  #
    }
    return url_dict


# 解析豆瓣url
def split_douban_url(url):
    """
    解析豆瓣url，其中二级url有movie和people类，三级url有movie_comment、user_movie和unknown
    通过判断是哪个类型，并得到类型对应的结果值
    :param url:
    :return: 包含url、url类型、url类型值的dict
    """
    url_dict = split_url(url)
    url_path = url_dict['path']
    remark = None
    if len(url_path) == 1:  # 一级
        url_type_value = None
        if url_path[0] == 'top250':
            url_type = 'top250'
        elif url_path[0] == 'subject_search':  # 没有对应的独立条目，会进入豆瓣搜索
            url_type = 'unknown'
            remark = '未知人物，搜索页面'
        else:
            url_type = 'unknown'
    elif len(url_path) == 2:  # 二级
        url_type_value = url_path[1]  # 通常第二个值就是类型对应的类型值
        if url_path[0] == 'subject':
            url_type = 'movie'
        elif url_path[0] == 'people':
            url_type = 'user'
        elif url_path[0] == 'personage':
            url_type = 'movie_personage'
        else:
            url_type = 'unknown'
    elif len(url_path) == 3:  # 三级
        url_type_value = url_path[1]  # 通常第二个值就是类型对应的类型值
        if url_path[0] == 'subject' and url_path[2] == 'comments':
            url_type = 'movie_comment'
        elif url_path[0] == 'people' and url_path[2] == 'collect':
            url_type = 'user_movie'
        else:
            url_type = 'unknown'
    elif len(url_path) > 3:  # 四级以上，特定情况
        if url_path[3] == 'movie' and url_path[4] == 'recommend':
            url_type, url_type_value = 'movie_recommend', None
        else:
            url_type, url_type_value = 'unknown', None
    else:
        url_type, url_type_value = 'unknown', None
    split_result = {
        'url': url,
        'url_type': url_type,
        'url_type_value': url_type_value,
    }
    if remark:
        split_result['remark'] = remark
    return split_result




if __name__ == '__main__':
    url_list = [
        # 'https://www.nbfox.com/academic-art/',
        'https://movie.douban.com/people/Lion1874/collect?start=0&sort=time&rating=all&filter=all'
    ]
    for url in url_list:
        split_douban_url(url)

