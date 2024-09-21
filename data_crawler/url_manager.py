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


def get_url(url=None, db_name=None, ):
    sql = f"""
    select url, url_type, url_status from s_url_manager
    where 1=1
    """
    sql += f""" and url = '{url}' """ if url else ''
    data = db_map.get(db_name).query(sql)
    return data


# 从数据库获取不同类型的url
def get_urls(url_type, db_name=None, style_code=None, limit=None, url_status='all'):
    """ 从url管理器获取url
    :param url_type: url的类型，如book、movie、music
    :param db_name: 数据库名称
    :param style_code:  分类代码
    :param limit:  限制数量
    :param url_status:  状态：all全部，success成功，fail失败，unknown未知, init初始化
    :return:
    """
    sql = f"""
    select url_type, url from s_url_manager
    where url_type = '{url_type}'
    """
    if url_status == 'success':
        sql += """ and url_status = 1 """
    elif url_status == 'fail':
        sql += """ and url_status = -1 """
    elif url_status == 'unknown':
        sql += """ and url_status in (0, 2) """
    elif url_status == 'init':
        sql += """ and url_status = 0 """
    sql += f""" and style_code = '{style_code}' """ if style_code else ''
    sql += f""" limit {limit} """ if limit else ''
    data = db_map.get(db_name).query(sql)
    return data


def get_url_map(url_type, db_name=None, style_code=None, url_status='all'):
    """
    :param url_status:  状态：all全部，success成功，fail失败，unknown未知, init初始化
    """
    url_data = get_urls(url_type, db_name=db_name, style_code=style_code, url_status=url_status)
    url_map = {item['url_type']: [] for item in url_data}
    for item in url_data:
        url_map[item['url_type']].append(item['url'])
    return url_map


def get_url_list(url_type, db_name=None, style_code=None, url_status='all'):
    """
    :param url_status:  状态：all全部，success成功，fail失败，unknown未知, init初始化
    """
    url_data = get_urls(url_type, db_name=db_name, style_code=style_code, url_status=url_status)
    return [item['url'] for item in url_data]


# url管理器
class UrlManager(object):

    def __init__(self, db_name):
        self.table_name = 's_url_manager'
        self.db_name = db_name

    def check_url(self, url):
        url_data = get_url(url=url, db_name=self.db_name)
        if not url_data:
            return None  # url不存在
        elif len(url_data) == 1 and url_data[0]['url_status'] == 0:
            return None  # 初始化状态
        elif len(url_data) == 1 and url_data[0]['url_status'] == 2:
            return None  # 未知状态
        elif len(url_data) == 1 and url_data[0]['url_status'] == 1:
            return True  # 成功
        elif len(url_data) == 1 and url_data[0]['url_status'] == -1:
            return False  # 失败

    # 获取url
    def get_all_url(self, url_type, style_code=None, is_download=None, is_parse=None):
        url_list = get_url_map(url_type, db_name=self.db_name, style_code=style_code)
        return url_list

    # 添加url
    def add_url(self, url_data, is_run_all=False):
        """
        添加url（只能一条，多了不行）
        :param url_data: list_dict
        :param is_run_all: 是否全部运行，否的话就先检查一下是不是已经解析过了，如果是，就不再添加了
        :return:
        """
        if url_data is None:
            logging.error('url为空')
            return False
        elif isinstance(url_data, str):
            url_data = {'url': url_data}
        elif isinstance(url_data, dict):  # 必须是list_dict格式，别的不好使
            pass
        if is_run_all is False:  # 检查一下是不是解析过了
            url_status = self.check_url(url_data['url'])
            if url_status is True:
                logging.info(f'该url已经成功解析过了: {url_data["url"]}')
                return None
        save_result = self.save_url(url_data=[url_data], mode=STORE_DATA_INSERT_UPDATE)
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
            url_status = 2
        elif result is True:
            url_status = 1
        else:
            url_status = 0
        logging.info(f'更新 {url} 状态: {url_status}')
        save_result = self.save_url(url_data=[{'url': url, 'url_status': url_status, 'remark': msg}], mode=STORE_DATA_UPDATE)
        return save_result

    def save_url(self, url_data, mode):
        """  保存许多url
        :param url_data:
        :param mode:
        :return:
        """
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
                    random_num = random.randint(5, 10)  # 随机停顿时间，多停顿一下，心急吃不了热豆腐
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
    dd = ''
    print(dd)