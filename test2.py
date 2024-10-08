import requests

proxies = [
    'a968.kdltps.com:15818'
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    # 'Cookie': 'bid=lMoU-zG5PyM; ap_v=0,6.0; ll="118318"; _pk_ref.100001.4cf6=["","",1629127326,"https://www.douban.com/search?q=%E8%B5%B7%E9%A3%8E%E4%BA%86"]; _pk_id.100001.4cf6=dc9bc732d899e6b0.1629127326.1.1629127326.1629127326.; _pk_ses.100001.4cf6=*; __utma=30149280.44131403.1629127326.1629127326.1629127326.1; __utmc=30149280; __utmz=30149280.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __utma=223695111.1271915937.1629127326.1629127326.1629127326.1; __utmb=223695111.0.10.1629127326; __utmc=223695111; __utmz=223695111.1629127326.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; __gads=ID=577f92e35a24ede4-226a22dfcfca00e9:T=1629127330:RT=1629127330:S=ALNI_MZjLpS9mRSkcArTIkN5ovX4MmgbSg; _vwo_uuid_v2=D8D767506C7ADFF6F529102491C4ABD70|620d2d0e0c1be943504124c4fabda8f2; __utmt=1; __utmb=30149280.2.9.1629127342196',
}
file = open('ip_pool.txt', 'wb')
def test_proxy(proxy):
    '''测试代理IP是否可用'''
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'https://{}'.format(proxy),
    }
    # 参数类型
    # proxies
    # proxies = {'协议': '协议://IP:端口号'}
    # timeout 超时设置 网页响应时间3秒 超过时间会抛出异常
    try:
        resp = requests.get(url='http://httpbin.org/get', proxies=proxies, timeout=3)
        # 获取 状态码为200
        if resp.status_code == 200:
            print(proxy, '\033[31m可用\033[0m')
            # 可以的IP 写入文本以便后续使用
            file.write(proxy)

        else:
            print(proxy, '不可用')

    except Exception as e:
        print(proxy, '不可用')


if __name__ == '__main__':
    for proxy in proxies:
        test_proxy(proxy)