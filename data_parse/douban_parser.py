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
import re
import urllib
from urllib import parse

from lxml import etree
import os
import requests

from data_parse.parse_tools.str_parser import parse_movie_name
from utils.trading_calendar import today
from constants import *
from data_crawler.html_downloader import HtmlDownloader
from data_parse.parse_tools.date_parser import standardize_date
from data_parse.parse_tools.url_parser import split_douban_url, split_url
from data_sync.data_load.mysql_data_load import save_table_data
from utils.class_tool.register_class import ParserRegister, DoubanParserRegister
from abc import ABC, abstractmethod

# 解析器，注册
douban_parser_map = DoubanParserRegister()


class DoubanParser(object):

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
        }
        self.target_url = 'https://movie.douban.com/'
        self.cur_url = None
        self.table_name = None
        self.target_db = 'douban_data'
        self.save_mode = STORE_DATA_INSERT_UPDATE

    @abstractmethod
    def parse_data(self, html) -> dict:
        """ 解析网页数据
        :param html: 接收原始网页
        :return:
        """
        pass

    def transform_data(self, data_dict):
        return data_dict

    def save_data(self, data_dict):
        if len(data_dict) == 0:
            return None, {}
        result, result_data = save_table_data(self.table_name, records=data_dict, db_name=self.target_db, mode=self.save_mode)
        if result is False or result is None:
            result_dict = {'length': len(data_dict), 'result_length': None, 'result_data': result_data}
            return False, result_dict
        else:
            logging.info(f'【保存数据】目标表{self.table_name}，计划执行数据量{len(data_dict)}，已执行数据量为{result}')
            result_dict = {'length': len(data_dict), 'result_length': result, 'result_data': result_data}
            return True, result_dict

    def run_parser(self, html):
        try:
            data = self.parse_data(html)
        except Exception as e:
            logging.error(f'网页解析失败：{e}')
            return False, str(e)

        # 保存数据
        data_dict = data['data_dict']
        parser_result = data.get('parse_status')
        parser_msg = data.get('parse_msg')
        url_list = data.get('url_list', [])        # 新增url

        logging.info(f'【解析数据】结果：{parser_result}，解析数量{len(data_dict)}，解析消息：{parser_msg}，新增url数量{len(url_list)}')
        if parser_result is False:
            logging.error(f'网页数据解析失败：{parser_msg}')
            return parser_result, parser_msg
        elif parser_result is None:
            logging.warning(f'网页数据解析未知：{parser_msg}')
            return parser_result, parser_msg
        data_dict = self.transform_data(data_dict)
        try:
            self.save_data(data_dict)
        except Exception as e:
            logging.error(f'错误：{e}')
            return False, str(e)

        if url_list:
            # 保存新增url，格式为update，避免覆盖已经存在的url
            save_table_data(db_name=self.target_db, table_name='s_url_manager', records=url_list, mode=STORE_DATA_INSERT_UPDATE)
        return parser_result, parser_msg


