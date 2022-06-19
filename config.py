from data_parse.shanghairanking_parser import ShanghaiRankingParser
from settings import WEIBO_DB_CONFIG, DOUBAN_DB_CONFIG, BILIBILI_DB_CONFIG
from data_parse.weibo_parser import WeiboBlogParser, WeiboImgParser
from utils.database.mysql import Mysql

parser_map = {
    'weibo_blog': WeiboBlogParser(),
    'img_url': WeiboImgParser(),
    'img_path': WeiboImgParser(),
    'shanghai_tanking': ShanghaiRankingParser(),
}

