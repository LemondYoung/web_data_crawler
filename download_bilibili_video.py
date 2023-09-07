
"""
测试下载bilibil视频
"""

import logging
import os.path

import you_get


# import os
# os.system('you-get -o d:/video/ https://www.bilibili.com/video/BV11B4y1D7EM?spm_id_from=333.999.0.0&vd_source=99cf2756ae9ed79fa6b6f4044eb6e7dc')


import sys
from you_get import common as you_get
from you_get.extractors import Bilibili
from you_get.json_output import download_urls
# from you_get.extractor import Bilibili
from settings import db_map
from constants import STORE_DATA_UPDATE
from data_parse.parse_tools import danmaku2ass
from data_sync.data_load.mysql_data_load import save_table_data
from utils import globalvar
from utils.log import InterceptHandler


# 下载哔哩哔哩视频
def download_bilibili_video(url_list, dir_path, xml_path=None, ass_path=None, is_download_video=True, is_transform_ass=True, title=None, is_debug=True):
    """
    :param url_list:
    :param dir_path:
    :param xml_path: 原字幕路径，默认空  # r'D:\video\为了逃避生活，我骑行流浪一年了，每天都在向着远方前行，但是最近也迷茫了.cmt.xml'
    :param ass_path: 标准的字幕路径，默认空  # r'D:\video\为了逃避生活，我骑行流浪一年了，每天都在向着远方前行，但是最近也迷茫了.cmt.ass'
    :param is_download_video:  是否转换下载视频，默认真
    :param is_transform_ass:  是否转换字幕文件，默认真
    :param title: 视频标题，默认空
    :param is_debug: 是否debug
    :return:
    """
    for index, url in enumerate(url_list, 1):
        logging.info('*'*100)
        logging.info('【%s/%s】要下载的视频连接 %s', index, len(url_list), url)
        logging.info('*'*100)

        # 判断是都下载视频
        if not is_download_video:
            logging.info('查看视频信息')
            sys.argv = ['you-get', url, '-i']
            you_get.main()
        else:
            logging.info('保存到 %s', dir_path)
            sys.argv = ['you-get', url, '-o', dir_path]
            if is_debug:
                sys.argv.append('--debug')
            try:
                you_get.main()
            except Exception as e:
                logging.error('下载视频失败，重试, %s', e)
                continue
        if not title:
            title = globalvar.get_value('video_title')  # 从全局变量里捞回来的，要修改依赖包
        logging.warning('下载的视频为：%s', title)

        # 判断是否转换字幕
        if not is_transform_ass:
            logging.info('不需要转换字幕文件')
            return True

        if not xml_path:
            xml_path = os.path.join(dir_path, title + '.cmt.xml')
        if not ass_path:
            ass_path = os.path.join(dir_path, title + '.cmt.ass')
        logging.info('弹幕原文件%s，转换后%s', xml_path, ass_path)
        sys.argv = ['file', xml_path,
                    '-o', ass_path,
                    '--size', '1080x1080', '--font', '"MS PGothic"', '--fontsize', '38', '--alpha', '0.6', '-dm', '15', '-ds', '5' # 弹幕配置，欢喜就好
                    ]
        danmaku2ass.main()


