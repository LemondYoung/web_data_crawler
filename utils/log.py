#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/23 13:28
# @Author  : Yang
# @File    : log.py
# @Software: PyCharm

import os, time
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    """
    拦截logging日志流
    """
    def __init__(self, log_path='data_sync.log'):
        super().__init__()
        if "\\" not in log_path and "/" not in log_path:
            log_path = os.path.join('logs', log_path.split('.')[0], log_path)
        dir_name = os.path.dirname(log_path)
        if dir_name and not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        # self.logger = logger.add(sink=sys.stderr, format='<level>{time:YYYY-MM-DD HH:mm:ss.SSS}</level> | <blue>{process: <5}</blue> | <level>{level: <7}</level> | [<blue>{name: <35}</blue>:<blue>{function:<20}</blue>:<blue>{line:<3}</blue>] - <level>{message}</level>')
        self.logger = logger.add(log_path, rotation="0:00", retention="10 days")  # 每天0点重建文件，文件保存10天

    def emit(self, record):
        # 获取相同的日志水平
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 从记录消息的起始位置开始寻找调用者
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


if __name__ == '__main__':
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    while True:
        logging.info('1')
        time.sleep(5)