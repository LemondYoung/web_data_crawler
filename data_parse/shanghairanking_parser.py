# 解析出page页
import json, datetime
import logging
import os

from lxml import etree

from data_crawler.html_parser import Parser
from data_parse.parse_tools.img_parser import ocr, get_img_format
from data_parse.parse_tools.url_parse import split_url


#
class ShanghaiRankingParser(Parser):

    def __init__(self):
        super().__init__()
        self.table_name = None

    def parse_data(self, html, url=None, parser_type=None, **kwargs):
        data = json.loads(html).get('data')
        if not data:
            logging.error('获取数据失败')
            return False
        logging.info('获取数据成功')

        return {
            'url': url,
            'result': True,
            'data_list': [
                {'table_name': 't_blog_info', 'data': new_blog_list},
                {'table_name': 't_img_info', 'data': img_data},
                {'table_name': 's_url_manager', 'data': blog_url_data},
                {'table_name': 's_url_manager', 'data': img_url_data},
            ]
        }

