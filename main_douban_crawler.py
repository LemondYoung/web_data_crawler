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
from data_crawler.url_manager import split_urls, get_urls, get_url_list
from data_parse.douban_parser import douban_parser_map
from data_parse.parse_tools.url_parse import split_douban_url
from utils.log import InterceptHandler

logging.basicConfig(handlers=[InterceptHandler()], level=0)


class DoubanCrawlerMain(object):
    def __init__(self):
        self.urlManager = url_manager.UrlManager(db_name='douban_data')
        self.htmlDownloader = html_downloader.HtmlDownloader()

    # 获取要解析的url
    def get_url(self, object_type, object_value, data_type=None, start=0, limit=20, status='P', sort='time' ):
        """
        @电影 movie: get_url(object_type='movie'', object_value='6791750', data_type=None, start=0, limit=20, status='P', sort='time' )
        @电影评论 movie_comment: get_url(object_type='movie', object_value='6791750', data_type=None, start=0, limit=20, status='P', sort='time' )
        @看过的电影 people_movie: get_url(object_type='user_movie', object_value='180015255')
        @用户 user: get_url(object_type='user', object_value='180015255', data_type=None, start=None, limit=None, status=None, sort=None )
        @用户电影 user_movie: get_url(object_type='user_movie', object_value='180015255', data_type='movie_list', start=0, limit=20, status=None, sort='time' )
        :param object_type:
        :param object_value:
        :param data_type:
        :param start: 0
        :param limit: 20
        :param status:
        :param sort: 排序 [new_score|time|follows] [time|rating|title]
        :return:
        """
        comment_sort_type = ['new_score', 'time', 'follows']  # 热门，最新，好友
        movie_sort_type = ['rating', 'time', 'title']  # 评价，时间，标题
        status_type = ['P', 'F']  # 看过，想看

        if object_type == 'movie':
            self.cur_url = urllib.parse.urljoin('https://movie.douban.com/subject/', object_value) + '/'
        elif object_type == 'user':
            self.cur_url = urllib.parse.urljoin('https://douban.com/people/', object_value) + '/'
        elif object_type == 'user_movie':
            self.cur_url = urllib.parse.urljoin('https://movie.douban.com/people/', object_value) + '/collect'

        else:
            return False

        if data_type == 'comment':
            if not isinstance(start, int) or not isinstance(limit, int) :
                logging.error('start or limit 格式错误，start=%s，limit=%s', start, limit)
                return False
            elif status not in status_type:
                logging.error('status错误，status=%s', status)
                return False
            elif sort not in comment_sort_type:
                logging.error('sort格式错误，sort=%s', sort)
                return False
            else:
                url_param = {
                    'start': start,
                    'limit': limit,
                    'status': status,
                    'sort': sort,
                }
            self.cur_url = urllib.parse.urljoin(self.cur_url, 'comments')
            query_string1 = urllib.parse.urlencode(url_param)
            self.cur_url = self.cur_url + '?' + query_string1
        elif data_type == 'movie_list':  # 用户电影列表
            if not isinstance(start, int):
                logging.error('start格式错误，start=%s', start)
                return False
            elif sort not in movie_sort_type:
                logging.error('sort格式错误，sort=%s', sort)
                return False
            else:
                url_param = {
                    'start': start,
                    'sort': sort,
                    'rating': 'all',
                    'filter': 'all',
                    # 'mode': 'grid',
                }
            query_string1 = urllib.parse.urlencode(url_param)
            self.cur_url = self.cur_url + '?' + query_string1
        return self.cur_url

    # 生成url
    def general_url_list(self, object_type, object_value=None, status=None, sort=None):
        """
        @电影评论 movie_comment: get_url_list(object_type='movie_comment', object_value='6791750', status='P', sort='time')
        @用户电影 user_movie: get_url_list(object_type='user_movie', object_value='', status=None, sort='time')
        @top250 top250: get_url_list(object_type='top250')
        :param object_type:
        :param object_value:
        :param status: ['P', 'F']  # 看过，想看
        :param sort: 排序 [new_score|time|follows] [time|rating|title]
        :return:
        """
        comment_sort_type = ['new_score', 'time', 'follows']  # 热门，最新，好友
        movie_sort_type = ['rating', 'time', 'title']  # 评价，时间，标题
        status_type = ['P', 'F']  # 看过，想看

        # 参数条件判断
        if status and status not in status_type:
            logging.error('status错误，status=%s', status)
            return False
        elif object_type == 'movie_comment' and sort and sort not in comment_sort_type:
            logging.error('sort格式错误，sort=%s', sort)
            return False
        elif object_type == 'user_movie' and sort and sort not in movie_sort_type:
            logging.error('sort格式错误，sort=%s', sort)
            return False

        # url 分流
        if object_type == 'movie_comment':
            status = status or 'P'
            sort = sort or 'time'
            count, step = 2000, 15
            list_list = [[start, step] for start in list(range(0, count))[0::step]]  # 指定长度和步长

            url_list = []
            base_url = urllib.parse.urljoin('https://movie.douban.com/subject/', object_value) + '/comments'
            for start, step in list_list:
                url_param = {
                    'start': start,
                    'limit': step,
                    'status': status,
                    'sort': sort,
                }
                url = base_url + '?' + urllib.parse.urlencode(url_param)
                url_list.append(url)

        elif object_type == 'user_movie':
            status = status or 'P'
            sort = sort or 'time'
            count, step = 2000, 15
            list_list = [[start, step] for start in list(range(0, count))[0::step]]  # 指定长度和步长

            url_list = []
            base_url = urllib.parse.urljoin('https://movie.douban.com/people/', object_value) + '/collect'
            for start, step in list_list:
                url_param = {
                    'start': start,
                    'sort': sort,
                    'rating': 'all',
                    'filter': 'all',
                    # 'mode': 'grid',
                }
                url = base_url + '?' + urllib.parse.urlencode(url_param)
                url_list.append(url)

        elif object_type == 'top250':
            count, step = 250, 25
            list_list = [[start, step] for start in list(range(0, count))[0::step]]  # 指定长度和步长

            url_list = []
            base_url = 'https://movie.douban.com/top250'
            for start, step in list_list:
                url_param = {
                    'start': start,
                    'filter': ''
                }
                url = base_url + '?' + urllib.parse.urlencode(url_param)
                url_list.append(url)
        else:
            url_list = False

        return url_list

    # 入口函数
    def run_crawler(self, urls_list=None):
        if not urls_list:
            url_value = 'anasshole'
            url = self.get_url(object_type='user_movie', object_value=url_value)
            add_result = self.urlManager.add_url(url)
            if add_result is False:
                logging.error('url添加失败')
                return False

            all_url = self.urlManager.get_all_url(is_download=False, is_parse=False)
        else:
            all_url = urls_list
        # 设置间隔策略
        logging.info('获取到url总数%s，开始设置策略', len(all_url))
        new_urls = split_urls(all_url, strategy="random")
        logging.warning('策略分配成功，共分为%s组', len(new_urls))
        # 开始爬虫
        windex = 1
        for index1, dic in enumerate(new_urls):
            urls, count, sleep = dic.values()

            logging.info('%s', '*'*110)
            logging.info('%s[%s/%s]此次爬取%s条，间隔%ss%s', '*'*50, index1, len(new_urls), count, sleep, '*'*50,)
            logging.info('%s', '*'*110)
            time.sleep(sleep)
            for index2, url in enumerate(urls, 1):
                time.sleep(1)
                parser_type = split_douban_url(url).get('url_type')
                logging.warning('%s当前url进度[%s/%s], 总进度[%s/%s] %s', '*'*40, index2, len(urls), windex, len(all_url), '*'*40)
                windex += 1
                # 1. 获取下载器
                html = self.htmlDownloader.request_data(url)
                if html is False:
                    logging.error('网页下载失败')
                    logging.warning(url)
                    continue
                self.urlManager.add_url(url)

                # 2. 获取对应的解析器
                cur_parser = douban_parser_map.get(parser_type)
                if not cur_parser:
                    logging.error('%s无对应的解析器', parser_type)
                    return False
                # 开始解析
                logging.info('当前解析器为%s', cur_parser)
                parser_result, parser_msg = cur_parser().run_parser(html=html)
                # 更新url
                self.urlManager.update_url(url, result=parser_result, msg=parser_msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    crawler = DoubanCrawlerMain()
    # crawler.run_crawler()
    urls = get_url_list(url_type='movie', db_name='douban_data')
    # urls = crawler.general_url_list(object_type='movie_comment', object_value='Lion1874', status='P', sort='time')
    # urls = crawler.general_url_list(object_type='movie_comment', object_value='6791750', status='P', sort='new_score')
    # urls = crawler.general_url_list(object_type='top250')
    urls = ['https://movie.douban.com/subject/30244761/']
    crawler.run_crawler(urls)
