#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> settings
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/18 15:55
@Desc   ：
==================================================
"""
import os

from utils.database.mysql import Mysql

PROJECT_NAME = 'web_data_crawler'
CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = CUR_PATH[:CUR_PATH.find(PROJECT_NAME) + len(PROJECT_NAME)]

IMG_PATH = os.path.join(ROOT_PATH, 'src', 'imgs')
FONT_PATH = os.path.join(ROOT_PATH, 'src', 'fonts')
DATA_PATH = os.path.join(ROOT_PATH, 'data')
HTML_DATA_PATH = os.path.join(DATA_PATH, 'html')
JSON_PATH = os.path.join(DATA_PATH, 'json')

# COOKIE = 'SUB=_2AkMWwS-1f8NxqwJRmP0WzGvlaIp_zQjEieKgnd5uJRMxHRl-yT9jqksYtRB6PUEBWjps0Sn6yBV4hdOK6owNynFCQQk-; XSRF-TOKEN=eX0JwM8DrpXvTihmg2-Ql5G_; _s_tentry=weibo.com; Apache=4086897996618.5015.1650446838318; SINAGLOBAL=4086897996618.5015.1650446838318; ULV=1650446838495:1:1:1:4086897996618.5015.1650446838318:; WBPSESS=a_YZA6I5qCR3U8i3Rfvlpv0zOZgTGkDCBD-68HjaqHKRQfuQc9Swji5AekjUgViFEzFEQARBJVpLv1K8nhMdAEUH_txBp-q9De5lBq2rphHP36d6s6Nj7s9ivN0NSldQTXyfEVJFwe5kYcRMVzhhjpwZut4nfevowe0qTNhxJps='
COOKIE = 'll="118318"; bid=d3wETblY2eg; _pk_id.100001.4cf6=49ed6c383ad14acf.1694851976.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.358396531.1694851978.1694851978.1694851978.1; __utmb=30149280.0.10.1694851978; __utmc=30149280; __utmz=30149280.1694851978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.831957860.1694851978.1694851978.1694851978.1; __utmb=223695111.0.10.1694851978; __utmc=223695111; __utmz=223695111.1694851978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
# DOUBAN_COOKIE = 'viewed="27107671"; bid=XqUJXdtYIjQ; __utmz=30149280.1724492430.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=30149280; ll="118327"; _pk_id.100001.8cb4=18dcf6f213bd5bc6.1725694332.; ap_v=0,6.0; __utma=30149280.1122461522.1724492430.1725697088.1725703800.4; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1725705772%2C%22https%3A%2F%2Fmovie.douban.com%2Fpeople%2FLion1874%2Fcollect%3Fstart%3D45%26sort%3Dtime%26rating%3Dall%26mode%3Dgrid%26type%3Dall%26filter%3Dall%22%5D; _pk_ses.100001.8cb4=1; dbcl2="251679774:OG7XL9wVPYA"; ck=-uwX; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25167; ct=y; __utmt=1; __utmb=30149280.26.10.1725703800'
DOUBAN_COOKIE = 'viewed="27107671"; bid=XqUJXdtYIjQ; _pk_id.100001.4cf6=ca03d43f954136ba.1725694237.; ll="118327"; __yadk_uid=61ry0EgqQki3VSITNtYyatckqPPYAnD7; _vwo_uuid_v2=DE12EEEF8DDB114C3712D7255F362B6D1|735fa241e9d34d805c543ca5a30e417c; dbcl2="251679774:OG7XL9wVPYA"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25167; ct=y; ck=-uwX; __utmc=30149280; __utmc=223695111; frodotk_db="2d8329cf5ba79fdf88897d6e12f6df9d"; __utmz=30149280.1726904819.17.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/explore; __utmz=223695111.1726916004.19.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/personage/27259353/creations; __utma=30149280.1122461522.1724492430.1726919507.1726930803.21; __utmb=30149280.2.10.1726930803; __utma=223695111.1090629521.1725694241.1726919603.1726930947.21; __utmb=223695111.0.10.1726930947; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1726930947%2C%22https%3A%2F%2Fwww.douban.com%2Fpersonage%2F27259353%2Fcreations%3Ftype%3Dfilmmaker%26start%3D10%26sortby%3Dcollection%26role%3D%26format%3Dpic%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0'
# TOKEN = ''

main_host = None

WEIBO_DB_CONFIG = {
    'host': main_host or 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'weibo_data',
}

DOUBAN_DB_CONFIG = {
    'host': main_host or 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'douban_data',
}

BILIBILI_DB_CONFIG = {
    'host': main_host or 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'bilibili_data',
}

KNOWLEDGE_DB_CONFIG = {
    'host': main_host or 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'knowledge_data',
}

ZHIHU_DB_CONFIG = {
    'host': main_host or 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'zhihu_data',
}

db_map = {
    'weibo_data': Mysql(**WEIBO_DB_CONFIG),
    'douban_data': Mysql(**DOUBAN_DB_CONFIG),
    'bilibili_data': Mysql(**BILIBILI_DB_CONFIG),
    'knowledge_data': Mysql(**KNOWLEDGE_DB_CONFIG),
    'zhihu_data': Mysql(**ZHIHU_DB_CONFIG),
}