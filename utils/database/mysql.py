#!/opt/.pyenv/shims/python3
# -*- coding: utf-8 -*-
# @Time    : 2017-10-19 13:51
# @Author  : pang
# @File    : mysql.py
# @Software: PyCharm

import logging
import sys

import pymysql
from DBUtils.PooledDB import PooledDB


# 警告转换为错误
from warnings import filterwarnings


filterwarnings('error', category=pymysql.Warning)

MAX_ROW_COUNT = 1000


class Mysql(object):
    INSERT_MODE = 1
    REPLACE_MODE = 2
    INSERT_UPDATE_MODE = 3
    UPDATE_MODE = 4

    def __init__(self, host, port, user, password, db):
        self.pool = PooledDB(creator=pymysql, mincached=1, maxcached=5,
                             host=host, port=port, user=user, passwd=password,
                             db=db, use_unicode=True, cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4')

    def __str__(self):
        return self.__class__.__name__

    def connection(self):
        return self.pool.connection()

    def query(self, sql, args=None):
        conn = self.connection()
        cur = conn.cursor()
        # logging.info('开始查询数据')
        try:
            cur.execute(sql, args)
        except Exception as e:
            logging.error('读取数据库失败！')
            logging.error(e)
            logging.error(sql)
            conn.rollback()
            cur.close()
            conn.close()
            return False
        conn.commit()
        result = cur.fetchall()
        # logging.info('查询数据成功')
        cur.close()
        conn.close()
        return result

    def execute(self, sql, commit=True, args=None):
        conn = self.connection()
        cur = conn.cursor()
        # 开始查询数据
        cur.execute(sql, args)
        # rowcount = cur.rowcount
        # logging.info('本次要操作的数据量'+str(rowcount))

        if commit:
            conn.commit()
            cur.close()
            conn.close()
            return None, None

        else:
            return cur, conn

    def executemany(self, sql, args=None):
        conn = self.connection()
        cur = conn.cursor()
        step = MAX_ROW_COUNT
        frames = [args[i:i + step] for i in range(0, len(args), step)]
        for frame in frames:
            cur.executemany(sql, frame)
        cur.close()
        conn.close()
        return cur

    def records_to_db(self, table_name, records, mode, cur=None, conn=None, delete_info=None, update_conditions=None):
        """
        批量插入数据到指定表
        :param table_name: 表名
        :param records: 要插入的数据.格式[{k1:v1, k2: v2}, {k1: v3, k2: v4}....].
        :param mode: 1: insert (主键冲突,插入失败). 2: replace(主键冲突,删除原有行再插入), 3: update (主键冲突更新数据)
        :param cur: 如果不提交的话需要传入游标，来确保删除插入是同一个事务
        :param conn: 同上
        :param delete_info: 删除标识（只有INSERT前起作用），='delete',则默认全部删除，否则进行字典解压，获取where条件
        :param update_conditions: 更新条件
        :return:
            result入库结果，frame数据（如果失败，则返回具体错误数据详情）
        """
        if len(records) == 0:
            logging.warning('入库数据量为0，退出')
            return 0, None
        else:
            item = records[0]

        # 插入语句生成
        if mode == self.INSERT_MODE:
            sql = "INSERT INTO `{table_name}` ({columns}) VALUES({values})".format(
                table_name=table_name,
                columns=", ".join([f"`{k}`" for k in item.keys()]),
                values=", ".join([f"%({k})s" for k in item.keys()]),
            )
        elif mode == self.REPLACE_MODE:
            sql = "REPLACE INTO `{table_name}` ({columns}) VALUES({values})".format(
                table_name=table_name,
                columns=", ".join([f"`{k}`" for k in item.keys()]),
                values=", ".join([f"%({k})s" for k in item.keys()]),
            )
        elif mode == self.INSERT_UPDATE_MODE:
            sql = "INSERT INTO `{table_name}` (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s".format(table_name=table_name)
            head = []
            mid = []
            tail = []
            for key in item.keys():
                head.append(f" `{key}` ")
                mid.append(f" %({key})s ")
                tail.append(f" `{key}`= VALUES(`{key}`)")
            sql = sql % (",".join(head), ",".join(mid), ",".join(tail))
        elif mode == self.UPDATE_MODE:
            # 第一个键值必须为条件，后面是需要更新的键值
            if not update_conditions:
                print('没有更新条件？')
            sql = "UPDATE `{table_name}` SET {update_values} where {condition_values}".format(
                table_name=table_name,
                update_values=", ".join([f"`{key}`= %({key})s" for key in item.keys() if key not in update_conditions]),
                condition_values=", ".join([f"`{key}`= %({key})s" for key in item.keys() if key in update_conditions]),
            )
        else:
            raise ValueError('mode error.')

        row_count = 0
        step = MAX_ROW_COUNT
        frames = [records[i:i + step] for i in range(0, len(records), step)]

        # 删除语句生成
        if delete_info is not None:
            if delete_info == 'truncate':
                delete_sql = """truncate table {table_name}""".format(table_name=table_name)
            elif delete_info == 'delete':
                delete_sql = """delete from {table_name}""".format(table_name=table_name)
            elif isinstance(delete_info, dict):
                delete_sql = """delete from {table_name} where 1=1""".format(table_name=table_name)
                for delete_col, delete_value in delete_info.items():
                    delete_sql += """ and {delete_col} in ({delete_value})""".format(delete_col=delete_col,
                                                                                     delete_value=delete_value)
            else:
                raise ValueError('delete_info格式错误！')
            logging.debug('当前要删除的语句%s', delete_sql)
            cur, conn = self.execute(sql=delete_sql, commit=False)

        elif cur is None and conn is None:
            # 如果删除游标为空的话，新建连接和游标
            conn = self.connection()
            cur = conn.cursor()

        # 开始插入数据
        # 全部成功后（包括delete）才提交，否则全部回退
        for frame in frames:
            try:
                cur.executemany(sql, frame)
                row_count += cur.rowcount
                # logging.info('查看变量内存占用：cur=%d MB, conn=%d MB', sys.getsizeof(cur) / 1024 / 1024, sys.getsizeof(conn) / 1024 / 1024)

            except Exception as e:
                logging.error('数据入库失败！回退')
                logging.error('当前数据入库语句为%s', sql)
                logging.error(e)
                conn.rollback()
                cur.close()
                conn.close()
                return False, frame

        conn.commit()
        cur.close()
        conn.close()
        return row_count, None



if __name__ == '__main__':
    mysql_db = MySql(**MYSQL_TEST_DB_CONFIG)
    data = [
        {'id': 11, 'name': 'dasfdas', 'sex': 1, },
        {'id': 12, 'name': '发顺丰', 'sex': 1, },
        {'id': 13, 'name': '刚刚', 'sex': 1, },
    ]
    mysql_db.records_to_db(table_name='test3', records=data)



