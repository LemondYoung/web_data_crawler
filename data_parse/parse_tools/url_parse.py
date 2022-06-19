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


# 分割字符串
def split_url(url):
    """
    :param url:
    :return:
    """
    url_all = urllib.parse.urlparse(url)
    url_path = os.path.normpath(url_all.path).split(os.sep)[1:]
    url_dict = {
        'scheme': url_all.scheme,  #
        'hostname': url_all.hostname,  #
        'port': url_all.port,  #
        'path': url_path,  #
        'query': url_all.query,  #
    }
    return url_dict


# 分割豆瓣url
def split_douban_url(url):
    url_dict = split_url(url)
    url_type_value = url_dict['path'][1]
    if len(url_dict['path']) == 2:  # 二级
        if url_dict['path'][0] == 'subject':
            url_type = 'movie'
        elif url_dict['path'][0] == 'people':
            url_type = 'user'
        else:
            url_type = 'other'
    elif len(url_dict['path']) == 3:  # 二级
        if url_dict['path'][0] == 'subject' and url_dict['path'][2] == 'comments':
            url_type = 'movie_comment'
        elif url_dict['path'][0] == 'people' and url_dict['path'][2] == 'collect':
            url_type = 'user_movie'
        else:
            url_type = 'other'
    else:
        url_type = 'other'
    split_result = {
        'url': url,
        'url_type': url_type,
        'url_type_value': url_type_value,
    }
    return split_result




if __name__ == '__main__':
    url_list = [
        'https://www.nbfox.com/academic-art/',
    ]
    for url in url_list:
        split_url(url)

