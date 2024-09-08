# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@desc: url统计
@author: yang li peng
@file: url_summary.py
@time: 2024/9/8
@info:
"""
from constants import STORE_DATA_REPLACE
from data_sync.data_load.mysql_data_load import save_table_data
from settings import db_map


def get_url_summary(db_name):
    sql = """
    select url_type, url_status, count(1) as count
    from s_url_manager
    group by url_type, url_status
    order by url_type, url_status
    """
    data = db_map.get(db_name).query(sql)
    return data


if __name__ == '__main__':
    db_name = 'douban_data'
    summary_data = get_url_summary(db_name)
    save_table_data('s_url_summary', summary_data, mode=STORE_DATA_REPLACE, db_name=db_name)