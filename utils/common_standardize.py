#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：hr_hedge_fund_data_sync -> common_standardize
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/9/24 10:29
@Desc   ：
==================================================
"""
import datetime
import logging
from functools import lru_cache


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    # print(day)
    for i in range(days):
        # print(b_date + day*i)
        yield b_date + day*i

# 获取全部日期列表
@lru_cache()
def get_stable_date_list(start_date=None, end_date=None, order='asc', return_type='list'):
    """
    获取日期列表(包括非交易日)（稳定版）
    @param end_date:
    @param start_date:
    @param return_type:
    """
    if start_date is None:
        start = datetime.datetime.now()
    else:
        start = datetime.datetime.strptime(start_date, "%Y%m%d")
    if end_date is None:
        end = datetime.datetime.now()
    else:
        end = datetime.datetime.strptime(end_date, "%Y%m%d")
    data = []
    if return_type == 'dict':
        for d in gen_dates(start, ((end-start).days + 1)):    # 29 + 1
            # print(d)   # datetime.datetime  类型
            data.append({'date': d.strftime("%Y%m%d")})
    else:
        for d in gen_dates(start, ((end-start).days + 1)):    # 29 + 1
            # print(d)   # datetime.datetime  类型
            data.append(d.strftime("%Y%m%d"))
        if order == 'desc':
            data.reverse()
    return data



def standardize_date(date, param_separator='', return_separator=''):
    """
    example: ['2021-01-01', '2021年5月11', '2021/5/11', '2021\\5\\11', '2020505', '20210511'] -> ['20210511', '20210511', '20210511', False, False, '20210511']
    :param date:
    :param param_separator: 参数日期间隔符号
    :param return_separator: 返回日期间隔符号
    :return:
    """
    import re
    date_separator = ['-', '年', '月', '/']
    if param_separator not in ('', '-', '/') or return_separator not in ('', '-', '/'):
        return False
    date_intersection = list(set(param_separator) & set(date_separator))  # 取日期所有字符 和 匹配列表的 交集
    if len(date_intersection) > 0:  # 有交集
        date_str = re.split('|'.join(date_separator), date)
        if len(date_str) == 3 and len(date_str[0]) == 4:  # 以年为开头，且年月日顺序齐全，否则不支持
            year = date_str[0]
            month = date_str[1].zfill(2)
            day = date_str[2][0:2].zfill(2)
            new_date = year+return_separator+month+return_separator+day
        else:  # 其他乱序格式，错误
            return False
    elif len(date) == 8:  # 无分隔符交集，且日期8位，直接返回
        new_date = date[0:4] + return_separator + date[4:6] + return_separator + date[6:8]
    elif len(date) > 8:  # 无分隔符交集，且日期大于8位，返回8位日期
        mat = re.search(r"19|20\d{6}", date)
        if mat:
            new_date = mat.group()
        else:
            return False
    else:  # 无分隔符交集，且日期不为8位，错误
        return False
    if new_date not in get_date_list():
        logging.error('日期取值错误')
        return False
    return new_date