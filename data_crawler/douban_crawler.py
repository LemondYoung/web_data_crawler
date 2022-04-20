#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> douban_crawler
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

from constants import *
from data_crawler.html_downloader import HtmlDownloader
from data_parse.parse_tools.date_parse import standardize_date
from data_parse.parse_tools.url_parse import split_douban_url, split_url
from data_sync.data_load.mysql_data_load import save_table_data

class DoubanCrawler(object):

    def __init__(self):
        super(DoubanCrawler, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
        }
        self.target_url = 'https://movie.douban.com/'
        self.cur_url = None
        self.table_name = None
        self.target_db = 'douban_db'
        self.save_mode = STORE_DATA_REPLACE

    def parse_data(self, html):
        pass

    def transform_data(self, data_dict):
        return data_dict

    def save_data(self, data_dict):
        result, result_data = save_table_data(self.table_name, records=data_dict, target_db_name=self.target_db, mode=self.save_mode)
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
        data_dict = self.transform_data(data_dict)
        self.save_data(data_dict)
        # 新增url
        url_list = data.get('url_list')
        if url_list:
            save_table_data(table_name='s_url_manager', records=url_list)
        return True


class DoubanUserCrawler(DoubanCrawler):

    def __init__(self):
        super(DoubanUserCrawler, self).__init__()
        self.table_name = 't_user_info'

    def parse_data(self, html):
        html = etree.HTML(html)
        # 短评列表
        user_url = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="pic"]/a/@href')[0])
        user_code = split_url(url=user_url).get('path')[1]
        user_name = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="info"]/h1/text()')[0])
        user_profile = html.xpath('//div[@id="profile"]')[0]
        user_address = str(user_profile.xpath('.//div[@class="user-info"]/a/text()')[0])
        user_join_date = str(user_profile.xpath('.//div[@class="user-info"]/div[@class="pl"]/text()')[1])
        user_intro = str(user_profile.xpath('.//span[@id="intro_display"]/text()')[0])
        data = {
            'data_dict': {
                'user_code': user_code,
                'user_name': user_name,
                'user_url': user_url,
                'user_area': user_address,
                'join_date': user_join_date,
                'intro': user_intro,
            }
        }
        return data


    def transform_data(self, data_dict):
        new_data = []
        user = data_dict
        user['user_name'] = user['user_name'].strip(' \n')
        user['join_date'] = standardize_date(user['join_date'], separator='')
        new_data.append(user)
        return new_data


class DoubanMovieCrawler(DoubanCrawler):

    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_info'

    def parse_data(self, html):
        html = etree.HTML(html)
        # 短评列表
        json_data = html.xpath('//script[@type="application/ld+json"]/text()')[0]
        json_ = json.loads(json_data, strict=False)
        poster_url = json_['image']
        movie_code = json_['url'].split('/')[2]

        movie_names = json_['name'].split(' ')
        movie_year = json_['datePublished']
        # movie_name = html.xpath('//title/text()')[0]
        movie_url = "https://movie.douban.com" + json_['url']

        summary = html.xpath('//div[@id="link-report"]/span[1]/text()')[0]
        info_list = etree.tostring(html.xpath('.//div[@id="info"]')[0], encoding="utf-8", pretty_print=True, method="text").decode("utf-8").split('\n')
        genres = movie_country = movie_year = movie_length = movie_language = alias = None
        for info in info_list:
            if '类型:' in info:
                genres = info.split('类型:')[1].strip('')
            elif '制片国家/地区:' in info:
                movie_country = info.split('制片国家/地区:')[1].strip('')
            elif '上映日期:' in info:
                movie_year = info.split('上映日期:')[1].strip('')
            elif '片长:' in info:
                movie_length = info.split('片长:')[1].strip('')
            elif '语言:' in info:
                movie_language = info.split('语言:')[1].strip('')
            elif '又名:' in info:
                alias = info.split('又名:')[1].strip('')


        movie_score = html.xpath('.//div[@id="interest_sectl"]')[0]
        rating = movie_score.xpath('.//strong/text()')[0]
        rating_count = movie_score.xpath('.//a[@class="rating_people"]/span[1]/text()')[0]

        data = {
            'data_dict': [{
                'movie_code': movie_code,
                'movie_name': movie_names[0],
                'movie_url': movie_url,
                'poster_url': poster_url,
                'rating': float(rating),
                'rating_count': int(rating_count),
                # 'wish_count': user_intro,
                # 'collent_count': user_intro,
                'movie_year': movie_year,
                'movie_country': movie_country,
                'movie_length': movie_length,
                'movie_language': movie_language,
                'alias': alias,
                'genres': genres,
                'summary': str(summary).strip(' \n'),
            }]
        }
        return data

    def transform_data(self, data_dict):
        new_data = []
        for item in data_dict:
            new_data.append(item)

        return new_data


