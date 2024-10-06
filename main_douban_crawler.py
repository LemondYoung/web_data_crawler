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
import os
import time
import urllib
from urllib import parse

from data_crawler import url_manager
from data_crawler.html_downloader import HtmlDownloader
from data_crawler.url_manager import split_urls, get_url_list
from data_parse.douban_parser import douban_parser_map
from data_parse.parse_tools.url_parser import split_douban_url
from settings import HTML_DATA_PATH, DOUBAN_COOKIE
from utils.log import InterceptHandler

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


class DoubanCrawlerMain(object):
    def __init__(self):
        self.db_name = 'douban_data'
        self.urlManager = url_manager.UrlManager(db_name=self.db_name)
        self.htmlDownloader = HtmlDownloader()

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
    @staticmethod
    def generate_url_list(object_type, object_value=None, status=None, sort=None):
        """ 生成豆瓣相关的url列表
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
            logging.info(f"准备生成url，规则{object_type}，总数{count}，每页{step}个")
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

        elif object_type == 'movie_recommend':
            tags = ['喜剧', '爱情', '动作', '科幻', '动画', '悬疑', '犯罪', '惊悚', '冒险', '音乐', '历史', '奇幻',
                    '恐怖', '战争', '传记', '歌舞', '武侠', '情色', '灾难', '西部', '纪录片', '短片']
            count, step = 500, 20
            list_list = [[start, step] for start in list(range(0, count))[0::step]]  # 指定长度和步长
            url_list = []
            base_url = 'https://m.douban.com/rexxar/api/v2/movie/recommend'
            for tag in tags:
                for start, step in list_list:
                    url_param = {
                        'refresh': 0,
                        'start': start,
                        'count': step,
                        'uncollect': 'false',
                        'selected_categories': '{"类型":"' + tag + '"}',
                        'tags': tag,
                        'ck': '-uwX'
                    }
                    url = base_url + '?' + urllib.parse.urlencode(url_param)
                    # url = r'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=300&count=20&uncollect=false&selected_categories={"类型":"惊悚"}&uncollect=false&tags="惊悚"&ck=-uwX'
                    url_list.append(url)
        else:
            url_list = False

        return url_list

    def get_demo_urls(self):
        url_value = 'anasshole'
        url = self.get_url(object_type='user_movie', object_value=url_value)
        add_result = self.urlManager.add_url(url)
        if add_result is False:
            logging.error('url添加失败')
            return False
        all_url = self.urlManager.get_all_url(url_type='user_movie', is_download=False, is_parse=False)
        return all_url

    # 入口函数
    def run_crawler(self, urls_list=None, is_run_all=True):
        """ 运行爬虫
        :param urls_list: url列表，如果没有的话，需要。。。
        :param is_run_all: 是否全部运行（检查url管理表）
        :return:
        """
        all_url = urls_list or self.get_demo_urls()
        # 设置间隔策略
        logging.info('获取到url总数%s，开始设置策略', len(all_url))
        new_urls = split_urls(all_url, strategy="random")
        logging.warning('策略分配成功，共分为%s组', len(new_urls))
        # 开始爬虫（分为两层，有一定的间隔策略）
        t_index, t_fail_count = 1, 0
        for index1, dic in enumerate(new_urls, 1):
            urls, count, sleep = dic.values()

            logging.info('%s', '*'*110)
            logging.info('%s[%s/%s]此次爬取%s条，间隔%ss%s', '*'*50, index1, len(new_urls), count, sleep, '*'*50,)
            logging.info('%s', '*'*110)
            fail_count = 0
            for index, url in enumerate(urls, 1):
                logging.warning('%s当前url进度[%s/%s], 总进度[%s/%s] %s', '*'*40, index, len(urls), t_index, len(all_url), '*'*40)
                t_index += 1

                # 1. 分析并检查url
                split_dict = split_douban_url(url)
                parser_type, url_remark = split_dict.get('url_type'), split_dict.get('remark')
                add_url_dict = {'url': url, 'url_type': parser_type}
                if url_remark:  # 这个的是未知状态才行
                    add_url_dict['remark'] = url_remark
                    add_url_dict['url_status'] = 2
                add_result = self.urlManager.add_url(add_url_dict, is_run_all)
                # 判断1.如果url已经存在且不重复运行，则不再解析；2.如果url是已知的未知状态，也不再解析
                if add_result is None or url_remark:
                    logging.info('url无需解析，跳过')
                    continue

                # 2. 获取下载器
                if parser_type == 'movie_recommend':
                    headers_dict = {'Referer': 'http://movie.douban.com/explore'}
                    html = self.htmlDownloader.request_api(url, headers_dict=headers_dict)
                else:
                    tunnel_dict = {"proxy": "p507.kdltpspro.com:15818", "user": "t12693231208168", "pwd": "4p3878eq"}
                    headers_dict = {'Cookie': DOUBAN_COOKIE}
                    html = self.htmlDownloader.request_data(url, use_proxies=True)
                    # html = self.htmlDownloader.request_data(url, headers_dict=headers_dict)
                # html_file = os.path.join(HTML_DATA_PATH, 'douban', 'user_251679774.html')
                # html = self.htmlDownloader.read_local_html_file(html_file)
                if html is False:
                    parser_result, parser_msg = False, '网页下载失败'
                    logging.error(f"网页下载失败: {url}")
                else:
                    # 3. 获取对应的解析器，开始解析
                    cur_parser = douban_parser_map.get(parser_type)
                    if not cur_parser:
                        logging.error(f'当前解析类型{parser_type}无对应的解析器')
                        return False
                    logging.info(f'当前解析类型为：{parser_type}，对应解析器：{cur_parser}', )
                    parser_result, parser_msg = cur_parser().run_parser(html=html)
                # 4. 更新url
                self.urlManager.update_url(url, result=parser_result, msg=parser_msg)
                if parser_result is False:
                    fail_count += 1
                    t_fail_count += 1
                logging.warning('%s当前失败个数[%s/%s], 总失败个数[%s/%s] %s', '*'*40, fail_count, index, t_fail_count, t_index, '*'*40)
                time.sleep(2)  # 停顿一会会，防止被封ip
            time.sleep(sleep)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    crawler = DoubanCrawlerMain()

    # 爬取电影 movie
    urls = get_url_list(url_type='movie', db_name='douban_data', url_status='init')
    # urls = get_url_list(url_type='movie', db_name='douban_data', url_status='fail')
    urls.reverse()

    # 爬取电影评论 movie_comment
    # urls = crawler.generate_url_list(object_type='movie_comment', object_value='Lion1874', status='P', sort='time')
    # urls = crawler.generate_url_list(object_type='movie_comment', object_value='1291546', status='P', sort='new_score')

    # 爬取用户电影 user_movie
    # urls = crawler.generate_url_list(object_type='user_movie', object_value='Lion1874', status='P', sort='time')
    # urls = crawler.generate_url_list(object_type='user_movie', object_value='anasshole', status='P', sort='time')
    # urls = crawler.generate_url_list(object_type='user_movie', object_value='251679774', status='P', sort='time')

    # 爬取电影 top250
    # urls = crawler.generate_url_list(object_type='top250')

    # 爬取电影推荐 movie_recommend
    # urls = crawler.generate_url_list(object_type='movie_recommend')

    # 爬取电影人 movie_personage
    # urls = get_url_list(url_type='movie_personage', db_name='douban_data', url_status='init')[0000:10000]
    # urls.reverse()
    # urls = get_url_list(url_type='movie_personage', db_name='douban_data', url_status='fail')
    # urls.reverse()
    # urls = urls1 + urls2

    # 指定爬取内容
    # urls = ['https://www.douban.com/personage/27255890/',]
    # urls = ['https://www.douban.com/personage/36688013/',]
    # urls = ['https://movie.douban.com/subject/5977807/']
    crawler.run_crawler(urls, is_run_all=True)
