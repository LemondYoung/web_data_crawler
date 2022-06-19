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


# COOKIE = 'SUB=_2AkMWwS-1f8NxqwJRmP0WzGvlaIp_zQjEieKgnd5uJRMxHRl-yT9jqksYtRB6PUEBWjps0Sn6yBV4hdOK6owNynFCQQk-; XSRF-TOKEN=eX0JwM8DrpXvTihmg2-Ql5G_; _s_tentry=weibo.com; Apache=4086897996618.5015.1650446838318; SINAGLOBAL=4086897996618.5015.1650446838318; ULV=1650446838495:1:1:1:4086897996618.5015.1650446838318:; WBPSESS=a_YZA6I5qCR3U8i3Rfvlpv0zOZgTGkDCBD-68HjaqHKRQfuQc9Swji5AekjUgViFEzFEQARBJVpLv1K8nhMdAEUH_txBp-q9De5lBq2rphHP36d6s6Nj7s9ivN0NSldQTXyfEVJFwe5kYcRMVzhhjpwZut4nfevowe0qTNhxJps='
COOKIE = 'Hm_lvt_af1fda4748dacbd3ee2e3a69c3496570=1654526730; Hm_lpvt_af1fda4748dacbd3ee2e3a69c3496570=1654527540; TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTQ1NDYxMjksImp0aSI6IjMzNDkwNSIsImlzcyI6IjE3OCoqKioxOTM5In0.QnhLLQbysQRKqUIWvolvvjZQwSwzHXAMW1sh6KduTyQ'
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

db_map = {
    'weibo_data': Mysql(**WEIBO_DB_CONFIG),
    'douban_data': Mysql(**DOUBAN_DB_CONFIG),
    'bilibili_data': Mysql(**BILIBILI_DB_CONFIG),
}