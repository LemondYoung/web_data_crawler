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
import os
from PIL import Image

import requests

from settings import IMG_PATH
from utils.widget import random_password


class HtmlDownloader(object):

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            # 'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
        }

    def request_data(self, url, connect_time=10, read_time=10, headers_dict=None, proxy=None, tunnel_dict=None):
        """
        :param url:
        :param connect_time:
        :param read_time:
        :param headers_dict: 额外的header。主要是cookie
        :param proxy: 代理ip地址
        :param tunnel_dict: 隧道配置 {"proxy": "a968.kdltps.com:15818", "user": "t12648078105036", "pwd": "6w1xbsd2"}
        :return:
        """
        if headers_dict and len(headers_dict) > 0:
            for k, v in headers_dict.items():
                self.headers[k] = v
        # 增加代理ip
        if proxy:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
        elif tunnel_dict:
            proxies = {
                "http": f"http://{tunnel_dict['user']}:{tunnel_dict['pwd']}@{tunnel_dict['proxy']}/",
                "https": f"http://{tunnel_dict['user']}:{tunnel_dict['pwd']}@{tunnel_dict['proxy']}/",
            }
        else:
            proxies = None

        logging.info('请求的url为：%s', url)
        try:
            response = self.__request(url, connect_time, read_time, proxies=proxies)
        except Exception as e:
            logging.error('网页获取失败:%s', e)
            return False
        status_code = response.status_code
        if status_code != 200:
            logging.error('网页获取失败,%s', status_code)
            return False
        response.encoding = 'utf-8'
        html = response.text
        return html

    # 请求api
    def request_api(self, url, connect_time=10, read_time=10, headers_dict=None):
        """
        :param url:
        :param connect_time:
        :param read_time:
        :param headers_dict: 额外的header。主要是cookie和其他请求头
        :return:
        """
        if headers_dict and len(headers_dict) > 0:
            for k, v in headers_dict.items():
                self.headers[k] = v

        logging.info('请求的url为：%s', url)
        response = self.__request(url, connect_time, read_time)
        status_code = response.status_code
        json_data = response.json()
        if status_code != 200:
            logging.error(f'网页获取失败:{status_code}，错误代码：{json_data.get("code")}, 信息：{json_data.get("msg")}')
            return False
        return json_data

    def __request(self, url, connect_time=10, read_time=10, proxies=None):
        response = requests.get(url, headers=self.headers, timeout=(connect_time, read_time), allow_redirects=True, proxies=proxies)
        response.encoding = 'utf-8'
        return response

    def download_img(self, img_url, img_dir_path=None, img_type='jpg', return_type='obj'):
        """
        :param img_url:
        :param img_dir_path:
        :param img_type: 图片类型
        :param return_type:
        :return:
        """
        if not img_dir_path:
            img_dir_path = IMG_PATH
        img_name = get_img_data(img_url=img_url, return_type='map', return_value='img_name').get(img_url)
        if img_name is None:
            logging.error('未获取到 %s 图片信息，请检查', img_url)
            img_name = random_password(count=28, type='uuid')
        img_path = os.path.join(img_dir_path, img_name + '.' + img_type)
        # 下载图片
        reponse = requests.get(img_url, headers=self.headers, stream=True, timeout=(60, 300))  # 连接超时60s，读取超时300s
        status_code = reponse.status_code
        if status_code != 200:
            logging.error('图片获取失败,%s', status_code)
            return False
        else:
            logging.info('图片获取成功，%s，耗时%sms', status_code, reponse.elapsed.microseconds)
        # size = reponse.size
        result = open(img_path, 'wb').write(reponse.content)  # 将内容写入图片
        logging.info("图片保存成功,地址%s, %s", img_path, result)

        # 解析图片格式
        # req = urllib.request.Request(url=img_url, headers=self.headers)
        # resp = urllib.request.urlopen(req)
        # resp = request.urlopen(img_url)
        img = Image.open(img_path)
        if return_type == 'obj':
            return img
        elif return_type == 'path':
            return img_path

    def download_video(self, url, dir_path=None, type='jpg', return_type='obj'):
        collection_source_list = ['bilibili', 'weibo']  # 待控制

    def read_local_html_file(self, file_path):
        """ 读取本地html文件 """
        file = open(file_path, 'r', encoding='utf-8')
        content = file.read()
        file.close()
        return content






if __name__ == '__main__':
    '''
    img_path 里面填图片路径,这里分两种情况讨论:
    第一种:假设你的代码跟图片是在同一个文件夹，那么只需要填文件名,例如 test1.jpg (test1.jpg 是图片文件名)
    第二种:假设你的图片全路径是 D:/img/test1.jpg ,那么你需要填 D:/img/test1.jpg
    '''
    headers_dict = {'Referer': 'http://movie.douban.com/explore'}
    # url = r'https://www.zhihu.com/api/v4/questions/585465221/feeds?cursor=d9f38bb508c45bfb520d037a2efe50d2&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1694957978758389513'
    # url = r'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=300&count=20&uncollect=false&selected_categories={"类型":"惊悚"}&uncollect=false&tags="惊悚"&ck=-uwX'
    # URL = 'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=160&count=20&selected_categories=%7B%22%E7%B1%BB%E5%9E%8B%22:%22%E8%A5%BF%E9%83%A8%22%7D&uncollect=false&tags=%E8%A5%BF%E9%83%A8&ck=-uwX'
    url = 'https://movie.douban.com/subject/3604148/'
    # html = HtmlDownloader().request_api(url, headers_dict=headers_dict)
    # html = HtmlDownloader().request_data(url)
    html = HtmlDownloader().request_data(url, tunnel_dict={"proxy": "a968.kdltps.com:15818", "user": "t12648078105036", "pwd": "6w1xbsd2"})
    # html = HtmlDownloader().read_local_html_file(r"D:\app\pycharm\project\data_crawler\web_data_crawler\data\html\douban\user_251679774.html")
    print(1)