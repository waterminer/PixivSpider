from _datetime import datetime
from bs4 import BeautifulSoup
from src import connect
import os
import re
import json

# 定义常量
now = datetime.now()
time = now.strftime("%Y%m%d_%H%M%S")
date_now = now.strftime("%Y%m%d")
path = './Downloads'
# 提取规则
rank_re = re.compile(r'data-rank="(.*?)"')
date_re = re.compile(r'data-date="(.*?)"')
title_re = re.compile(r"(?<=data-title=\"|data-title=\')(.*)(?=\" data-user-name=|\' data-user-name=)")
artist_re = re.compile(r'data-user-name="(.*?)"')
view_count_re = re.compile(r'data-view-count="(.*?)"')
id_re = re.compile(r'data-id="(.*?)"')
original_re = re.compile(r'"original":"(.*?)"')
ext_re = re.compile(r'(jpg|png|gif)')


# 获取榜单的方法
def get_rank(proxies, num, database={}):
    for i in range(1, num + 1):
        i = str(i)
        rank_url = 'https://www.pixiv.net/ranking.php?p=' + i
        req = connect.ask_url(rank_url, proxies)
        rank_bs = BeautifulSoup(req.text, "lxml")
        for section in rank_bs.find_all("section", class_="ranking-item"):
            item = str(section)
            rank = re.findall(rank_re, item)[0]
            artworks_id = re.findall(id_re, item)[0]
            title = re.findall(title_re, item)[0]
            artist = re.findall(artist_re, item)[0]
            date = re.findall(date_re, item)[0]
            view = re.findall(view_count_re, item)[0]
            item_data = {
                'rank': rank,
                'id': artworks_id,
                'title': title,
                'artist': artist,
                'date': date,
                'view': view
            }
            database[artworks_id] = item_data
            '''
            # 以下用于检查输出结果
            print("#" + rank + "\ntitle: " + title + "\nartist: " + artist + "\nid: " + id + "\ndate: " + date + 
                  "\nview: " + view + "\n") 
            '''
    return database


# 保存图片的方法
def save(picture, name, ext):
    print("正在保存这张图： " + name)
    if not os.path.exists(path):
        os.makedirs('Downloads')
    save_path = path + '/' + str(name) + '.' + ext
    with open(save_path, 'wb') as fp:
        try:
            fp.write(picture)
        except Exception as e:
            print(e)
        fp.close()


# 下载榜单图片的方法
def get_rank_picture_source(database, proxies, switch=0):
    for artworks_id in database:
        url = 'https://www.pixiv.net/ajax/illust/' + artworks_id + '/pages?lang=zh'
        req = connect.ask_url(url, proxies)
        json_obj = json.loads(json.dumps(req.json()))
        i = 0
        if switch == 0:
            url = json_obj['body'][0]['urls']['original']
            ext = re.findall(ext_re, url)[0]
            picture = connect.ask_url(url, proxies)
            name = str(artworks_id + "_" + str(i))
            save(picture.content, name, ext)
        elif switch == 1:
            for urls_list in json_obj['body']:
                url = urls_list['urls']['original']
                ext = re.findall(ext_re, url)[0]
                picture = connect.ask_url(url, proxies)
                name = str(artworks_id + "_" + str(i))
                save(picture.content, name, ext)
                i = i + 1
        else:
            print("选项错误！")
            exit(1)


# 下载原图的方法
def get_picture_source(artworks_id, proxies):
    artworks_id = str(artworks_id)
    url = 'https://www.pixiv.net/ajax/illust/' + artworks_id + '/pages?lang=zh'
    req = connect.ask_url(url, proxies)
    json_obj = json.loads(json.dumps(req.json()))
    i = 0
    for urls_list in json_obj['body']:
        url = urls_list['urls']['original']
        ext = re.findall(ext_re, url)[0]
        picture = connect.ask_url(url, proxies)
        save(picture.content, artworks_id + "_" + str(i), ext)
        i = i + 1