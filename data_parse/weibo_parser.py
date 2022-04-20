

# 解析出page页
import json
import logging

from lxml import etree

from data_crawler.html_parser import Parser
from data_parse.parse_tools.url_parse import split_url


class WeiboBlogParser(Parser):

    def __init__(self):
        super().__init__()
        self.table_name = None

    def parse_data(self, html, url=None):
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
            }
            new_blog_list.append(new_item)

        img_list = []
        for item in new_blog_list:
            try:
                if item['img_num'] > 0:
                    for img_code, value in item['img_infos_str'].items():
                        for img_type, v in value.items():
                            img_item = {
                                'img_code': img_code,
                                'img_url': v.get('url'),
                                'img_name': None,
                                'format': v['url'].split('.')[-1] if v.get('url') else None,
                                'width': v['width'],
                                'height': v['height'],
                                'img_type': img_type,
                            }
                            img_list.append(img_item)
            except Exception as e:
                logging.error('圖片解析失敗，%s', e)
                logging.error(item)
                pass
            item['img_ids_str'] = json.dumps(item['img_ids_str'])
            item['img_infos_str'] = json.dumps(item['img_infos_str'])
            item['user_str'] = json.dumps(item['user_str'])

        url_item = {
            'url': url,
            'url_type': 'blog',
            'remark': None,
            'data_source': 'weibo',
        }
        url_data = [url_item]
        return {
            't_blog_info': {'url': url, 'result': True, 'data': new_blog_list},
            't_img_info': {'url': url, 'result': True, 'data': img_list},
            's_url_manager': {'url': url, 'result': True, 'data': url_data},
        }

