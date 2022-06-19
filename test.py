import logging

from spider_main import spiderMain

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    style = 'realism'
    url_list = ['https://www.shanghairanking.cn/api/v2010/inst?name=&prov=&cat=&lev=&givemeall=y&inbound=&limit=']
    spiderMain().run(parser_type='shanghai_tanking', urls=url_list, style=style)