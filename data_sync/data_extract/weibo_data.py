


# 获取绘画信息
import json

from config import db_map
db = db_map.get('weibo_data')


def get_img_data(name=None, img_url=None, return_type='map', return_value=None):
    sql = """
    select *
    from t_img_info
    where 1=1
    """
    if name:
        sql += """ and name = '{name}' """.format(name=name)
    elif img_url:
        sql += """ and img_url = '{img_url}' """.format(img_url=img_url)

    data = db.query(sql)
    if return_type == 'map':
        data_map = {}
        for item in data:
            if return_value == 'img_name':
                img_name = item['img_name']
                data_map[item['img_url']] = img_name
        return data_map
    else:
        return data


def get_poetry_img(content=None, return_type=None):
    # 内容筛选
    sql = """
    select *
    from t_blog_info
    where 1=1
    """
    data = db.query(sql)
    filter_data = [item for item in data if content in item['content_text']]
    all_id_list = []
    for item in filter_data:
        id_list = json.loads(item['img_ids_str'])
        all_id_list.extend(id_list)

    url_list = []
    for id in all_id_list:
        url = """https://wx3.sinaimg.cn/orj1080/{img_code}.jpg""".format(img_code=id)
        url_list.append(url)
    # sql = """ select img_url from t_img_info where 1=1 and img_type='original' and img_code in ('{codes}')
    # """.format(codes="','".join(all_id_list))
    # data = db.query(sql)

    # if return_type == 'list':
    #     return [item['img_url'] for item in data]
    # else:
    #     return data
    return url_list


if __name__ == '__main__':
    data = get_poetry_img(content='快来看看最打动你的作品是哪首', return_type='list')
    print(data)