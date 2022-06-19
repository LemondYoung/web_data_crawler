# -*- coding: UTF-8 -*-


# 解析出page页
import json, datetime
import logging
import os

from lxml import etree

from data_crawler.html_parser import Parser
from data_parse.parse_tools.img_parser import ocr, get_img_info
from data_parse.parse_tools.url_parse import split_url
from settings import db_map
from utils.computer.file import File


class WeiboBlogParser(Parser):

    def __init__(self):
        super().__init__()
        self.table_name = None

    def parse_data(self, html, url=None, parser_type=None, **kwargs):
        data = json.loads(html).get('data')
        if not data:
            logging.error('获取数据失败')
            return False
        logging.info('获取数据成功')
        blog_list = data['list']
        new_blog_list = []
        print(blog_list[0])
        for blog_item in blog_list:
            new_item = {
                'blog_id': blog_item['id'],
                'blog_code': blog_item['mblogid'],
                'content_text': blog_item['text_raw'],
                'img_ids_str': blog_item.get('pic_ids'),
                'img_infos_str': blog_item.get('pic_infos'),
                'img_num': blog_item.get('pic_num'),
                'user_str': blog_item['user'],
                'create_time': datetime.datetime.strptime(blog_item['created_at'], '%a %b %d %H:%M:%S %z %Y'),
            }
            new_blog_list.append(new_item)

        img_data = []
        for item in new_blog_list:
            try:
                if item['img_num'] > 0:
                    for img_code, value in item['img_infos_str'].items():
                        for img_type, v in value.items():
                            if img_type not in ('thumbnail', 'bmiddle','large','original', 'largest', 'mw2000',):
                                continue
                            img_item = {
                                'img_code': img_code,
                                'img_url': v.get('url'),
                                'img_name': img_code + '_' + img_type,
                                'format': v['url'].split('.')[-1] if v.get('url') else None,
                                'width': v['width'],
                                'height': v['height'],
                                'img_type': img_type,
                            }
                            img_data.append(img_item)
            except Exception as e:
                logging.error('圖片解析失敗，%s', e)
                logging.error(item)
                pass
            item['img_ids_str'] = json.dumps(item['img_ids_str'], ensure_ascii=False, indent=2)
            item['img_infos_str'] = json.dumps(item['img_infos_str'], ensure_ascii=False, indent=2)
            item['user_str'] = json.dumps(item['user_str'], ensure_ascii=False, indent=2)

        blog_url_item = {
            'url': url,
            'url_type': 'blog',
            'remark': None,
            'data_source': 'weibo',
        }
        blog_url_data = [blog_url_item]
        img_url_data = []
        for item in img_data:
            new_item = {
                'url': item['img_url'],
                'url_type': 'img',
                'style_code': item['img_type'],
                'data_source': 'weibo',
            }
            img_url_data.append(new_item)
        return {
            'url': url,
            'result': True,
            'data_list': [
                {'table_name': 't_blog_info', 'data': new_blog_list},
                {'table_name': 't_img_info', 'data': img_data},
                {'table_name': 's_url_manager', 'data': blog_url_data},
                {'table_name': 's_url_manager', 'data': img_url_data},
            ]
        }


class WeiboImgParser(Parser):

    def __init__(self):
        super().__init__()
        self.table_name = None

    def parse_data(self, html, url=None, parser_type=None, **kwargs):
        img_path = html
        dir_path = kwargs.get('dir_path')
        # content 是识别后得到的结果
        ocr_text = ocr(img_path)
        img_info = get_img_info(img_path)
        品_index = None
        for text in ocr_text:
            if '品' in text:
                品_index = ocr_text.index(text)
                break
        if 品_index is None:
            for text in ocr_text:
                if '作' in text:
                    品_index = ocr_text.index(text)
                    break
        try:
            last_index = ocr_text.index('大赛详情及投稿见@上海交通大学研究生会置顶微博')
            text_index = ocr_text[品_index - 1]
            text_title = ocr_text[品_index + 1]
            text_author = ocr_text[last_index - 3]
            text_content = ocr_text[品_index + 2: last_index - 3]
        except Exception as e:
            logging.error('图片ocr解析格式错误，%s', e)
            logging.error(ocr_text)
            return {
                'url': url,
                'result': False,
                'data_list': []
            }
        img_content_dict = {
            'index': text_index,
            'title': text_title,
            'author': text_author,
            'content': text_content,
        }
        # 重命名
        if text_title and text_author and dir_path:
            img_name = text_index + ' - ' + text_title + ' - ' + text_author
            new_img_path = os.path.join(dir_path, img_name + '.jpg')
            try:
                os.rename(img_path, new_img_path)  # 重命名,覆盖原先的名字
                logging.warning('图片名字由%s改为%s', img_path, new_img_path)
                url = new_img_path
            except FileExistsError as e:
                logging.error('文件已存在,%s', e)
                return {
                    'url': url,
                    'result': False,
                    'data_list': []
                }

        img_item = {
            'img_url': url,
            'content': json.dumps(img_content_dict, ensure_ascii=False, indent=2),
            'format': img_info.get('format'),
            'width': img_info.get('width'),
            'height': img_info.get('height'),
            'parser_type': parser_type,
        }
        if text_title and text_author:
            img_item['img_name'] = text_index + ' - ' + text_title + ' - ' + text_author
        else:
            img_item['img_name'] = None


        img_data = [img_item]
        return {
            'url': url,
            'result': True,
            'data_list': [
                {'table_name': 't_img_info', 'data': img_data},
            ]
        }


# 数据库中的poetry content转存txt文件
def poetry_to_txt():
    collage_list = File(file_path=r'D:\software\pycharm\project\data_sync\web_data_crawler\data\txt\all_college.txt').read_txt_data()
    collage_str = ''.join(collage_list)
    sql = """select content from t_img_info where content is not null"""
    data = db_map.get('weibo_data').query(sql)
    for item in data:
        d = json.loads(item['content'])
        print(d)
        cc = [collage for collage in collage_list if collage in d['author']]
        if len(cc) != 1:  # 啥情况？
            print(d['author'] + '匹配到啥了？', cc)
            continue
        collage = cc[0]
        author = d['author'].split(collage)[0]
        title = d['index'] + ' - ' + d['title'] + ' - ' + author + ' - ' + collage
        file_path = os.path.join(r'D:\software\pycharm\project\data_sync\web_data_crawler\data\txt\poetry', title+'.txt')
        File(file_path=file_path, is_check_file=False).save_txt(d['content'])
        break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    poetry_to_txt()