def get_bilibili_video_url(return_type=None):
    sql = """ select url, url_name from s_url_manager where 1=1 
    and source_name = 'bilibili'  and url_type = 'video' and url_status = 0"""
    data = db_map.get('bilibili_data').query(sql)
    return data

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    url_list = [
        # 'https://www.bilibili.com/video/BV163411g7Ke',
        # 'https://www.bilibili.com/video/BV1R34y1V7xr',
        # 'https://www.bilibili.com/video/BV1qY411M7tj',
        # 'https://www.bilibili.com/video/BV1d34y1L7tx',
        # 'https://www.bilibili.com/video/BV11B4y1D7EM',
        # 'https://www.bilibili.com/video/BV1i94y1m71c',
        # 'https://www.bilibili.com/video/BV1sg411d7Xb',
        # 'https://www.bilibili.com/video/BV1N94y1m7g8',
        # 'https://www.bilibili.com/video/BV11Z4y1b74X',
        # 'https://www.bilibili.com/video/BV1dF41157h2',
        # 'https://www.bilibili.com/video/BV1Y94y1U7GF',
        # 'https://www.bilibili.com/video/BV1C34y1j74j',
        # 'https://www.bilibili.com/video/BV1iB4y197Yk',
        # 'https://www.bilibili.com/video/BV1VA4y1Z7p5',
        # 'https://www.bilibili.com/video/BV1tv4y1N7vB',
        # 'https://www.bilibili.com/video/BV1vZ4y187Zs',
        # 'https://www.bilibili.com/video/BV1Wa411J7vn',
        # 'https://www.bilibili.com/video/BV1vB4y1y7E7',
        # 'https://www.bilibili.com/video/BV1eZ4y1a7ty',
        # 'https://www.bilibili.com/video/BV1fa411E7ax',
        # 'https://www.bilibili.com/video/BV1qR4y1A7e2',
        # 'https://www.bilibili.com/video/BV1kT4y1679u',
        # 'https://www.bilibili.com/video/BV1PF411M7k6',
        # 'https://www.bilibili.com/video/BV1W34y1Y7KN',
        # 'https://www.bilibili.com/video/BV1ea411a7iq',
        # 'https://www.bilibili.com/video/BV1aa411e7Aa',
        # 'https://www.bilibili.com/video/BV1LB4y1174T',
        # 'https://www.bilibili.com/video/BV1YS4y1875M',
        # 'https://www.bilibili.com/video/BV1KA4y1D7Lf',
        # 'https://www.bilibili.com/video/BV1mu411k78B',
        # 'https://www.bilibili.com/video/BV1Du411k7mK',
        # 'https://www.bilibili.com/video/BV1pR4y1K7Mq',
        # 'https://www.bilibili.com/video/BV1CZ4y117ZJ',
        # 'https://www.bilibili.com/video/BV1R541127g3',
        # 'https://www.bilibili.com/video/BV1ML4y1V7tu',
        # 'https://www.bilibili.com/video/BV1RY411j7ni',
        # 'https://www.bilibili.com/video/BV1c44y1G7mQ',
        # 'https://www.bilibili.com/video/BV1k541127Wn',
        # 'https://www.bilibili.com/video/BV1bS4y1275u',
        # 'https://www.bilibili.com/video/BV1RY411L7LX',
        # 'https://www.bilibili.com/video/BV1ei4y1D78q',
        # 'https://www.bilibili.com/video/BV1Vr4y1p7SP',
        # 'https://www.bilibili.com/video/BV1Dr4y1p7vE',
        # 'https://www.bilibili.com/video/BV1Ha411i753',
        # 'https://www.bilibili.com/video/BV1TS4y1K76Q',
        # 'https://www.bilibili.com/video/BV17P4y1K7Mf',
        # 'https://www.bilibili.com/video/BV1EP4y1M7JC',
        # 'https://www.bilibili.com/video/BV1pY4y1q7mB',
        # 'https://www.bilibili.com/video/BV1cr4y1s7cx',
        # 'https://www.bilibili.com/video/BV1jP4y1M7Pe',
        # 'https://www.bilibili.com/video/BV1Jq4y1Y7gM',
        # 'https://www.bilibili.com/video/BV1Jq4y1Y74Q',
        # 'https://www.bilibili.com/video/BV1VY4y1q7ub',
        # 'https://www.bilibili.com/video/BV1ou411q7ma',
        # 'https://www.bilibili.com/video/BV1HY411n7dh',
        # 'https://www.bilibili.com/video/BV1Gu411q7mB',
        # 'https://www.bilibili.com/video/BV1Qr4y1B7Rn',
        # 'https://www.bilibili.com/video/BV1744y1T76v',
        # 'https://www.bilibili.com/video/BV1kL4y1T75n',
        # 'https://www.bilibili.com/video/BV1kP4y1M7aM',
        # 'https://www.bilibili.com/video/BV1hb4y1W76a',
        # 'https://www.bilibili.com/video/BV1nS4y1S792',
        # 'https://www.bilibili.com/video/BV1mb4y1x7oC',
        # 'https://www.bilibili.com/video/BV1LT4y1D7HS',
        # 'https://www.bilibili.com/video/BV1Tu411Q7Eq',
        # 'https://www.bilibili.com/video/BV16T4y1Q7pd',
        # 'https://www.bilibili.com/video/BV1M34y1k7ES',
        # 'https://www.bilibili.com/video/BV17S4y1F7nH',
        # 'https://www.bilibili.com/video/BV1qi4y1f7Yz',
        # 'https://www.bilibili.com/video/BV1JP4y1w7Hq',
        # 'https://www.bilibili.com/video/BV1Ka41117Es',
        # 'https://www.bilibili.com/video/BV1F34y1C7eB',
        # 'https://www.bilibili.com/video/BV1GF411n7Go',
        # 'https://www.bilibili.com/video/BV1Ub4y1j7ZX',
        # 'https://www.bilibili.com/video/BV1dF411J7em',
        # 'https://www.bilibili.com/video/BV1gS4y117EP',
        # 'https://www.bilibili.com/video/BV1V34y1y7NK',
        # 'https://www.bilibili.com/video/BV1kF411H7h4',
        # 'https://www.bilibili.com/video/BV1hZ4y1Z7G1',
        # 'https://www.bilibili.com/video/BV1pL4y1x7mU',
        # 'https://www.bilibili.com/video/BV1Uq4y1C7V3',
        # 'https://www.bilibili.com/video/BV1mr4y1e78q',
        # 'https://www.bilibili.com/video/BV1wF411p7eX',
        # 'https://www.bilibili.com/video/BV1eq4y1c7Qt',
        # 'https://www.bilibili.com/video/BV1vS4y1o72Y',
        #'https://www.bilibili.com/video/BV1e34y1B79X',
        # 'https://www.bilibili.com/video/BV1Qm4y1U7LC',
        'https://www.bilibili.com/video/BV1V44y1L7BH',
        'https://www.bilibili.com/video/BV1aq4y1y7k7',
        'https://www.bilibili.com/video/BV1Cq4y1y7gt',
        'https://www.bilibili.com/video/BV14a411q7SC',
        'https://www.bilibili.com/video/BV1qY411a7JD',
        'https://www.bilibili.com/video/BV1Kr4y1v7VA',
        'https://www.bilibili.com/video/BV1za411z7Ma',
        'https://www.bilibili.com/video/BV1m34y1z732',
        'https://www.bilibili.com/video/BV1tm4y1Q71Q',
        'https://www.bilibili.com/video/BV14L4y1E7Pe',
        'https://www.bilibili.com/video/BV1pm4y1Q7nr',
        'https://www.bilibili.com/video/BV1Ar4y1S7PQ',
        'https://www.bilibili.com/video/BV1fa411z7LE',
        'https://www.bilibili.com/video/BV17D4y1c7iD',
        'https://www.bilibili.com/video/BV1uP4y1H7oQ',
        'https://www.bilibili.com/video/BV1SY411W7Ud',
        'https://www.bilibili.com/video/BV1WP4y1G7QA',
        'https://www.bilibili.com/video/BV1jM4y1A7Z5',
        'https://www.bilibili.com/video/BV1L34y1973c',
        'https://www.bilibili.com/video/BV1Xb4y1i7BG',
        'https://www.bilibili.com/video/BV1FP4y1G7pN',
        'https://www.bilibili.com/video/BV1hb4y1B7wL',
        'https://www.bilibili.com/video/BV1ih411s7W2',
        'https://www.bilibili.com/video/BV1kf4y1K7wd',
        'https://www.bilibili.com/video/BV1Cq4y1B7yX',
        'https://www.bilibili.com/video/BV1Bf4y1K7Gi',
        'https://www.bilibili.com/video/BV1uY41147ZP',
        'https://www.bilibili.com/video/BV1cR4y1b7NU',
        'https://www.bilibili.com/video/BV1w44y1Y7gt',
        'https://www.bilibili.com/video/BV1AL4y1i7vx',
        'https://www.bilibili.com/video/BV1aP4y157WD',
        'https://www.bilibili.com/video/BV1rS4y1d7AM',
        'https://www.bilibili.com/video/BV1Xb4y187cM',
        'https://www.bilibili.com/video/BV1kR4y1E7ut',
        'https://www.bilibili.com/video/BV1oq4y1r7H8',
        'https://www.bilibili.com/video/BV1Gf4y1u7p5',
        'https://www.bilibili.com/video/BV1jh411t7hH',
        'https://www.bilibili.com/video/BV1VQ4y1S7oY',
        'https://www.bilibili.com/video/BV1Zh411b7KD',
        'https://www.bilibili.com/video/BV1b44y1v7p5',
        'https://www.bilibili.com/video/BV12L411g71o',
        'https://www.bilibili.com/video/BV1cQ4y1Q7ER',
        'https://www.bilibili.com/video/BV12F411Y7Lr',
        'https://www.bilibili.com/video/BV1Jq4y1974z',
        'https://www.bilibili.com/video/BV1Tu411f7gW',
        'https://www.bilibili.com/video/BV12P4y1t7uN',
        'https://www.bilibili.com/video/BV1uQ4y1z7Ch',
        'https://www.bilibili.com/video/BV1ML411G7qE',
        'https://www.bilibili.com/video/BV183411C7C2',
        'https://www.bilibili.com/video/BV1JR4y1H7nW',
        'https://www.bilibili.com/video/BV1VT4y1f7TC',
        'https://www.bilibili.com/video/BV1fL4y1z7SJ',
        'https://www.bilibili.com/video/BV1Jh411J7kv',
        'https://www.bilibili.com/video/BV14f4y1c7LZ',
        'https://www.bilibili.com/video/BV1bb4y117Qw',
        'https://www.bilibili.com/video/BV1WQ4y1C76M',
        'https://www.bilibili.com/video/BV12u411f76Y',
        'https://www.bilibili.com/video/BV1Yf4y1F7GZ',
        'https://www.bilibili.com/video/BV1xM4y137vQ',
        'https://www.bilibili.com/video/BV1v64y187hD',
        'https://www.bilibili.com/video/BV1tf4y1E7Ny',
        'https://www.bilibili.com/video/BV1XQ4y1672h',
        'https://www.bilibili.com/video/BV1pq4y1N74n',
        'https://www.bilibili.com/video/BV1x64y1h7VT',
        'https://www.bilibili.com/video/BV1EM4y1g7Lb',
        'https://www.bilibili.com/video/BV1yh411W7e8',
        'https://www.bilibili.com/video/BV1hv411P77k',
        'https://www.bilibili.com/video/BV19L411472p',
        'https://www.bilibili.com/video/BV1Gf4y1A76t',
        'https://www.bilibili.com/video/BV1hU4y1P7Lx',
        'https://www.bilibili.com/video/BV1Rh411W7rP',
        'https://www.bilibili.com/video/BV1844y187Fm',
        'https://www.bilibili.com/video/BV1hL4y1Y7VE',
        'https://www.bilibili.com/video/BV1DA411c7vA',
        'https://www.bilibili.com/video/BV1VM4y15727',
    ]
    data = get_bilibili_video_url()
    dir_path = r'f:\video'
    title = None

    logging.info('获取到要下载的video个数:%s', len(data))
    for index, item in enumerate(data, 1):
        logging.info('【【%s/%s】】', index, len(data))
        url = item['url']
        title = item['url_name']
        url_list = [url]
        download_bilibili_video(url_list, dir_path, title=title, is_download_video=True)
        result = save_table_data(table_name='s_url_manager', records=[{'url': url, 'url_status': 1}], target_db_name='bilibili_data', mode=STORE_DATA_UPDATE)
