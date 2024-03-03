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
import random
from settings import db_map
from constants import *
from data_crawler.html_outputer import HtmlOutput


# 从数据库获取不同类型的url
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


def get_url_list(url_type, db_name=None, limit=None, url_status='add'):
    if not db_name:
        print('请指定db_name')
        return []
    sql = """
    select url from s_url_manager
    where url_type = '{url_type}'
    """.format(url_type=url_type)
    if url_status == 'add':
        sql += """ and url_status = 0 """
    if limit:
        sql += """ limit {limit} """.format(limit=limit)
    data = db_map.get(db_name).query(sql)
    return [item['url'] for item in data]


# url管理器
class UrlManager(object):

    def __init__(self, db_name):
        self.table_name = 's_url_manager'
        self.db_name = db_name

    # 获取url
    @staticmethod
    def get_all_url(url_type, style_code=None, is_download=None, is_parse=None):
        url_list = get_urls(url_type, style_code=style_code, return_type='map', type='add')
        return url_list

    # 添加url
    def add_url(self, url_data):
        """
        添加url
        :param url_data: list_dict
        :return:
        """
        if url_data is None:
            logging.error('url为空')
            return False
        elif isinstance(url_data, str):
            url_data = [{'url': url_data}]
        save_result = self.save_url(url_data=url_data, mode=STORE_DATA_REPLACE)
        return save_result

    # 更新url
    def update_url(self, url, result=True, msg=None):
        """ 更新url
        :param url:
        :param result: 成功或失败或未知，都要更新
        :param msg:
        :return:
        """
        if result is False:
            url_status = -1
        elif result is None:
            url_status = 0
        else:
            url_status = 1
        logging.info(f'更新 {url} 状态: {url_status}')
        save_result = self.save_url(url_data=[{'url': url, 'url_status': url_status, 'remark': msg}], mode=STORE_DATA_UPDATE)
        return save_result

    def save_url(self, url_data, mode):
        result, msg = HtmlOutput().save_table_data(db_name=self.db_name, table_name=self.table_name, records=url_data, mode=mode, update_conditions=['url'])
        return result


# 切分url列表
def split_urls(urls, strategy="random"):
        """
        切分url
        :param urls:
        :param strategy: 策略：random随机
        :return: list_dict，包含停顿时间、个数，新列表
        """
        new_urls = []
        fixed_num = 10
        if strategy == 'random':
            index = 1
            sub_new_urls = []
            random_num = random.randint(1, 5)
            for url in urls:
                sub_new_urls.append(url)
                if index == fixed_num + random_num:
                    new_urls.append({
                        'urls': sub_new_urls,
                        'count': len(sub_new_urls),
                        'sleep': random_num,
                    })
                    index = 1
                    sub_new_urls = []
                    random_num = random.randint(1, 5)
                    continue
                index += 1
            else:
                new_urls.append({
                        'urls': sub_new_urls,
                        'count': len(sub_new_urls),
                        'sleep': random_num,
                    })
        else:
            pass
        return new_urls


if __name__ == '__main__':
    dd = get_urls(url_type='img_url', return_type='list')
    print(dd)