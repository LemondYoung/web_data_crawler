#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：hr_hedge_fund_data_sync -> dir
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/9/24 10:14
@Desc   ：
==================================================
"""


# 文件夹基类
import datetime
import logging
import os
import shutil
import tarfile
import time
import uuid

from settings import PROJECT_NAME
from utils.common_standardize import standardize_date
from utils.computer.file import File


class Dir(object):
    """
    1. 查找目录
    2. 输入输出路径标准化
    """

    def __new__(cls, dir_path):
        if not os.path.isdir(dir_path):  # 跳过非目录对象
            logging.warning('%s非文件夹对象', dir_path)
            return False
        else:
            return object.__new__(cls)

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get_dir_info(self):
        dir_info = {}
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(self.dir_path)))
        modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(self.dir_path)))
        dir_info['create_time'] = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        dir_info['modify_time'] = datetime.datetime.strptime(modify_time, "%Y-%m-%d %H:%M:%S")
        return dir_info

    # 压缩压缩包
    def zip_file(self, dir_path, zip_type='tgz'):
        if not os.path.isdir(dir_path):
            logging.error('文件夹不存在')
            return False
        root_path, dir_name = os.path.split(dir_path)
        zip_name = dir_name + '.tar.gz'
        zip_path = os.path.join(root_path, zip_name)
        with tarfile.open(zip_path, 'w:gz') as tar:
            for root, dirs, files in os.walk(dir_path):
                for single_file in files:
                    filepath = os.path.join(root, single_file)
                    tar.add(filepath, arcname=single_file)
        return zip_path

    # 删除目录下文件
    def del_files(self, judgement_type='file_name_date', overdue_days=30):
        """
        :param dir_path
        :param judgement_type 判断依据【file_name_date文件名中的日期、create_time创建时间】
        :param overdue_days 过期天数
        """
        _ = self.walk_dir(dir_path=self.dir_path).get(1)  # 获取第一层全部文件和目录
        dirs = _.get('dirs')
        files = _.get('files')
        all = dirs + files
        today_time = datetime.datetime.today()
        today_date = datetime.datetime.today().strftime('%Y%m%d')

        delete_list = []
        if judgement_type == 'file_name_date':
            for single in all:
                single_path = os.path.join(self.dir_path, single)
                file_type = 'dir' if os.path.isdir(single_path) else 'computer'
                data_date = standardize_date(single, param_separator='', return_separator='')
                data_time = datetime.datetime.strptime(data_date, '%Y%m%d')
                delta_days = (today_time - data_time).days
                if delta_days > overdue_days:
                    logging.info('%s天 %s该删除了', delta_days, single)
                    try:
                        if os.path.isfile(single_path):
                            os.remove(single_path)
                        elif os.path.isdir(single_path):
                            shutil.rmtree(single_path)
                            # os.removedirs(single_path)
                        logging.info("已删除文件：%s", single_path)
                        item = {
                            'ID': str(uuid.uuid1()).replace('-', ''),
                            'FILE_NAME': single,
                            'DATA_DATE': data_date,
                            'FILE_TYPE': file_type,
                            'SAVE_MODE': 'delete',
                        }
                        delete_list.append(item)
                    except Exception as e:
                        print(e)
                else:
                    logging.info('%s天 %s还不用删除', delta_days, single)

        elif judgement_type == 'create_time':
            for single in all:
                single_path = os.path.join(self.dir_path, single)
                if os.path.isfile(single_path):
                    file = File(file_path=single_path)
                    create_time = file.get_file_info().get('create_time')
                    file_type = 'computer'
                    data_date = standardize_date(single, return_separator='')
                elif os.path.isdir(single_path):
                    dir = Dir(dir_path=single_path)
                    create_time = dir.get_dir_info().get('create_time')
                    file_type = 'dir'
                    data_date = standardize_date(single, return_separator='')
                else:
                    logging.error('对象类型错误')
                    return False

                delta_days = (today_time - create_time).days
                if delta_days > overdue_days:
                    logging.info('%s天 %s该删除了', delta_days, single)
                    try:
                        os.remove(single_path)
                        logging.info("已删除文件：%s", single_path)
                        item = {
                            'FILE_NAME': single,
                            'DATA_DATE': data_date if data_date else datetime.datetime.strftime(create_time, '%Y%m%d'),
                            'FILE_TYPE': file_type,
                            'SAVE_MODE': 'delete',
                        }
                        delete_list.append(item)
                    except Exception as e:
                        print(e)
                else:
                    logging.info('%s天 %s还不用删除', delta_days, single)
        return delete_list

    def del_dir(self):
        print('要刪除的文件夹为%s，缓冲5s' % (self.dir_path))
        time.sleep(5)
        if not self.dir_path.find(PROJECT_NAME):
            logging.warning('要删除的文件夹非项目下文件夹，请检查！')
            return False
        else:
            shutil.rmtree(self.dir_path)  # 谨慎删除
        if not os.path.isdir(self.dir_path):  # 跳过非目录对象
            logging.info('删除成功')
            return True
        else:
            logging.error('删除失败')
            return False


    def walk_dir(self, dir_path, depth=1):
        dirs_list = []  # 存放第1级子目录
        files_list = []  # 存放第1级子目录
        root_depth = len(dir_path.split(os.path.sep))
        for cur_path, dirs, files in os.walk(dir_path, topdown=False):
            cur_depth = len(cur_path.split(os.path.sep))
            for file in files:
                if cur_depth == root_depth:
                    files_list.append(file)
                else:
                    break
            for dir in dirs:
                if cur_depth == root_depth:
                    dirs_list.append(dir)
                else:
                    break
        dic = {
            1: {'dirs': dirs_list, 'files': files_list}
        }
        return dic

    # 获取目录下全部文件
    def find_files(self, file_type=None):
        dir_path = self.dir_path
        file_list = []
        for name in os.listdir(dir_path):
            if file_type == 'xls' and (name.endswith('.xlsx') or name.endswith('.xls') or name.endswith('.xlsm')):
                # 生成excel文件的绝对路径
                excel_absolute_path = os.path.join(dir_path, name)
                file_list.append(excel_absolute_path)
            elif file_type == 'txt' and name.endswith('.txt'):
                absolute_path = os.path.join(dir_path, name)
                file_list.append(absolute_path)
            elif file_type == 'json' and name.endswith('.json'):
                absolute_path = os.path.join(dir_path, name)
                file_list.append(absolute_path)
            elif file_type == 'jpg' and (name.endswith('.jpg') or name.endswith('.jpeg')):
                absolute_path = os.path.join(dir_path, name)
                file_list.append(absolute_path)
            elif file_type == 'png' and (name.endswith('.png')):
                absolute_path = os.path.join(dir_path, name)
                file_list.append(absolute_path)
            elif file_type is None:
                absolute_path = os.path.join(dir_path, name)
                file_list.append(absolute_path)
            else:
                logging.error('文件类型错误')
                return False
        return file_list

    # 标准化输入输出文件目录
    def standard_file_dir(self, out_type, in_dir=None, in_file=None, out_dir=None, out_file=None):
        """
        输入目录自动获取全部，或者指定文件路径
        输出目录自动生成，或指定文件路径
        """
        if in_file and not os.path.isfile(in_file):
            logging.error('输入文件不存在')
            return None

        new_list = []
        if in_dir and not in_file and out_dir and not out_file:  # 指定输入输出目录
            xls_list = self.find_files(in_dir)  # 获取全部指定类型文件
            for xls_path in xls_list:
                path, file = os.path.split(xls_path)
                name = file.split('.')[0]
                if name[0:2] != '~$':
                    out_file = os.path.join(out_dir, name + '.' + out_type)
                    new_path_list = [xls_path, out_file]
                    new_list.append(new_path_list)

        elif not in_dir and in_file and out_dir and not out_file:  # 指定输入文件和输出目录
            path, file = os.path.split(in_file)
            name = file.split('.')[0]
            if name[0:2] != '~$':
                out_file = os.path.join(out_dir, name + '.' + out_type)
                new_list = [[in_file, out_file]]

        elif not in_dir and in_file and not out_dir and out_file:  # 指定输入输出文件
            new_list = [[in_file, out_file]]

        elif not in_dir and in_file and not out_dir and not out_file:  # 指定输入文件，默认输出文件目录和名称都以输入为准
            path, file = os.path.split(in_file)
            name = file.split('.')[0]
            if name[0:2] != '~$':
                out_file = os.path.join(path, name + '.' + out_type)
                new_list = [[in_file, out_file]]
        else:
            logging.error('输入文件形式错误！')
            raise Exception
        return new_list

    def run_unzip_file(self, zip_path, zip_type='tgz', file_type='txt'):
        logging.info('获取压缩文件路径')
        dir_path = self.unzip_file(zip_path=zip_path, zip_type=zip_type)
        if dir_path:
            logging.info('解压成功，文件夹路径%s', dir_path)
            logging.info('查找解压文件夹下所有文件，文件类型%s', file_type)
            files = self.find_files(dir_path=dir_path, file_type=file_type)
            if files and len(files) > 0:
                logging.info('解压文件查找成功，文件个数%s', len(files))
                return dir_path
            else:
                logging.info('解压文件查找失败')
                return False

        else:
            logging.error('解压失败')
            return False



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # zip_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data\data.tar.gz'
    # dir_path = r'D:\program\pycharm\projects\data_sync\hr_hedge_fund_data_sync\data'
    # Dir(dir_path).run_unzip_file(zip_path, file_type='json')
    dir_path = r'D:\software\pycharm\project\data_sync\web_data_crawler\src\imgs'
    dd = Dir(dir_path).find_files()
    print(dd)