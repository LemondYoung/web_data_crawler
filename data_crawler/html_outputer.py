#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> html_outputer
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/23 13:20
@Desc   ：
==================================================
"""


import logging

from config import db_map
from constants import *


mode_map = {
    STORE_DATA_REPLACE: 'REPLACE',
    STORE_DATA_UPDATE: 'UPDATE',
    STORE_DATA_INSERT: 'INSERT',
    STORE_DATA_DELETE_INSERT: 'DELETE-INSERT',
    STORE_DATA_TRUNCATE_INSERT: 'TRUNCATE-INSERT',
}
ignore_log_table = ['s_url_manager']


class HtmlOutput(object):

    def __init__(self, table_name=None):
        self.table_name = table_name
        self.target_db = 'weibo_data'
        self.save_mode = STORE_DATA_UPDATE

    def save_table_data(self, table_name, records, date=None, mode=STORE_DATA_REPLACE, target_db_name='weibo_data', delete_info=None):
        if not table_name:
            return 0, None
        db = db_map[target_db_name]
        if table_name not in ignore_log_table:
            logging.debug('保存数据，目标数据库为%s，入库模式为%s', target_db_name, mode_map.get(mode))
        if mode == STORE_DATA_REPLACE:
            result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.REPLACE_MODE)
        elif mode == STORE_DATA_UPDATE:
            result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.UPDATE_MODE)
        elif mode == STORE_DATA_INSERT:
            result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE)
        elif mode == STORE_DATA_DELETE_INSERT:
            result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE, delete_info=delete_info)
        elif mode == STORE_DATA_TRUNCATE_INSERT:
            result, result_data = db.records_to_db(table_name=table_name, records=records, mode=db.INSERT_MODE, delete_info='truncate')
        else:
            raise ValueError('数据入库模式错误，%s' % mode)
        # 保存状态
        return result, result_data

    def save_data(self, data_dict):
        if self.table_name is None:
            logging.info('目标表为空，不保存数据')
            return True, None
        result, result_data = self.save_table_data(self.table_name, records=data_dict, target_db_name=self.target_db, mode=self.save_mode)
        if result is False or result is None:
            _ = {'length': len(data_dict), 'result_length': None, 'result_data': result_data}
            return [False, _]
        else:
            logging.info('计划执行数据量%s，已执行数据量为%s', len(data_dict), result)
            _ = {'length': len(data_dict), 'result_length': result, 'result_data': result_data}
            return [True, _]