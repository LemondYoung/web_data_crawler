#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> url_manager
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:21
@Desc   ：
==================================================
"""
from data_sync.data_extract.douban_data import get_all_url
from data_sync.data_load.mysql_data_load import save_table_data
from data_parse.parse_tools.url_parse import split_douban_url

from constants import *

# url管理器
class UrlManager(object):

    def __init__(self):
        self.table_name = 's_url_manager'

    # 获取url
    def get_all_url(self, is_download=None, is_parse=None):
        url_list = get_all_url(return_type='list', is_download=is_download, is_parse=is_parse)
        return url_list

    # 添加url
    def add_url(self, url):
        split_result = split_douban_url(url)
        _ = {
            'url': split_result.get('url'),
            'url_type': split_result.get('url_type'),
            'is_download': 0,
            'is_parse': 0
        }
        dic = [_]
        save_result = self.save_url(url_dict=dic, mode=STORE_DATA_REPLACE)
        return save_result

    def update_url(self, url):
        split_result = split_douban_url(url)
        _ = {
            'url': split_result.get('url'),
            'url_type': split_result.get('url_type'),
            'is_download': 1,
            'is_parse': 1
        }
        dic = [_]
        save_result = self.save_url(url_dict=dic, mode=STORE_DATA_REPLACE)
        return save_result

    def save_url(self, url_dict, mode):
        result = save_table_data(table_name=self.table_name, records=url_dict, mode=mode)
        if not result:
            return False
        else:
            return True
