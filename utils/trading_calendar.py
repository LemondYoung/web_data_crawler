#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 11:09
# @Author  : Yang
# @File    : trading_calendar.py
# @Software: PyCharm
import datetime, logging
import time

import pandas as pd
from functools import lru_cache


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        # print(b_date + day*i)
        yield b_date + day*i


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






# 判断今天是否为工作日
def is_week_day(date=None):
    if date:
        date = datetime.datetime.strptime(date, '%Y%m%d')
    else:
        date = datetime.datetime.now()
    # 假如今天是周日
    week_day = date.weekday()
    # 如果今天是周日，则返回True
    if week_day in [0, 1, 2, 3, 4]:
        return True
    else:
        return False


# 两个日期之间的差（多格式）
def get_date_interval(begin_date, end_date=None, unit='d', is_int=False):
    """
    :param begin_date: 20210101
    :param end_date: 20220101
    :param unit: 间隔单位，['d', 'm', 'y', 'ymd'] 年 月 日 年月日
    :param is_int: 是否取整数，【True：四舍五入，False：保留两位小数】
    """
    if end_date is None:
        end_date = datetime.datetime.strftime(datetime.datetime.today(), '%y%m%d')
    if isinstance(str(begin_date), str) and isinstance(str(end_date), str):
        if begin_date > end_date:
            logging.error('开始日期不能大于结束日期，begin_date:%s，end_date:%s', begin_date, end_date)
            return False
        begin_date_ = datetime.datetime.strptime(str(begin_date), '%Y%m%d')
        end_date_ = datetime.datetime.strptime(str(end_date), '%Y%m%d')
        year_interval = end_date_.year - begin_date_.year
        month_interval = end_date_.month - begin_date_.month
        day_interval = end_date_.day - begin_date_.day
        if unit == 'ymd':
            return {'year_interval': year_interval, 'month_interval': month_interval, 'day_interval': day_interval,}
        elif unit == 'y':
            month_to_year = month_interval/12
            day_to_year = day_interval/365
            year_interval_all = round(year_interval + month_to_year + day_to_year) if is_int is True else round(year_interval + month_to_year + day_to_year, 2)
            return {'year_interval': year_interval_all}
        elif unit == 'm':
            year_to_month = year_interval*12
            day_to_month = day_interval / 30
            month_interval_all = round(year_to_month + month_interval + day_to_month) if is_int is True else round(year_to_month + month_interval + day_to_month, 2)
            return {'month_interval': month_interval_all}
        elif unit == 'd':
            day_interval_all = (end_date_ - begin_date_).days
            return {'day_interval': day_interval_all}
    else:
        logging.error('开始结束日期类型错误，begin_date:%s，end_date:%s', type(begin_date), type(end_date))
        return None


# 两个日期小时之间的差（多格式）
def get_date_time_interval(begin_date, end_date, begin_time, end_time, unit='h', is_int=False):
    """
    :param begin_date: 20210101
    :param end_date: 20220101
    :param unit: 间隔单位，['d', 'm', 'y', 'ymd'] 年 月 日 年月日
    :param is_int: 是否取整数，【True：四舍五入，False：保留两位小数】
    """
    # if end_date is None:
    #     end_date = datetime.datetime.strftime(datetime.datetime.today(), '%y%m%d')
    if isinstance(begin_date, str) and isinstance(end_date, str) and isinstance(begin_time, str) and isinstance(end_time, str):
        if begin_date > end_date:
            logging.error('开始日期不能大于结束日期，begin_date:%s，end_date:%s', begin_date, end_date)
            return False
        begin_date_ = datetime.datetime.strptime(begin_date+begin_time, '%Y%m%d%H%M%S')
        end_date_ = datetime.datetime.strptime(end_date+end_time, '%Y%m%d%H%M%S')
        day_interval = end_date_.day - begin_date_.day
        hour_interval = end_date_.hour - begin_date_.hour
        if unit == 'dh':
            if hour_interval < 0:
                day_interval = day_interval - 1
                hour_interval = hour_interval + 24
            return {'day_interval': day_interval, 'hour_interval': hour_interval,}
        elif unit == 'h':
            hour_interval_all = (end_date_ - begin_date_).seconds / 3600 + (end_date_ - begin_date_).days * 24
            hour_interval = int(hour_interval_all) if is_int else round(hour_interval_all, 2)
            return {'hour_interval': hour_interval}
    else:
        logging.error('开始结束日期类型错误，begin_date:%s，end_date:%s', type(begin_date), type(end_date))
        return None


# 获取季度list
def get_quarter_list(begin_date='20200101', end_date=None, order='asc', quarter_type='quarter', limit=None):
    """
    获取季度日期的列表
    @param begin_date:
    @param end_date:
    @param order:
    @param quarter_type: 默认quarter代表一年的四个季度日期，half_year代表半年度的日期，not_half_year代表一季度和三季度，year年度
    @param limit:
    @return:
    """
    if quarter_type == 'half_year':
        quarter_list = ['0630', '1231']
    elif quarter_type == 'not_half_year':
        quarter_list = ['0331', '0930']
    elif quarter_type == 'year':
        quarter_list = ['1231']
    else:
        quarter_list = ['0331', '0630', '0930', '1231']
    date_list = get_stable_date_list(start_date=begin_date, end_date=end_date, order='asc', return_type='list')
    quarter_date_list = []
    for date in date_list:
        if date[4:8] in quarter_list:
            quarter_date_list.append(date)
    if order == 'desc':
        quarter_date_list.reverse()
    if limit:
        return quarter_date_list[:limit]
    return quarter_date_list


# 封装一些日期
now_hour = datetime.datetime.now().hour
today = datetime.datetime.now().strftime("%Y%m%d")
yesterday = (datetime.datetime.strptime(today, '%Y%m%d') - datetime.timedelta(days=1)).strftime('%Y%m%d')


if __name__ == '__main__':
    import pandas as pd
    # begin_date = None
    # data = [{'trading_day': '20210726', 'pre_trading_day': '20210723'},
    #         {'trading_day': '20210727', 'pre_trading_day': '20210726'},
    #         {'trading_day': '20120702', 'pre_trading_day': '20120630'},]
    # df = pd.DataFrame(data, columns=['trading_day', 'pre_trading_day'])
    #
    # print(get_interval_trading_days(begin_date=df['trading_day'], end_date=df['pre_trading_day']))

    # print(get_lately_trading_day(get_pre_day('20220112', n=365)))
    # print(get_lately_trading_day(get_pre_day('20220112', n=7)))
    dd = get_month_list()
    # print(get_date_interval(begin_date='20200101', end_date='20210203', unit='m', is_int=False))
    # print(split_date_time(begin_date='20211020', end_date='20211020', begin_time='220000', end_time='001959'))
    # print(get_date_time_interval(begin_date='20211020', end_date='20211020', begin_time='030000', end_time='071959', unit='h', is_int=True))
    # dd = split_date_time(begin_date='20211207', begin_time='240000', end_date='20211208', end_time='010000')
    # dd = solar_and_lunar('19970313', calendar_type='solar')
    # dd = get_quarter_list(order='desc', limit=2)
    dd = get_pre_day('20230822', 7)
    print(dd)

