#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> mysql_data_load
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/18 15:53
@Desc   ：
==================================================
"""

import logging

from constants import *
from utils.database.mysql import MySql
from settings import DOUBAN_DB_CONFIG

douban_db = MySql(**DOUBAN_DB_CONFIG)


# 保存数据
def save_table_data(table_name, records, date=None, mode=STORE_DATA_REPLACE, target_db_name='douban_db', delete_info=None):
    if target_db_name == 'douban_db':
        db = douban_db
    else:
        raise ValueError('数据库错误')
    logging.warning('目标数据库为%s', target_db_name)
    if mode == STORE_DATA_REPLACE:
        logging.info('当前入库模式为 REPLACE')
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.REPLACE_MODE)
    elif mode == STORE_DATA_UPDATE:
        logging.info('当前入库模式为 UPDATE')
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.UPDATE_MODE)
    elif mode == STORE_DATA_INSERT:
        logging.info('当前入库模式为 INSERT')
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE)
    elif mode == STORE_DATA_DELETE_INSERT:
        logging.info('当前入库模式为 DELETE-INSERT')
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE, delete_info=delete_info)
    elif mode == STORE_DATA_TRUNCATE_INSERT:
        logging.info('当前入库模式为 TRUNCATE-INSERT')
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE, delete_info='truncate')
    else:
        raise ValueError('数据入库模式错误，%s' % mode)
    # 保存状态
    return result, result_data