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
import random
import logging
import time
import urllib
from urllib import parse

from data_crawler import url_manager
from data_crawler import html_downloader
from data_crawler import douban_crawler
from data_parse.parse_tools.url_parse import split_douban_url
from utils.log import InterceptHandler

logging.basicConfig(handlers=[InterceptHandler()], level=0)

parser = {
    'user': douban_crawler.DoubanUserCrawler(),
    'movie': douban_crawler.DoubanMovieCrawler(),
    'movie_comment': douban_crawler.DoubanCommentCrawler(),
    'user_movie': douban_crawler.DoubanUserMovieCrawler(),
}


class spiderMain(object):
    def __init__(self):
        self.urlManager = url_manager.UrlManager()
        self.htmlDownloader = html_downloader.HtmlDownloader()


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


    def get_url_list(self, object_type, object_value, step=20, count=100, status='P', sort='time'):
        """
        @电影评论 movie_comment: get_url_list(object_type='movie_comment', object_value='6791750', step=20, count=100, status='P', sort='time')
        @用户电影 user_movie: get_url_list(object_type='user_movie', object_value='', step=20, count=100, status=None, sort='time')
        :param object_type:
        :param object_value:
        :param start: 0
        :param limit: 20
        :param status:
        :param sort: 排序 [new_score|time|follows] [time|rating|title]
        :return:
        """
        comment_sort_type = ['new_score', 'time', 'follows']  # 热门，最新，好友
        movie_sort_type = ['rating', 'time', 'title']  # 评价，时间，标题
        status_type = ['P', 'F']  # 看过，想看
        _ = list(range(0, count))[0::step]
        list_list = [[start, step] for start in _]

        # 参数条件判断
        if not isinstance(step, int) or not isinstance(count, int):
            logging.error('start or limit 格式错误，step=%s，count=%s', step, count)
            return False
        elif status not in status_type:
            logging.error('status错误，status=%s', status)
            return False
        elif object_type == 'movie_comment' and sort not in comment_sort_type:
            logging.error('sort格式错误，sort=%s', sort)
            return False
        elif object_type == 'user_movie' and sort not in movie_sort_type:
            logging.error('sort格式错误，sort=%s', sort)
            return False

        # url 分流
        if object_type == 'movie_comment':
            url_list = []
            cur_url = urllib.parse.urljoin('https://movie.douban.com/subject/', object_value) + '/comments'
            for start, step in list_list:
                url_param = {
                    'start': start,
                    'limit': step,
                    'status': status,
                    'sort': sort,
                }
                query_string1 = urllib.parse.urlencode(url_param)
                url = cur_url + '?' + query_string1
                url_list.append(url)

        elif object_type == 'user_movie':
            url_list = []
            cur_url = urllib.parse.urljoin('https://movie.douban.com/people/', object_value) + '/collect'
            for start, step in list_list:
                url_param = {
                    'start': start,
                    'sort': sort,
                    'rating': 'all',
                    'filter': 'all',
                    # 'mode': 'grid',
                }
                query_string1 = urllib.parse.urlencode(url_param)
                url = cur_url + '?' + query_string1
                url_list.append(url)
        else:
            url_list = False

        return url_list


    def split_urls(self, urls, strategy="random"):
        """
        切分url
        :param strategy: 策略：random随机
        :return:
        """
        new_urls = []
        fixed_num = 10
        if strategy == 'random':
            index = 1
            sub_new_urls = []
            random_num = random.randint(0, 5)
            for url in urls:
                sub_new_urls.append(url)
                if index == fixed_num + random_num:
                    _ = {
                        'urls': sub_new_urls,
                        'count': fixed_num + random_num,
                        'sleep': random_num,
                    }
                    new_urls.append(_)
                    index = 1
                    sub_new_urls = []
                    random_num = random.randint(0, 5)
                    continue
                index += 1
        else:
            pass
        return new_urls

    def run_crawler(self, urls_list=None):
        if not urls_list:
            # 入口
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
        new_urls = self.split_urls(all_url, strategy="random")
        logging.warning('策略分配成功，共分为%s组', len(new_urls))
        # 开始爬虫
        for index, dic in enumerate(new_urls):
            urls = dic.get('urls')
            sleep = dic.get('sleep')

            logging.info('%s', '*'*110)
            logging.info('%s[%s/%s]此次爬取%s条，间隔%ss%s', '*'*50, index, len(new_urls), dic.get('count'), sleep, '*'*50,)
            logging.info('%s', '*'*110)
            time.sleep(sleep)
            for url in urls:
                time.sleep(1)
                parser_type = split_douban_url(url).get('url_type')

                # 获取下载器
                html = self.htmlDownloader.request_data(url)
                if html is False:
                    logging.error('网页下载失败')
                    logging.warning(url)
                    return False
                # 获取对应的解析器
                curParser = parser.get(parser_type)
                # 开始解析
                logging.info('当前解析器为%s', curParser)
                parser_result = curParser.run_parser(html=html)
                if parser_result is False:
                    logging.error('网页解析失败')
                    return False
                else:
                    self.urlManager.update_url(url)
                # todo 更新url


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    splider = spiderMain()
    # splider.run_crawler()
    # get_url_list(object_type='user_movie', object_value='', step=20, count=100, status=None, sort='time')
    urls = splider.get_url_list(object_type='user_movie', object_value='Lion1874', step=10, count=2000, status='P', sort='time')
    # urls = splider.get_url_list(object_type='movie_comment', object_value='6791750', step=20, count=3000, status='P', sort='new_score')
    splider.run_crawler(urls)