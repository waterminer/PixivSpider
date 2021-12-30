from src import connect
from src import data


def menu():
    temp = input("请选择爬虫模式：(0~2)\n1.爬取日榜\n2.下载图片\n0.退出\n") or 0
    i = int(temp)
    if i == 0:
        exit(0)
    elif i == 1:
        temp = int(input("请选择爬取页数:(1~6,默认为2)\n一页50个结果\n最大是6，为了虫虫们的未来！\n") or 2)
        if (temp >= 1) & (temp <= 6):
            print("开始爬取日榜数据")
            num = temp
            database = data.get_rank(proxy, num)
            temp = int(input("当遇到图集时，是否要爬取该图集所有图片?（默认:否）\n1.是\n2.否\n") or 2)
            if temp == 1:
                num = 1
            elif temp == 2:
                num = 0
            else:
                print("选项错误！\n")
                menu()
            data.get_rank_picture_source(database, proxy, num)
        else:
            print("输入的值超出范围！\n")
            menu()
    elif i == 2:
        temp = input("请输入要下载的图片：(图片ID)\n")
        artworks_id = str(temp)
        data.get_picture_source(artworks_id, proxy)

'''
#废弃的菜单
def menu2():
    # 登录菜单
    temp = input('请选择登录方式（0～1）\n1.账号登录\n2.cookie登录\n3.游客登录\n0.退出\n')
    i = int(temp)
    if i == 0:
        exit(0)
    elif i == 1:
        connect.account_login()
    elif i == 2:
        connect.cookies_login()
        data.get_rank()
        exit(0)
    elif i == 3:
        print("功能尚未实现")
        exit(0)
    else:
        print("错误输入！")
        exit(1)
'''

if __name__ == '__main__':
    print("正在初始化")
    connect.get_config()
    proxy = connect.use_proxy()
    connect.cookies_login()
    menu()
    print("done!")