class DoubanCommentCrawler(DoubanCrawler):

    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_comment'

    def parse_data(self, html):
        html = etree.HTML(html)

        movie_url = str(html.xpath('//div[@class="movie-summary"]/div[@class="movie-pic"]/a/@href')[0])
        movie_code = split_douban_url(movie_url).get('url_type_value')
        # 短评列表
        comment_list = html.xpath('//div[@id="comments"]//div[@class="comment"]')
        new_comment_list = []
        for comment in comment_list:
            comment_user = str(comment.xpath('.//span[@class="comment-info"]/a/text()')[0])
            comment_user_url = str(comment.xpath('.//span[@class="comment-info"]/a/@href')[0])
            if len(comment.xpath('.//span[@class="comment-info"]/span')) == 3:
                comment_rating = str(comment.xpath('.//span[@class="comment-info"]/span[2]/@title')[0])
            else:
                comment_rating = None
            comment_time = str(comment.xpath('.//span[@class="comment-info"]/span[@class="comment-time "]/@title')[0])
            comment_content = str(comment.xpath('.//span[@class="short"]/text()')[0])
            vote_count = int(comment.xpath('.//span[@class="comment-vote"]/span[1]/text()')[0])
            comment_item = {
                'movie_code': movie_code,
                'user_name': comment_user,
                'user_url': comment_user_url,
                'comment_score': comment_rating,
                'comment_date_time': comment_time,
                'comment_content': comment_content,
                'vote_count': vote_count,
            }
            new_comment_list.append(comment_item)
        data = {
            'data_dict': new_comment_list
        }
        return data

    def transform_data(self, data_dict):
        score_map = {
            '力荐': 5,
            '推荐': 4,
            '还行': 3,
            '较差': 2,
            '很差': 1,
        }
        new_data = []
        comment_list = data_dict
        for item in comment_list:
            try:
                item['user_code'] = split_douban_url(item['user_url']).get('url_type_value')
                item['comment_score'] = score_map.get(item['comment_score'])
                comment_time = datetime.datetime.strptime(item['comment_date_time'], '%Y-%m-%d %H:%M:%S')
                item['comment_date_time'] = comment_time
                item['comment_date'] = datetime.datetime.strftime(comment_time, '%Y%m%d')

                new_data.append(item)
            except Exception as e:
                continue
        return new_data


class DoubanUserMovieCrawler(DoubanCrawler):

    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_comment'

    def parse_data(self, html1):
        # html2 = """{html}""".format(html=html)
        html = etree.HTML(html1)
        # result = etree.tostring(html1, encoding='utf-8')  # 解析对象输出代码
        # result1 = result.decode('utf-8')
        sub_url = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="pic"]/a/@href')[0])
        user_code = sub_url.split('/')[2]
        # 短评列表
        movie_list = html.xpath('//div[@id="content"]//div[@class="item"]')
        new_movie_list = []
        url_list = []
        for movie in movie_list:
            movie_url = movie.xpath('.//div[@class="info"]/ul/li[1]/a/@href')[0]
            info_li = movie.xpath('.//div[@class="info"]/ul/li')
            temp = etree.tostring(movie.xpath('.//div[@class="info"]/ul')[0], encoding='utf-8').decode('utf-8')
            try:
                if len(info_li) >= 3:  # 日期和评分
                    movie_start = movie.xpath('.//div[@class="info"]/ul/li[3]/span[1]/@class')[0]
                    comment_date = movie.xpath('.//div[@class="info"]/ul/li[3]/span[2]/text()')[0]
                    # comment_tag = movie.xpath('.//div[@class="info"]/ul/li[3]/span[3]/text()')[0]
                    if len(info_li) >= 4:  # 评论
                        comment = movie.xpath('.//div[@class="info"]/ul/li[4]/span[1]/text()')[0]
                    else:
                        logging.warning('%s的评论解析失败, 未标注评论日期或分数', movie_url)
                        comment = None
                else:
                    logging.warning('%s的日期和评论解析失败, 未评论', movie_url)
                    movie_start = comment_date = comment = None
            except Exception as e:
                logging.error('%s的评论解析失败%s, 其他原因%s', movie_url, e, temp)
                continue
                # try:
                #     _ = movie.xpath('.//div[@class="info"]/ul/li')
                #     if len(_) == 4:  # 评论在第四个li
                #         comment = movie.xpath('.//div[@class="info"]/ul/li[4]/span[1]/text()')[0]
                #     else:
                #         temp = etree.tostring(_, encoding='utf-8').decode('utf-8')
                #         comment = None
                #         logging.error('li长度不够%s', temp)
                # except Exception as e:
                #     logging.error('%s的评论解析失败, 其他原因%s', movie_url, e)
                #     comment = None
            comment_item = {
                'user_code': user_code,
                'movie_url': str(movie_url),
                'comment_score': str(movie_start),
                'comment_date': str(comment_date),
                # 'comment_tag': comment_tag,
                'comment_content': str(comment),
            }
            new_movie_list.append(comment_item)
            url_list.append({'url': movie_url, 'url_type': 'movie'})
        data = {
            'data_dict': new_movie_list,
            'url_list': url_list,
        }
        return data

    def transform_data(self, data_dict):
        score_map = {
            'rating5-t': 5,
            'rating4-t': 4,
            'rating3-t': 3,
            'rating2-t': 2,
            'rating1-t': 1,
        }
        new_data = []
        for item in data_dict:
            item['movie_code'] = split_douban_url(item['movie_url']).get('url_type_value')
            item['comment_score'] = score_map.get(item['comment_score'])
            item['comment_date'] = standardize_date(date=item['comment_date'])

            new_data.append(item)
        return new_data



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    url = r'https://movie.douban.com/subject/6791750/comments'
    html = HtmlDownloader().request_data(url)

    # crawler = DoubanUserCrawler()
    crawler = DoubanCommentCrawler()
    # crawler = DoubanMovieCrawler()
    # print(crawler.get_url(object_type='movie', data_type='comment'))
    crawler.run_parser(html)