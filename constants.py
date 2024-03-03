#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> constants
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/18 15:56
@Desc   ：
==================================================
"""

STORE_DATA_DELETE = 1001  # 删除
STORE_DATA_REPLACE = 1002  # 增量 使用唯一主键防止重复
STORE_DATA_INSERT_UPDATE = 1003  # 使用唯一主键更新数据
STORE_DATA_UPDATE = 1004  # 纯更新
STORE_DATA_INSERT = 1005  # 插入数据
STORE_DATA_DELETE_INSERT = 1006  # 刪除后插入数据
STORE_DATA_TRUNCATE_INSERT = 1007  # 清空后插入数据



