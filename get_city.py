import requests
import sys


def get_CityName():
    try:
        res = requests.post(url='http://ip-api.com/json/?lang=zh-CN', data={'ip': 'myip'}, timeout=10)
        result = res.json()['city']
        if result == '北京':
           result = '上海'
    except:
        print(" [!]正在进行网络自检并重试")
        try:
            res = requests.post(url='http://ip-api.com/json/?lang=zh-CN', data={'ip': 'myip'}, timeout=15)
            result = res.json()['city']
        except:
            print(" [!]无法从相关网站获得请求(请求总时长：25s)，退出脚本")
            sys.exit(1)

    if len(result) == 0:
        print(' [!] 未自动匹配到你所在地的地区信息:' + result)
    return result
