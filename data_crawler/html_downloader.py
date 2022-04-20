#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> html_downloader
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:20
@Desc   ：
==================================================
"""
import logging

import requests


class HtmlDownloader(object):

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            # 'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
        }

        self.return_type = 'obj'

    def request_data(self, url, connect_time=10, read_time=10, headers_dict=None):
        if headers_dict and len(headers_dict) > 0:
            for k, v in headers_dict.items():
                self.headers[k] = v

        logging.info('请求的url为：%s', url)
        response = self.__request(url, connect_time, read_time)
        status_code = response.status_code
        if status_code != 200:
            logging.error('网页获取失败,%s', status_code)
            return False
        response.encoding = 'utf-8'
        html = response.text
        return html

    def __request(self, url, connect_time=10, read_time=10):
        response = requests.get(url, headers=self.headers, timeout=(connect_time, read_time), allow_redirects=False)
        response.encoding = 'utf-8'
        return response


