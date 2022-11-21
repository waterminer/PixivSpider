import configparser
import os
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import ProxyError

config = configparser.ConfigParser()
config_raw = configparser.RawConfigParser()
config_path = "./config/connect.config"
base_url = "https://www.pixiv.net"
rank_url = "https://www.pixiv.net/ranking.php"
login_url = "https://accounts.pixiv.net/login"
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


# 总算是封装了一个类，每次链接都被迫要往参数里填代理实在是太蠢了
class Connect:

    # 尝试利用代理网络连接pixiv,返回一个proxies
    def _get_proxy(self):
        config.read(config_path, encoding='utf-8')
        host = config['proxy']['host']
        port = ':' + config['proxy']['port']
        proxy_host = host + port
        self._proxies = {'http': proxy_host, 'https': proxy_host}
        return

    def __init__(self):
        self._proxies = None
        self._cookie = None
        self._get_proxy()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
            'referer': 'https://www.pixiv.net/'
        }
        print("正在尝试连接pixiv...")
        try:
            test = requests.get(base_url, headers=self._headers, proxies=self._proxies)
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

            else:
                print("请求失败:返回码_", re_code)
                exit(1)

    # 实际上并没有用到的cookies
    def cookies_login(self):
        config_raw.read("./config/connect.config", encoding='utf-8')
        self._cookie = config_raw['cookie']['cookie']
        self._headers['cookie'] = self._cookie.encode('utf-8')
        return

    def ask_url(self, url):
        html = req.get(url, headers=self._headers, proxies=self._proxies)
        return html


# 以下代码暂时废弃（一脚踢google验证钢板上，除非有大佬能解决这个问题)
'''
def account_login(proxies):
    print('该功能开发中...')
    
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
