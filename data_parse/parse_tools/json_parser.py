"""
解析json字符串
"""
import json
import datetime
import pandas as pd


def read_json_file(json_path):
    file = open(json_path, 'r', encoding='utf-8')
    s = json.load(file)
    return s



