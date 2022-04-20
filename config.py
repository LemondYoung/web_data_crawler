

from settings import WEIBO_DB_CONFIG
from data_parse.weibo_parser import WeiboBlogParser
from utils.database.mysql import Mysql

parser = {
    'weibo_blog': WeiboBlogParser(),
}

db_map = {
    'weibo_data': Mysql(**WEIBO_DB_CONFIG),
    'douban_data': Mysql(**WEIBO_DB_CONFIG),
}