# PixivSpider
一个P站爬虫，练手作，比我好用的爬虫多了去了  
## 依赖项：
#### bs4/requests/lxml  
当然，您还要安装python和pip  
用以下指令来安装依赖项:  
```
$ pip install bs4  
$ pip install requests  
$ pip install lxml  
```
## 关于config配置:
运行一次__init__之后，会生成一个config文件  
用记事本打开并修改里面的配置  
目前为止，proxy代理服务是必须要有的，其中的host项代表主机地址，port项代表端口  
另外，cookie项可以选填，不填的话就是游客登陆，目前没有做爬关注画师的功能，所以应该影响不大  
account项完全不用填，因为绕不过google验证，这个功能暂时放着  
***
~~*大概就是这些了吧*~~
***
