#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：hr_hedge_fund_data_sync -> computer
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/9/24 10:14
@Desc   ：
==================================================
"""

import json
import logging
import os, re
import tarfile
import time, datetime

import pandas as pd
import xlrd
import openpyxl


# 文件基类
class File(object):
    """
    1、获取、判断文件类型
    2、打开文件(excel)
    3、保存文件
    """
    def __new__(cls, file_path=None, is_check_file=True):
        if is_check_file:
            if not os.path.isfile(file_path):  # 跳过非文件对象
                logging.warning('%s非文件对象', file_path)
                return False
            else:
                return object.__new__(cls)
        else:
            file = open(file_path, 'w')
            return object.__new__(cls)

    def __init__(self, file_path=None, is_check_file=True):
        self.file_path = file_path
        self.path, self.file = os.path.split(file_path)
        self.file_name, self.file_type = self.file.split('.', 1)
        self.file_type_map = {
            'xlsx': 'xls',
            'xls': 'xls',
            'docx': 'doc',
            'doc': 'doc',
            'txt': 'txt',
            'tar.gz': 'tar.gz',
            'tar': 'tar',
        }
        self.std_file_type = None

    def get_file_info(self, return_type=None):
        """
        判断文件类型，并标准化
        :param expect_file_type: 如果期望文件类型为空，则默认通过字典中所有文件类型
        :return:
        """
        file_info = {}
        logging.debug('获取文件类型')
        new_type = self.file_type_map.get(self.file_type)
        if not new_type:
            logging.error('%s文件类型错误！所有文件类型：%s', type, str(self.file_type_map.keys()))
            return False
        else:
            self.std_file_type = new_type
            file_info['file_type'] = new_type

        logging.debug('获取文件大小')
        info = os.stat(self.file_path)
        file_size = round(info.st_size / 1024, 4)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.st_ctime))
        modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.st_mtime))
        file_info['file_size'] = file_size
        file_info['create_time'] = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        file_info['modify_time'] = datetime.datetime.strptime(modify_time, "%Y-%m-%d %H:%M:%S")
        file_info['file_name'] = self.file_name

        if return_type == 'file_type':
            return file_info['file_type']
        elif return_type == 'file_size':
            return file_info['file_size']
        else:
            return file_info

    # 解压压缩包
    def unzip_file(self, zip_type='tgz'):
        zip_path = self.file_path
        if not os.path.isfile(zip_path):
            logging.error('压缩文件不存在')
            return False
        path, file = os.path.split(zip_path)
        name = file.split('.')[0]
        new_path = os.path.join(path, name)
        tar = tarfile.open(zip_path, mode="r:gz")  # "r:gz"表示 open for reading with gzip compression
        tar.extractall(path=new_path)  # 将tar.gz文件解压到temp文件夹下
        tar.close()
        return new_path

    def is_expect_file_type(self, expect_file_type=None):
        if expect_file_type == 'xls':
            if self.file_type not in ['xlsx', 'xlsm', 'xls']:
                return False
        elif expect_file_type == 'json':
            if self.file_type not in ['json']:
                return False
        elif expect_file_type == 'doc':
            if self.file_type not in ['docx', 'doc']:
                return False
        elif expect_file_type == 'txt':
            if self.file_type not in ['txt']:
                return False
        else:
            logging.error('期望文件格式错误')
            return False
        return True

    def read_excel(self):
        """打开excel文件"""
        if not self.is_expect_file_type('xls'):
            logging.info('非excel文件对象')
            return False
        try:
            excel = xlrd.open_workbook(self.file_path, encoding_override="utf-8")
            all_sheet = excel.sheets()
        except Exception as e:
            logging.info('excel文件打开失败，%s', e)
            return False

        excel_sheets = {}
        for sheet in all_sheet:
            if sheet.nrows > 1:
                logging.info("该Excel共有{0}个sheet,当前sheet名称为{1},该sheet共有{2}行,{3}列".format(len(all_sheet), sheet.name, sheet.nrows, sheet.ncols))
            else:
                logging.warning('%s有效数据为空', sheet.name)
                excel_sheets[sheet.name] = None
                continue

            first_row = sheet.row_values(0)  # 获取指定行对象
            logging.info('表行：%s', first_row)
            data = []
            for row_index in range(sheet.nrows):  # 循环打印每一行
                if row_index == 0:
                    continue
                item = sheet.row_values(row_index)
                item_dict = dict(zip(first_row, item))
                data.append(item_dict)
            excel_sheets[sheet.name] = data
        return excel_sheets

    @classmethod
    def save_excel(self, df, sheet_name='score_all'):
        file_path = r'E:\文档\财通证券\text.xlsx'
        if not os.path.exists(file_path):
            logging.info('%s不存在，重新创建', file_path)
            writer = pd.ExcelWriter(file_path)
            df.to_excel(writer, sheet_name=sheet_name)
            writer.save()
            writer.close()
        else:
            try:
                logging.warning('%s已存在，开始追加%s', file_path, sheet_name)
                writer = pd.ExcelWriter(file_path)
                book = openpyxl.load_workbook(file_path)
                writer.book = book
                df.to_excel(writer, sheet_name=sheet_name)
                writer.save()
                writer.close()
            except PermissionError as e:
                logging.error('文件被打开，请关闭，%s', e)
            except Exception as e:
                logging.error('文件其他错误，%s', e)

    def read_txt_data(self, num_per_line=None):
        """
        读取并解析txt文档测试数据
        :param file_name:
        :param num_per_line:每行数据个数
        :return:
        """
        with open(self.file_path, encoding='utf-8') as file_object:
            # line = file_object.readline()  # 读取一行;指针自动下移
            lines = file_object.readlines()  # 读取每一行存在一个列表中

        data_string = []
        for line in lines:
            # print line
            data_line = line.strip("\n").split()  # 去除首尾换行符，并按空格划分
            if num_per_line and len(data_line) != num_per_line:  # if data_line == []:
                continue
            else:
                data_string.append(data_line)

        # print "data_string = ", data_string
        data = []
        for i in range(len(data_string)):
            if len(data_string[i]) == 1:  # 每行只有一个
                data.append(data_string[i][0])
            else:
                for j in range(len(data_string[i])):
                    data[i][j] = float(data_string[i][j])

        # print "data = ", data
        # print data[1][3]
        return data

    def save_txt(self, data):
        # l = ["A", "B", "C", "D"]
        f = open(self.file_path, mode="w", encoding="utf-8")
        if isinstance(data, list):
            # f.writelines(data)  # 写到一行
            f.write('\n'.join(data))  # 写到好多行
            f.close()
        return True

    def save_json(self, data):
        """保存数据为json文件"""
        expect_result = self.is_expect_file_type(expect_file_type='json')
        if expect_result is False:
            logging.error('文件格式错误')
            return False
        try:
            b = json.dumps(data, ensure_ascii=False, indent=4)
            f2 = open(self.file_path, mode='w', encoding="utf-8")
            f2.write(b)
            f2.close()
            return True
        except Exception as e:
            logging.error('保存json文件错误, %s', e)
            return False

    def read_json(self):
        """保存数据为json文件"""
        if self.is_expect_file_type(expect_file_type='json'):
            try:
                file = open(self.file_path, 'r')
                str = file.read()
                data = json.loads(str)
                file.close()
                # data = json.loads(self.file_path)
                return data
            except Exception as e:
                logging.error('读取json文件错误, %s', e)
                return False
        else:
            logging.error('文件格式错误')
            return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # file_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data\20150129_1.json'
    # data = File(file_path).read_json()
    # print(data)

    file_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data\business_table.txt'
    # file_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data\other_20150112.tar.gz'
    # dir_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data'
    # file = File
    # df = pd.DataFrame([{'a':1, 'b':2}, {'a': 5, 'b':4}])
    data_list = File(file_path).read_txt_data()
    print(data_list)



