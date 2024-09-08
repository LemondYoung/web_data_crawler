#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_Parser -> douban_Parser
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/16 23:38
@Desc   ：
==================================================
"""
import json
import logging, datetime
import urllib
from urllib import parse

from lxml import etree
import os
import requests
from utils.trading_calendar import today
from constants import *
from data_crawler.html_downloader import HtmlDownloader
from data_parse.parse_tools.date_parse import standardize_date
from data_parse.parse_tools.url_parse import split_douban_url, split_url
from data_sync.data_load.mysql_data_load import save_table_data
from utils.class_tool.register_class import ZhihuParserRegister

# 获取解析器
zhihu_parser_map = ZhihuParserRegister()


class ZhihuParser(object):

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
        }
        self.cur_url = None
        self.table_name = None
        self.target_db = 'zhihu_data'
        self.save_mode = STORE_DATA_REPLACE

    def parse_data(self, html):
        pass

    def transform_data(self, data_dict):
        return data_dict

    def save_data(self, data_dict):
        result, result_data = save_table_data(self.table_name, records=data_dict, db_name=self.target_db, mode=self.save_mode)
        if result is False or result is None:
            _ = {'length': len(data_dict), 'result_length': None, 'result_data': result_data}
            return [False, _]
        else:
            logging.info('计划执行数据量%s，已执行数据量为%s', len(data_dict), result)
            _ = {'length': len(data_dict), 'result_length': result, 'result_data': result_data}
            return [True, _]

    def run_parser(self, html):
        data = self.parse_data(html)

        # 保存数据
        data_dict = data['data_dict']
        parser_result = data.get('parse_status')
        parser_msg = data.get('parse_msg')
        data_dict = self.transform_data(data_dict)
        self.save_data(data_dict)

        # 新增url
        url_list = data.get('url_list')
        if url_list:
            # 保存新增url，格式为update，避免覆盖已经存在的url
            save_table_data(db_name=self.target_db, table_name='s_url_manager', records=url_list, mode=STORE_DATA_UPDATE)
        return parser_result, parser_msg


@zhihu_parser_map.register(func_name='question')
class ZhihuQuestionParser(ZhihuParser):

    def __init__(self):
        super().__init__()
        self.table_name = ''

    def parse_data(self, data):
        json_data = json.loads(data)
        data_list = json_data['data']
        session = json_data.get('session')
        next_url = json_data['paging']['next']
        url_list = [next_url]
        print(1)
        return {
            'parse_status': True,
            'parse_msg': '解析成功',
            'data_dict': [{
            }],
            'url_list': url_list,
        }


    def transform_data(self, data_dict):
        return data_dict




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    url = r'https://movie.douban.com/subject/6791750/comments'
    html = HtmlDownloader().request_data(url)

    # Parser = DoubanUserParser()
    Parser = DoubanCommentParser()
    # Parser = DoubanMovieParser()
    # print(Parser.get_url(object_type='movie', data_type='comment'))
    Parser.run_parser(html)