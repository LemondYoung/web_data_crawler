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
import logging

from settings import db_map
from constants import *
from data_crawler.html_outputer import HtmlOutput


# 获取不同类型的url
def get_urls(url_type, style_code=None, limit=None, return_type='map', type='add'):
    sql = """
    select url_type, url from s_url_manager
    where url_type = '{url_type}'
    """.format(url_type=url_type)
    if type == 'add':
        sql += """ and url_status = 0 """
    if style_code:
        sql += """ and style_code = '{style_code}' """.format(style_code=style_code)
    if limit:
        sql += """ limit {limit} """.format(limit=limit)
    data = db_map.get('weibo_data').query(sql)
    if return_type == 'map':
        data_map = {}
        for item in data:
            if item['url_type'] not in data_map:
                data_map[item['url_type']] = [item['url']]
            else:
                data_map[item['url_type']].append(item['url'])
        return data_map
    elif return_type == 'list':
        return [item['url'] for item in data]
    else:
        return data


class UrlManager(object):

    def __init__(self):
        self.table_name = 's_url_manager'

    # 获取url
    @staticmethod
    def get_all_url(url_type, style_code=None, is_download=None, is_parse=None):
        url_list = get_urls(url_type, style_code=style_code, return_type='map', type='add')
        return url_list

    # 添加url
    def add_url(self, url_data):
        if url_data is None:
            logging.error('url为空')
            return False
        save_result = self.save_url(url_data=url_data, mode=STORE_DATA_REPLACE)
        return save_result

    # 更新url
    def update_url(self, url, result=True):
        """
        :param url:
        :param result: 两种状态，成功或失败，都要更新
        :return:
        """
        logging.info('更新 %s 状态', url)
        if result:
            url_data = [{'url': url, 'url_status': 1}]
        else:
            url_data = [{'url': url, 'url_status': -1}]  # 失败
        save_result = self.save_url(url_data=url_data, mode=STORE_DATA_UPDATE)
        return save_result

    def save_url(self, url_data, mode):
        result, msg = HtmlOutput().save_table_data(table_name=self.table_name, records=url_data, mode=mode)
        return result


if __name__ == '__main__':
    dd = get_urls(url_type='img_url', return_type='list')
    print(dd)