@douban_parser_map.register(func_name='user', func_info='豆瓣用户')
class DoubanUserParser(DoubanParser):

    def __init__(self):
        super(DoubanUserParser, self).__init__()
        self.table_name = 't_user_info'

    def parse_data(self, ori_html):
        html = etree.HTML(ori_html)
        # 短评列表
        user_url = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="pic"]/a/@href')[0])
        user_code = split_url(url=user_url).get('path')[1]
        user_name = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="info"]/h1/text()')[0])
        user_profile = html.xpath('//div[@id="profile"]')[0]
        user_join_date = str(user_profile.xpath('.//div[@class="user-info"]/div[@class="pl"]/text()')[1])
        user_address = str(user_profile.xpath('.//div[@class="user-info"]/div/span[@class="ip-location"]/text()')[0])
        user_intro = str(user_profile.xpath('.//span[@id="intro_display"]/text()')[0])
        data = {
            'parse_status': True,
            'parse_msg': None,
            'data_dict': {
                'user_code': user_code,
                'user_name': user_name.strip(' \n'),
                'user_url': user_url,
                'user_area': user_address.strip(' \n'),
                'join_date': user_join_date.strip(' \n'),
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


@douban_parser_map.register(func_name='movie', func_info='豆瓣电影')
class DoubanMovieParser(DoubanParser):

    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_info'

    def parse_data(self, html_source):
        unknown_msg, error_msg = "", ""
        html = etree.HTML(html_source)
        # 短评列表
        json_data = html.xpath('//script[@type="application/ld+json"]/text()')[0]  # 解析script标签中的json数据
        json_ = json.loads(json_data, strict=False)
        poster_url = json_['image']
        # if poster_url == 'https://img2.doubanio.com/cuphead/movie-static/pics/movie_default_large.png':
        #     poster_url = None
        movie_code = json_['url'].split('/')[2]

        # 正则表达式解析中文名称
        movie_name_str = json_['name']
        movie_name, other_name = parse_movie_name(movie_name_str)  # 调用已经写好的名称解析函数（主要运用正则表达式）

        movie_url = "https://movie.douban.com" + json_['url']

        summary_list = html.xpath('//div[@id="link-report-intra"]/span[@property="v:summary"]/text()')
        if len(summary_list) == 0:
            summary_list = html.xpath('//div[@id="link-report-intra"]/span[@class="all hidden"]/text()')
        summary = '\n'.join([element.strip(' \n') for element in summary_list])  # 沒分段
        info_list = etree.tostring(html.xpath('.//div[@id="info"]')[0], encoding="utf-8", pretty_print=True, method="text").decode("utf-8").split('\n')
        director = scriptwriter = leading = genres = movie_country = movie_year_str = movie_year = movie_length = movie_language = alias = score = score_number = None
        for info in info_list:
            if '导演:' in info:
                director = info.split('导演:')[1].strip(' ')
            elif '主演:' in info:
                leading = info.split('主演:')[1].strip(' ')
            elif '编剧:' in info:
                scriptwriter = info.split('编剧:')[1].strip(' ')
            elif '类型:' in info:
                genres = info.split('类型:')[1].strip(' ')
            elif '制片国家/地区:' in info:
                movie_country = info.split('制片国家/地区:')[1].strip(' ')
            elif '上映日期:' in info:
                movie_year_str = info.split('上映日期:')[1].strip(' ').split('(')[0]
            elif '首播:' in info:
                movie_year_str = info.split('首播:')[1].strip(' ').split('(')[0]
            elif '片长:' in info:
                movie_length = info.split('片长:')[1].strip(' ')
            elif '语言:' in info:
                movie_language = info.split('语言:')[1].strip(' ')
            elif '又名:' in info:
                alias = info.split('又名:')[1].strip(' ')
            try:
                movie_year = datetime.datetime.strptime(movie_year_str, '%Y-%m-%d').date()
            except Exception as e:
                movie_year = None
        # 解析电影人物列表
        personage_list = html.xpath('//span[@class="attrs"]/a')
        personage_url_list = []
        for personage in personage_list:
            personage_url = str(personage.xpath('./@href')[0])
            personage_name = str(personage.xpath('./text()')[0])
            personage_url_list.append({'url': personage_url, 'url_name': personage_name,'url_type': 'movie_personage'})

        # 豆瓣评分
        try:
            movie_score = html.xpath('.//div[@id="interest_sectl"]')[0]
            score = float(movie_score.xpath('.//strong/text()')[0])
            score_number = int(movie_score.xpath('.//a[@class="rating_people"]/span[1]/text()')[0])
        except Exception:  # 可能是太小众了，或者还未上映，或者就不让评分，综合下来数量很多，咱也给他都通过
            # unknown_msg += "豆瓣评分获取为空；"
            pass
        data_dict = [{
                'movie_code': movie_code,
                'movie_name': movie_name,
                'other_name': other_name,
                'movie_url': movie_url,
                'poster_url': poster_url,
                'score': score,
                'score_number': score_number,
                # 'wish_count': user_intro,
                # 'collent_count': user_intro,
                'director': director,
                'scriptwriter': scriptwriter,
                'leading': leading,
                'movie_year_str': movie_year_str,
                'movie_year': movie_year,
                'movie_country': movie_country,
                'movie_length': movie_length,
                'movie_language': movie_language,
                'alias': alias,
                'genres': genres,
                'summary': summary,
            }]
        # 整理解析状态
        if error_msg:
            data = {'parse_status': False, 'parse_msg': error_msg+unknown_msg, 'data_dict': data_dict}
        elif unknown_msg:
            data = {'parse_status': None, 'parse_msg': unknown_msg, 'data_dict': data_dict}
        else:  # 正常解析
            data = {'parse_status': True, 'parse_msg': None, 'data_dict': data_dict,
                    'url_list': personage_url_list}
        return data

    def transform_data(self, data_dict):
        return data_dict


@douban_parser_map.register(func_name='movie_comment', func_info='豆瓣电影评论')
class DoubanCommentParser(DoubanParser):

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
                comment_score = str(comment.xpath('.//span[@class="comment-info"]/span[2]/@title')[0])
            else:
                comment_score = None
            comment_time = str(comment.xpath('.//span[@class="comment-info"]/span[@class="comment-time "]/@title')[0])
            comment_content = str(comment.xpath('.//span[@class="short"]/text()')[0])
            vote_count = int(comment.xpath('.//span[@class="comment-vote"]/span[1]/text()')[0])
            comment_item = {
                'movie_code': movie_code,
                'user_name': comment_user,
                'user_url': comment_user_url,
                'comment_score': comment_score,
                'comment_date_time': comment_time,
                'comment_content': comment_content,
                'vote_count': vote_count,
            }
            new_comment_list.append(comment_item)
        data = {
            'parse_status': True,
            'parse_msg': None,
            'data_dict': new_comment_list,
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


@douban_parser_map.register(func_name='user_movie', func_info='豆瓣用户电影')
class DoubanUserMovieParser(DoubanParser):

    def __init__(self):
        super().__init__()
        self.table_name = 't_user_movie'

    def parse_data(self, html_ori):
        html = etree.HTML(html_ori)
        sub_url = str(html.xpath('//div[@id="db-usr-profile"]/div[@class="pic"]/a/@href')[0])
        user_code = sub_url.split('/')[2]
        # 短评列表
        movie_list = html.xpath('//div[@class="grid-view"]/div[@class="item comment-item"]')
        if len(movie_list) == 0:
            return {'parse_status': None, 'parse_msg': '该页面无用户电影信息', 'data_dict': []}
        new_movie_list = []
        url_list = []
        for movie in movie_list:
            movie_url = movie.xpath('.//div[@class="info"]/ul/li[1]/a/@href')[0]
            info_li = movie.xpath('.//div[@class="info"]/ul/li')
            temp = etree.tostring(movie.xpath('.//div[@class="info"]/ul')[0], encoding='utf-8').decode('utf-8')
            try:
                if len(info_li) >= 3:  # 有评论日期
                    movie_start = movie.xpath('.//div[@class="info"]/ul/li[3]/span[1]/@class')[0]
                    comment_date = movie.xpath('.//div[@class="info"]/ul/li[3]/span[@class="date"]/text()')[0]
                    # comment_tag = movie.xpath('.//div[@class="info"]/ul/li[3]/span[3]/text()')[0]
                else:
                    logging.warning('%s的日期和评论解析为空, 未评论', movie_url)
                    movie_start = comment_date = None
                if len(info_li) >= 4:  # 有评论内容
                    comment_content = movie.xpath('.//div[@class="info"]/ul/li[4]/span[1]/text()')[0]
                else:
                    comment_content = None
            except Exception as e:
                logging.error('%s的评论解析失败，其他原因%s %s', movie_url, e, temp)
                continue

            comment_item = {
                'user_code': user_code,
                'movie_url': str(movie_url),
                'comment_score': str(movie_start),
                'comment_date': str(comment_date),
                # 'comment_tag': comment_tag,
                'comment_content': str(comment_content) if comment_content is not None else None,
            }
            new_movie_list.append(comment_item)
            url_list.append({'url': movie_url, 'url_type': 'movie'})
        data = {
            'parse_status': True,
            'parse_msg': None,
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


@douban_parser_map.register(func_name='top250', func_info='豆瓣电影TOP250')
class DoubanTop250Parser(DoubanParser):

    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_top250'

    def parse_data(self, ori_html):
        # html2 = """{html}""".format(html=html)
        html = etree.HTML(ori_html)
        movie_list = html.xpath('//ol[@class="grid_view"]/li/div[@class="item"]')
        data = []
        url_list = []
        for movie in movie_list:
            rank = movie.xpath('./div[@class="pic"]/em/text()')[0]
            movie_url = movie.xpath('./div[@class="info"]/div[@class="hd"]/a/@href')[0]
            movie_name = movie.xpath('./div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()')[0]
            score = movie.xpath('./div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
            try:
                brief = movie.xpath('./div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()')[0]
            except Exception as e:
                brief = None

            movie_item = {
                'rank': rank,
                'movie_url': movie_url,
                'movie_name': str(movie_name),
                'score': str(score),
                'brief': str(brief) or None,
            }
            data.append(movie_item)
            url_list.append({'url': movie_url, 'url_type': 'movie'})
        return {
            'parse_status': True,
            'parse_msg': None,
            'data_dict': data,
            'url_list': url_list,
        }

    def transform_data(self, data_dict):
        new_data = []
        for item in data_dict:
            item['movie_code'] = split_douban_url(item['movie_url']).get('url_type_value')
            item['join_date'] = today
            new_data.append(item)
        return new_data


@douban_parser_map.register(func_name='movie_recommend', func_info='豆瓣电影推荐')
class DoubanMovieRecommendParser(DoubanParser):
    """
    豆瓣电影推荐，主要是获取豆瓣电影的列表，详细信息or评论可以等拿到url后再进一步解析
    """
    def __init__(self):
        super().__init__()
        self.table_name = 's_url_manager'

    def parse_data(self, json_data):
        # 该接口返回的json数据，可以直接使用不需要解析
        data = []
        for item in json_data['items']:
            if item['type'] == 'movie':
                movie_url = f"https://movie.douban.com/subject/{item['id']}/"
                movie_name = item['title']
                data.append({'url': movie_url, 'url_name': movie_name, 'url_type': 'movie'})
        return {'data_dict': data, 'parse_status': True, 'parse_msg': None}


@douban_parser_map.register(func_name='movie_personage', func_info='豆瓣电影人物')
class DoubanMoviePersonageParser(DoubanParser):
    """
    豆瓣电影任务，导演、编剧、主演人物主页信息，外加影片数据量、最近的50部电影
    """
    def __init__(self):
        super().__init__()
        self.table_name = 't_movie_personage'

    def request_collection(self, collection_id):
        """ 直接请求收藏列表 """
        collection_url = f'https://m.douban.com/rexxar/api/v2/elessar/work_collections/{collection_id}/works?collection_title=影视&sortby=collection&count=50'
        json_data = HtmlDownloader().request_api(collection_url, headers_dict={'Referer': 'http://movie.douban.com/explore'})
        # 电影数量
        movie_count = json_data.get('total')
        # 解析电影列表（样例，肯定不完整，该接口也没找到循环的方法）
        movie_url_list = []
        for item in json_data.get('works'):
            movie = item['subject']
            movie_url = movie['url']
            movie_name = movie['title']
            movie_url_list.append({'url': movie_url, 'url_name': movie_name, 'url_type': 'movie'})
        return movie_count, movie_url_list

    def parse_data(self, ori_html):
        html = etree.HTML(ori_html)
        # 解析url、code、头像链接
        personage_url = html.xpath('//meta[@property="og:url"]/@content')[0]
        personage_code = personage_url.split('/')[-1]
        avatar_url = html.xpath('//img[@class="avatar"]/@src')[0]
        # https://img1.doubanio.com/f/vendors/8dd0c794499fe925ae2ae89ee30cd225750457b4/pics/personage-default-medium.png
        # 正则表达式解析中文名称
        personage_name_str = html.xpath('//h1[@class="subject-name"]/text()')[0]
        personage_name, other_name = parse_movie_name(personage_name_str)  # 调用已经写好的名称解析函数（主要运用正则表达式）

        # 解析人物简介
        summary_list = html.xpath('//div[@class="content"]/p/text()')
        summary = '\n'.join([element for element in summary_list])  # 沒分段

        # 解析信息列表
        info_list = html.xpath('.//ul[@class="subject-property"]/li')
        info_dict = {}
        for info_item in info_list:
            info_name = info_item.xpath('./span[@class="label"]/text()')[0].strip().strip(':')
            info_value = info_item.xpath('./span[@class="value"]/text()')[0].strip().strip(':')
            info_dict[info_name] = info_value

        # 其他电影人（不在同一个url）
        # partners = html.xpath('.//section[@id="partners"]')[0]
        # partner_herf = partners.xpath('./div[@class="partners-mod-info"]/a/@href')

        # 使用正则表达式查找 收藏夹work_collection_id 的值
        script_content = html.xpath('//div[@id="content"]/div/div/script/text()')[0]
        match = re.search(r'window\.work_collection_id\s*=\s*(\d+);', script_content)
        if match:
            collection_id = match.group(1)
            try:
                movie_count, movie_url_list = self.request_collection(collection_id)
            except Exception as e:
                logging.error('请求收藏列表失败，原因：%s', e)
                movie_count, movie_url_list = None, []
        else:
            collection_id, movie_count, movie_url_list = None, None, []
        data = [{
            'personage_code': personage_code,
            'personage_name': personage_name,
            'other_name': other_name,
            'personage_url': personage_url,
            'avatar_url': avatar_url,
            'gender': info_dict.get('性别'),
            'birth_date_str': info_dict.get('出生日期'),
            'death_date_str': info_dict.get('去世日期'),
            'birth_place': info_dict.get('出生地'),
            'alias': info_dict.get('更多外文名'),
            'family_members': info_dict.get('家庭成员'),
            'profession': info_dict.get('职业'),
            'collection_id': collection_id,
            'movie_count': movie_count,
            'summary': summary
        }]
        return {'data_dict': data, 'parse_status': True, 'parse_msg': None, 'url_list': movie_url_list}

    def transform_data(self, data_dict):
        for item in data_dict:
            # 转换日期格式
            try:
                item['birth_date'] = datetime.datetime.strptime(item['birth_date_str'], '%Y年%m月%d日')
            except Exception:
                item['birth_date'] = None
            try:
                item['death_date'] = datetime.datetime.strptime(item['death_date_str'], '%Y年%m月%d日')
            except Exception:
                item['death_date'] = None
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