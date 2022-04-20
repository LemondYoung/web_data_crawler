#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> html_parser
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:21
@Desc   ：
==================================================
"""


class Parser(object):

    def __init__(self):
        self.target_url = 'https://movie.douban.com/'
        self.cur_url = None
        self.table_name = None

    def parse_data(self, html, url=None):
        pass

    def transform_data(self, data_dict):
        url_data = data_dict.get('s_url_manager').get('data')
        if url_data:
            for item in url_data:
                item['data_source'] = None
                item['style_code'] = self.style
        return data_dict

    def run_parser(self, html, url, **kwargs):  # 从接收下载的html开始
        self.style = kwargs['style']
        # 解析数据（结果数据 + url数据）
        data = self.parse_data(html, url)

        data_dict = self.transform_data(data)

        return data_dict