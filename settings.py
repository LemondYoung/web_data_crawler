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
JSON_PATH = os.path.join(DATA_PATH, 'json')

# COOKIE = 'SUB=_2AkMWwS-1f8NxqwJRmP0WzGvlaIp_zQjEieKgnd5uJRMxHRl-yT9jqksYtRB6PUEBWjps0Sn6yBV4hdOK6owNynFCQQk-; XSRF-TOKEN=eX0JwM8DrpXvTihmg2-Ql5G_; _s_tentry=weibo.com; Apache=4086897996618.5015.1650446838318; SINAGLOBAL=4086897996618.5015.1650446838318; ULV=1650446838495:1:1:1:4086897996618.5015.1650446838318:; WBPSESS=a_YZA6I5qCR3U8i3Rfvlpv0zOZgTGkDCBD-68HjaqHKRQfuQc9Swji5AekjUgViFEzFEQARBJVpLv1K8nhMdAEUH_txBp-q9De5lBq2rphHP36d6s6Nj7s9ivN0NSldQTXyfEVJFwe5kYcRMVzhhjpwZut4nfevowe0qTNhxJps='
COOKIE = 'll="118318"; bid=d3wETblY2eg; _pk_id.100001.4cf6=49ed6c383ad14acf.1694851976.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.358396531.1694851978.1694851978.1694851978.1; __utmb=30149280.0.10.1694851978; __utmc=30149280; __utmz=30149280.1694851978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.831957860.1694851978.1694851978.1694851978.1; __utmb=223695111.0.10.1694851978; __utmc=223695111; __utmz=223695111.1694851978.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
# TOKEN = ''

WEIBO_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'weibo_data',
}

DOUBAN_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'douban_data',
}

BILIBILI_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'bilibili_data',
}

KNOWLEDGE_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'knowledge_data',
}

ZHIHU_DB_CONFIG = {
    'host': 'localhost',
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