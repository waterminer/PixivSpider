import configparser
import os
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import ProxyError

config = configparser.ConfigParser()
config_raw = configparser.RawConfigParser()
config_path = "./config/connect.config"
base_url = "https://www.pixiv.net"
rank_url = "https://www.pixiv.net/ranking.php"
login_url = "https://accounts.pixiv.net/login"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    'referer': 'https://www.pixiv.net/'
}
req = requests.session()


# 初始化config文件
def get_config():
    if not os.path.exists("./config/connect.config"):
        if not os.path.exists("./config"):
            os.makedirs("./config")
        config['proxy'] = {
            'host': '127.0.0.1', 'port': '0000'
        }
        config['account'] = {
            'pixiv_id': '这项不必填写', 'password': '这项不必填写'
        }
        config['cookie'] = {
            'cookie': ''
        }
        with open(config_path, 'w', encoding='utf-8') as file:
            config.write(file)
        input('请配置设置文件："config/connect.config"') or 0
        exit(1)
    else:
        return config


# 尝试利用代理网络连接pixiv,返回一个proxy（其实是懒得用类来封装了）
def use_proxy():
    print("正在尝试连接pixiv...")
    config.read(config_path, encoding='utf-8')
    host = config['proxy']['host']
    port = ':' + config['proxy']['port']
    proxy_host = host + port
    proxies = {'http': proxy_host, 'https': proxy_host}  # 左边那堆玩意儿是拿来组装代理地址的
    try:
        test = requests.get(base_url, headers=headers, proxies=proxies)
    except ProxyError:
        print("连接失败，请检查网络连接或代理配置！")
        exit(1)
    except ConnectionError:
        print("连接失败，请检查网络连接或代理配置！")
        exit(1)
    else:
        re_code = test.status_code
        if re_code == 200:
            print("OK")
            return proxies
        else:
            print("请求失败:返回码_" + re_code)
            exit(1)


# 以下代码暂时废弃（一脚踢google验证钢板上，除非有大佬能解决这个问题)
def account_login(proxies):
    print('该功能开发中...')
    '''
    print('正在尝试登录pixiv')
    data_re = req.get(login_url, headers=headers, proxies=proxies)
    login_soup = BeautifulSoup(data_re.text, 'lxml')
    config.read(config_path)
    pixiv_id = config['account']['pixiv_id']
    password = config['account']['password']
    post_key = login_soup.find('input')['value']
    data = {
        'pixiv_id': pixiv_id,
        'password': password,
        'post_key': post_key
    }
    data_re = req.post("https://accounts.pixiv.net/api/login?lang=zh", data=data, headers=headers, proxies=proxies)
    print(data_re.test)
    config['cookie']['device_token'] = data_re.cookies['device_token']
    config['cookie']['PHPSESSID'] = data_re.cookies['PHPSESSID']
    '''


def cookies_login():
    config_raw.read("./config/connect.config", encoding='utf-8')
    cookie = config_raw['cookie']['cookie']
    headers['cookie'] = cookie.encode('utf-8')
    return


def ask_url(url, proxies):
    html = req.get(url, headers=headers, proxies=proxies)
    return html
