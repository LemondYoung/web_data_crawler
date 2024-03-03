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

from settings import db_map
from constants import *

mode_map = {
    STORE_DATA_REPLACE: 'REPLACE',
    STORE_DATA_INSERT_UPDATE: 'UPDATE-DUPLICATE',
    STORE_DATA_UPDATE: 'UPDATE',
    STORE_DATA_INSERT: 'INSERT',
    STORE_DATA_DELETE_INSERT: 'DELETE-INSERT',
    STORE_DATA_TRUNCATE_INSERT: 'TRUNCATE-INSERT',
}
ignore_log_table = []


# 保存数据
def save_table_data(table_name, records, mode=STORE_DATA_REPLACE, db_name='weibo_data', delete_info=None,
                    update_conditions: list = None):
    """
    :param table_name: 目标数据库
    :param records: 数据集
    :param mode: 模式（可选项如下）
    :param db_name: 目标数据库
    :param delete_info: 删除语句
    :param update_conditions: 更新条件
    :return:
    """
    if not table_name:
        print(f'数据库为空：{db_name}')
        return 0, None
    db = db_map[db_name]
    if table_name not in ignore_log_table:
        logging.debug('保存数据，目标数据库为%s，入库模式为%s', db_name, mode_map.get(mode))
    if mode == STORE_DATA_REPLACE:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.REPLACE_MODE)
    elif mode == STORE_DATA_INSERT_UPDATE:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_UPDATE_MODE)
    elif mode == STORE_DATA_UPDATE:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.UPDATE_MODE,
                                               update_conditions=update_conditions)
    elif mode == STORE_DATA_INSERT:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE)
    elif mode == STORE_DATA_DELETE_INSERT:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE,
                                               delete_info=delete_info)
    elif mode == STORE_DATA_TRUNCATE_INSERT:
        result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE,
                                               delete_info='truncate')
    else:
        raise ValueError('数据入库模式错误，%s' % mode)
    # 保存状态
    return result, result_data