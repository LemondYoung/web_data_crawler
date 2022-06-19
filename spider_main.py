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
import random
import time

from config import parser_map
from data_crawler.html_downloader import HtmlDownloader
from data_crawler.html_outputer import HtmlOutput
from data_crawler.url_manager import UrlManager, get_urls
from data_sync.data_extract.weibo_data import get_poetry_img
from settings import COOKIE
from utils.computer.dir import Dir

from utils.log import InterceptHandler




class spiderMain(object):
    def __init__(self):
        self.urlManager = UrlManager()  # 管理器
        self.htmlDownloader = HtmlDownloader()  # 下载器

    def split_urls(self, url_list, strategy="random"):
        new_url_list = []
        index = 0
        while index < len(url_list):
            num = random.randint(7, 12)
            sub_list = url_list[index: index + num]
            new_url_list.append({'sleep': num, 'count': num, 'urls': sub_list})
            index += num
        return new_url_list

    # 运行爬虫
    def run_crawler(self, parser_type=None, urls_list: list = None, download_type='text', is_strategy=False, **kwargs):
        if is_strategy:
            # 设置间隔策略
            logging.info('获取到url总数%s，开始设置策略', len(urls_list))
            new_url_list = self.split_urls(url_list=urls_list, strategy="random")
            logging.warning('策略分配成功，共分为%s组', len(new_url_list))
        else:
            new_url_list = urls_list

        # 开始爬虫
        index = 1
        logging.warning('当前策略分组%s组', len(new_url_list))
        for urls_obj in new_url_list:  # 按爬取策略分类

            if isinstance(urls_obj, dict):
                sub_url_list = urls_obj.get('urls')
                sleep = urls_obj.get('sleep')

                logging.info('%s', '*'*110)
                logging.info('%s此次爬取%s条，间隔%ss%s', '*'*50, urls_obj.get('count'), sleep, '*'*50,)
                logging.info('%s', '*'*110)
                time.sleep(sleep)
            elif isinstance(urls_obj, list):
                sub_url_list = urls_obj
            elif isinstance(urls_obj, str):
                sub_url_list = [urls_obj]
            else:
                logging.info('urls格式有误，%s', urls_obj)
                return False

            for url in sub_url_list:  # 内层分类
                time.sleep(1)
                logging.warning('%s当前url进度[%s/%s]%s', '*'*40, index, len(sub_url_list) * len(new_url_list), '*'*40)
                index += 1
                # 下载器下载数据
                logging.info('[2.1]、开始下载网页，当前下载类型%s', download_type)
                if download_type == 'text':
                    html = self.htmlDownloader.request_data(url, headers_dict={'cookie': COOKIE})
                    if html is False:
                        logging.error('网页下载失败，跳过')
                        logging.warning(url)
                        continue
                elif download_type == 'img_url':
                    logging.info('要下载的图片url=%s', url)
                    html = self.htmlDownloader.download_img(img_url=url, return_type='path')
                    if html is False:
                        logging.error('下载图片失败')
                        continue
                    logging.info('保存图片成功')
                elif download_type == 'img_path':
                    html = url
                # 解析器解析数据
                logging.info('[2.2]、开始解析数据，当前解析类型%s', parser_type)
                cur_parser = parser_map.get(parser_type)
                logging.info('当前解析器为%s', cur_parser.__class__.__name__)
                data_dict = cur_parser.run_parser(html=html, url=url, parser_type=parser_type, **kwargs)
                result = data_dict['result']
                data_list = data_dict['data_list']
                if result:
                    # 保存数据
                    logging.info('[2.2]、解析数据成功')
                    logging.info('[2.3]、开始保存数据')
                    for j, table_data in enumerate(data_list, 1):
                        table_name = table_data['table_name']
                        data = table_data['data']
                        logging.info('[2.3.%s]、目标表%s', table_name, j)
                        if table_name == 's_url_manager':
                            logging.info('保存url，个数%s', len(data) if data else None)
                            add_result = UrlManager().add_url(url_data=data)
                        else:
                            save_result, msg_dict = HtmlOutput(table_name=table_name).save_data(data)
                    UrlManager().update_url(url=url, result=result)
                    logging.info('[2.3]、保存data成功，数量%s', len(data_list) if data_list else None)
                else:
                    logging.error('[2.2]、解析数据失败')
                    UrlManager().update_url(url=url, result=False)


    def run(self, parser_type, urls: list = None, style='academic-art', **kwargs):
        logging.info('解析类型为%s', parser_type)
        if parser_type == 'img_url':
            urls = get_urls(url_type='img', style_code='original', return_type='list', type='add') if not urls or len(urls) == 0 else urls
            self.run_crawler(parser_type=parser_type, urls_list=urls, style=style, download_type=parser_type, **kwargs)
        if parser_type == 'img_path':
            self.run_crawler(parser_type=parser_type, urls_list=urls, style=style, download_type=parser_type, **kwargs)
        else:
            urls = get_urls(url_type='blog', style_code=None, return_type='list', type='add') if not urls or len(urls) == 0 else urls
            self.run_crawler(parser_type=parser_type, urls_list=urls, style=style, **kwargs)




if __name__ == '__main__':
    logging.basicConfig(handlers=[InterceptHandler('spider_url.log')], level=logging.INFO)

    # splider.run_crawler()
    # get_url_list(object_type='user_movie', object_value='', step=20, count=100, status=None, sort='time')
    # urls = splider.get_url_list(object_type='user_movie', object_value='Lion1874', step=10, count=2000, status='P', sort='time')

    # 获取风格的page_url
    style = 'realism'
    url_list = ['https://weibo.com/ajax/statuses/mymblog?uid=2100623570&page=5']
    # url_list = get_poetry_img(content='快来看看最打动你的作品是哪首', return_type='list')
    dir_path = r'D:\software\pycharm\project\data_sync\web_data_crawler\src\tmp'
    new_dir_path = r'D:\software\pycharm\project\data_sync\web_data_crawler\src\imgs'
    url_list = Dir(dir_path).find_files()
    # url_list = get_urls(url_type='img_url', return_type='list')
    spiderMain().run(parser_type='img_path', urls=url_list, style=style, dir_path=new_dir_path)


