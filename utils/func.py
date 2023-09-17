#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：hr_hedge_fund_data_sync -> func
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/11/16 15:46
@Desc   ：
==================================================
"""

# 获取函数信息
import inspect
import logging
import os
import sys


# 获取函数信息
def get_func_info(func):
    """
    : return: 函数名称func_name, 函数模块func_module, 函数参数func_param, 绝对路径func_abs_path, 注释func_doc
    """
    if not callable(func):
        logging.warning('%s非可执行函数，无法查看信息', func)
        return None
    code_line = inspect.getsource(func).split("\n")
    index = 0
    for index, code in enumerate(code_line):
        if code.startswith("def "):
            break
    source_code = "\n".join(code_line[index:])
    func_doc = paser_func_doc(func.__doc__)
    info = {
        'func_name': func.__name__,
        'func_intro': func_doc['func_intro'],  # 函数介绍
        'func_desc': func_doc['func_desc'],  # 函数注释
        'func_return': func_doc['func_return'],
        'func_module': func.__module__,
        'func_param': str(inspect.signature(func)),  # 函数参数
        'func_abs_path': os.path.abspath(inspect.getfile(func)),  # 绝对路径
        'parent_func_name': sys._getframe(1).f_code.co_name,  # 上层函数
        'source_code': source_code,  # 代码内容
        'source_path': func.__code__.co_filename.replace("\\", "/"),
    }
    return info


# 测试函数
def a(age, name='path'):
    """ 获取利率
    获取利率.....
    :param return_type: 返回类型
    :param return_value: 返回值
    :return: 番薯
    """
    pass


# 解析函数的注释
def paser_func_doc(doc):
    doc_list = doc.split('\n') if doc and isinstance(doc, str) else []
    doc_dict = {
        'func_intro': '未命名函数',  # 函数名称
        'func_desc': '',  # 函数注释
        'func_param': [],  # 函数参数
        'func_return': '',  # 返回返回结果
    }
    for index, d in enumerate(doc_list):
        d = d.strip(' ')
        try:
            if index == 0:
                doc_dict['func_intro'] = d if '@param' not in d and '@return' not in d else '未命名函数'
            elif index == 1 and '@param' not in d and '@return' not in d and ':param' not in d and ':return' not in d:
                doc_dict['func_desc'] = d
            elif '@param' in d or ':param' in d:
                doc_dict['func_param'].append(d.replace('@param', '').replace(':param', '').strip(' :'))
            elif '@return' in d or ':return' in d:
                doc_dict['func_return'] = d.replace('@return', '').replace(':return', '').strip(' :')
        except Exception as e:
            logging.debug('函数注释解析失败, %s', e)
            continue
    return doc_dict


# 参数检查（功能太具体了，不太适合在这抽象，后续想想怎么处理）
def check_param(rule, code, name):
    """
    参数检查，需要指定规则，如果不存在该规则就警告且返回True
    @param rule: 目前实现：code_name_either_or代码名字二选一
    @return:
    """
    rules = ['code_name_either_or']
    if rule not in rules:
        logging.warning(f'{rule}规则不存在')
    elif rule == 'code_name_either_or':
        if (code and name) or (not code and not name):
            logging.error('参数检查不通过，code和name不能同时传入')
            return False
    return True


if __name__ == '__main__':

    print(get_func_info(a))
    print(paser_func_doc(a.__doc__))
