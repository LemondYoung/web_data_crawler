#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：hr_hedge_fund_data_sync -> system_
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/12/7 16:24
@Desc   ：
==================================================
"""
import os
import platform


# 获取当前系统版本
def get_cur_system():
    c = platform.system()
    return c


# 执行cmd命令
def execute_cmd(command=None):
    result = os.system(command)
    print('执行结果:', result)
    return result

if __name__ == '__main__':
    print(get_cur_system())