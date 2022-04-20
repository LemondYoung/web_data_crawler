#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> douban_data
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:47
@Desc   ：
==================================================
"""

from utils.database.mysql import MySql
from settings import DOUBAN_DB_CONFIG

douban_db = MySql(**DOUBAN_DB_CONFIG)

def get_all_url(is_download=True, is_parse=True, limit=None, return_type='list'):
    sql = """
    select url from s_url_manager
    where 1=1
    """
    if is_download is False:
        sql += """ and is_download = 0"""
    if is_parse is False:
        sql += """ and is_parse = 0"""
    if limit:
        sql += """ limit {limit} """.format(limit=limit)
    data = douban_db.query(sql)
    if return_type == 'list':
        url_list = [item['url'] for item in data]
        return url_list
    else:
        return data
