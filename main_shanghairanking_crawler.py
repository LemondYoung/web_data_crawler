import logging

from main_crawler import CrawlerMain

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    style = 'realism'
    url_list = ['https://www.shanghairanking.cn/api/v2010/inst?name=&prov=&cat=&lev=&givemeall=y&inbound=&limit=']
    CrawlerMain().run(parser_type='shanghai_tanking', urls=url_list, style=style)