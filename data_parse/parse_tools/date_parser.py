#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> date_parser
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/18 15:44
@Desc   ：
==================================================
"""


def standardize_date(date, separator=''):
    """
    example: ['2021-01-01', '2021年5月11', '2021/5/11', '2021\\5\\11', '2020505', '20210511'] -> ['20210511', '20210511', '20210511', False, False, '20210511']
    :param date:
    :param separator: 返回日期的字符间隔
    :return:
    """
    import re
    date_separator = ['-', '年', '月', '/']
    if separator not in ('', '-', '/'):
        return False
    date_intersection = list(set(list(date)) & set(date_separator))  # 取日期所有字符 和 匹配列表的 交集
    date = date.strip(' ')
    if len(date_intersection) > 0:  # 有交集
        date_str = re.split('|'.join(date_separator), date)
        if len(date_str) == 3 and len(date_str[0]) == 4:  # 以年为开头，且年月日顺序齐全，否则不支持
            year = date_str[0]
            month = date_str[1].zfill(2)
            day = date_str[2][0:2].zfill(2)
            new_date = year+separator+month+separator+day
        else:  # 其他乱序格式，错误
            return False
    elif len(date) == 8:  # 无分隔符交集，且日期8位，直接返回
        new_date = date[0:4] + separator + date[4:6] + separator + date[6:8]
    elif len(date) > 8:  # 无分隔符交集，且日期大于8位，返回8位日期
        mat = re.search(r"19|20\d{6}", date)
        if mat:
            new_date = mat.group()
        else:
            return False
    else:  # 无分隔符交集，且日期不为8位，错误
        return False
    return new_date



if __name__ == '__main__':
    a = ['2021-01-01', '2021年5月11', '2021/5/11', '2021\\5\\11', '东城攻略_1210511', '20210511']
    for date in a:
        result = standardize_date(date, separator='')
        print(result)