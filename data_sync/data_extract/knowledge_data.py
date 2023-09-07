"""
# File       : knowledge_data.py
# Time       ：2022/6/19 16:13
# Author     ：lemondyoung
# version    ：python 3
# Description：
"""
from settings import db_map

db = db_map.get('knowledge_data')


def get_knowledge_data(table_name, filter: dict = None, return_type=None, return_value=None):
    sql = """
    select * from {table_name}
    where 1=1
    """.format(table_name=table_name)
    if filter and isinstance(filter, dict):
        for key, value in filter.items():
            sql += """ and {key} in ({value}) """.format(key, value)
    data = db.query(sql)
    if return_type == 'list':
        return [item[return_value] for item in data]
    else:
        return data


if __name__ == '__main__':
    data = get_knowledge_data('t_all_collage', return_type='list', return_value='collage_name')
    print(data)