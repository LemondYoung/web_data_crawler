"""
# File       : bilibili_parser.py
# Time       ：2022/6/12 23:45
# Author     ：author name
# version    ：python 3.6
# Description： 解析哔哩哔哩的url
"""
import logging
import os

from data_parse.parse_tools.json_parser import read_json_file
from data_sync.data_load.mysql_data_load import save_table_data
from settings import JSON_PATH

"""可以返回指定用户的视频列表
pn 第几页
ps 一页几个,最多50
"""
'https://api.bilibili.com/x/space/arc/search?mid=697166795&ps=50&tid=0&pn=4&keyword=&order=pubdate'

import datetime
import pandas as pd


# 临时
def get_bilibili_video_json_code(json_obj, return_type=None):
    v_list = json_obj['data']['list']['vlist']
    url_list = []
    name_list = []
    new_data = []
    for item in v_list:
        video_code = item['bvid']  # https://www.bilibili.com/video/BV163411g7Ke
        video_title = item['title']
        video_author = item['author']
        video_length = item['length']
        video_comment = item['comment']  # 弹幕数
        video_review = item['video_review']  # 弹幕数
        video_play = item['play']  # 评论数
        video_author_id = item['mid']
        video_time = datetime.datetime.fromtimestamp(item['created']).strftime("%Y-%m-%d %H:%M:%S")
        url = 'https://www.bilibili.com/video/' + video_code
        new_item = {
            'video_code': video_code,
            'video_title': video_title,
            'video_author': video_author,
            'video_length': video_length,
            'video_comment': video_comment,
            'video_review': video_review,
            'video_play': video_play,
            'video_author_id': video_author_id,
            'video_url': url,
            'video_time': video_time,
        }
        new_data.append(new_item)
    if return_type == 'df':
        df = pd.DataFrame(new_data)
        return df
    else:
        return new_data


def run_bilibili_video_json_code():
    cur_path = os.path.join(JSON_PATH, 'bilibili_user_videos', 'xuyun')
    json_path_list = [
        os.path.join(cur_path, 'xuyun_1.json'),
        os.path.join(cur_path, 'xuyun_2.json'),
        os.path.join(cur_path, 'xuyun_3.json'),
        os.path.join(cur_path, 'xuyun_4.json'),
        ]

    all_df = pd.DataFrame()
    all_data = []
    for json_path in json_path_list:
        json_obj = read_json_file(json_path)
        data = get_bilibili_video_json_code(json_obj, return_type=None)
        # all_df = pd.concat([all_df, df], ignore_index=True)
        all_data.extend(data)
    result = save_table_data(table_name='t_video_info', records=all_data, target_db_name='bilibili_data')
    # print(all_data)
    return result

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_bilibili_video_json_code()