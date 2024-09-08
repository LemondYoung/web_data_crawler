#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> spider_main
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:21
@Desc   ：
==================================================
"""
import logging
import time
import urllib
from urllib import parse

from data_crawler import url_manager
from data_crawler import html_downloader
from data_crawler.url_manager import split_urls
from data_parse.zhihu_parser import zhihu_parser_map
from utils.log import InterceptHandler

logging.basicConfig(handlers=[InterceptHandler()], level=0)


class ZhihuCrawlerMain(object):
    def __init__(self):
        self.urlManager = url_manager.UrlManager(db_name='zhihu_data')
        self.htmlDownloader = html_downloader.HtmlDownloader()

    # 获取要解析的url
    def get_url(self ):
        pass

    # 生成url
    def generate_url_list(self):
        pass

    # 入口函数
    def run_crawler(self, url=None, is_run_all=True):

        # 开始爬虫
        windex = 1
        while True:
            logging.info('%s', '*'*110)
            time.sleep(3)
            windex += 1
            try:
                # 1. 解析分析url
                parser_type = 'question'
                add_result = self.urlManager.add_url({'url': url, 'url_type': parser_type}, is_run_all)
                if add_result is None:
                    logging.info('url无需解析，跳过')
                    continue

                # 2. 获取下载器
                html = self.htmlDownloader.request_data(url)
                if html is False:
                    logging.error('网页下载失败')
                    logging.warning(url)
                    return False

                # 3. 获取对应的解析器开始解析
                cur_parser = zhihu_parser_map.get(parser_type)
                if not cur_parser:
                    logging.error('%s无对应的解析器', parser_type)
                    return False
                logging.info('当前解析器为%s', cur_parser)
                parser_result, parser_msg = cur_parser().run_parser(html=html)
                if parser_result is False:
                    logging.error('网页解析失败')
            except Exception as e:
                logging.error(e)
                parser_result = False
            self.urlManager.update_url(url, result=parser_result, msg=parser_msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    crawler = ZhihuCrawlerMain()
    # splider.run_crawler()
    # get_url_list(object_type='user_movie', object_value='', step=20, count=100, status=None, sort='time')
    # urls = crawler.generate_url_list(object_type='movie_comment', object_value='Lion1874', step=10, count=2000, status='P', sort='time')
    # urls = splider.generate_url_list(object_type='movie_comment', object_value='6791750', step=20, count=3000, status='P', sort='new_score')
    url = 'https://www.zhihu.com/api/v4/questions/585465221/feeds?cursor=d9f38bb508c45bfb520d037a2efe50d2&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1694957978758389513'
    url = 'https://www.zhihu.com/api/v4/questions/585465221/feeds?cursor=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=3&offset=1&order=default&platform=desktop&session_id='
    crawler.run_crawler(url)
