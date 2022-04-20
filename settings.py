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

COOKIE = 'SUB=_2AkMWwS-1f8NxqwJRmP0WzGvlaIp_zQjEieKgnd5uJRMxHRl-yT9jqksYtRB6PUEBWjps0Sn6yBV4hdOK6owNynFCQQk-; XSRF-TOKEN=eX0JwM8DrpXvTihmg2-Ql5G_; _s_tentry=weibo.com; Apache=4086897996618.5015.1650446838318; SINAGLOBAL=4086897996618.5015.1650446838318; ULV=1650446838495:1:1:1:4086897996618.5015.1650446838318:; WBPSESS=a_YZA6I5qCR3U8i3Rfvlpv0zOZgTGkDCBD-68HjaqHKRQfuQc9Swji5AekjUgViFEzFEQARBJVpLv1K8nhMdAEUH_txBp-q9De5lBq2rphHP36d6s6Nj7s9ivN0NSldQTXyfEVJFwe5kYcRMVzhhjpwZut4nfevowe0qTNhxJps='

WEIBO_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'weibo_data',
}