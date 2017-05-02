# coding=utf-8

## 进入耳机页面进行疯狂的抓取，抓取深度为3
## 配置url规则

import re
import urllib.request
import logging
import urllib.parse
import time
import traceback
import os
from bs4 import BeautifulSoup

DEPTH = 3

##日志文件
LOG_PATH = "spider_log.log"
## 获取页面之后编码转换
PAGE_CODE = "GBK"

##爬虫每爬一个页面在该目录下写一个文件
FILE_BASE_PATH = "files/"

## 模拟火狐浏览器user-agent
U_A = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
HEADERS = {"User-Agent": U_A}

##初始化日志类
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_PATH)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# 设置console日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

linkHashMap = {}

values = {'wd': 'python',
          'opt-webpage': 'on',
          'ie': 'gbk'}
url_values = urllib.parse.urlencode(values)

url_values = url_values.encode(encoding='gb2312')

reg = "^http://news.carnoc.com/{1}[]$"


##读取抓取首页后的文章
def getIndexResult(filepath):
    file_obj = open(filepath)
    try:
        all_content = file_obj.read()
        return all_content
    except Exception as ex:
        print(ex)
    finally:
        file_obj.close()


p = re.compile(r"http://news.carnoc.com/(cache/)?(list/){1}(\w(/\w)*)+.html")


##深度挖掘数据，暂定为深度为3
def iteratorDrillData(content, depth):
    print("*******************当前深度：【" + str(depth) + "】*********************")
    if depth > 0:
        contentlist = content.split("\n")
        for con in contentlist:
            kv = con.split("\1")
            try:
                if len(kv) > 1 and kv[1]:
                    if "http://news.carnoc.com/" not in kv[1]:
                        kv[1] = kv[1]
                    logging.info("请求" + kv[1])
                    if kv[1] in linkHashMap:
                        break
                    htmlContent = getHtml(getRequestClass(kv[1], url_values))
                    if htmlContent:
                        alist = getTitleAndUrl(htmlContent)
                        newsBlock = getPageNewsSoup(htmlContent)
                        ## print(newsBlock)
                        if newsBlock:
                            fromSite = newsBlock.find_all()
                            publishDate = newsBlock.find_all()
                            author = newsBlock.find_all()
                            ##print(newsBlock[0])
                            newsText = newsBlock.find()
                            if newsText:
                                createNewFileAndWrite(mkdirBefore(kv[1][23:len(kv[1])]), str(newsText))
                                ##print(alist)
                        for m in alist:
                            if m and m[1] and p.match(m[1]):
                                try:
                                    print(m)
                                    iteratorDrillData(m[0] + "\1" + m[1], depth - 1)
                                except:
                                    continue
            except:
                traceback.print_exc()
                continue


def mkdirBefore(urlString):
    s = urlString.split("/")
    # lis = s[0:len(s)-1]
    # for i in range(0,len(s)-1):
    # if not os.path.exists(FILE_BASE_PATH+lis[i]):
    # os.mkdir(FILE_BASE_PATH+lis[i])
    # print("创建目录"+lis[i])
    print("写入目录文件：" + "html/" + s[-1])
    return "html/" + s[-1]


def getRequestClass(url, url_values):
    linkHashMap[url] = 2
    return urllib.request.Request(url, url_values, HEADERS)

    ##获取网页内容函数


def getHtml(req_url):
    try:
        response = urllib.request.urlopen(req_url)
    except:
        return None
    return response.read().decode("GBK")


##写文件函数
def createNewFileAndWrite(file_name, content):
    file_obj = open(FILE_BASE_PATH + file_name + ".txt", "w+")
    file_obj.write(content)
    file_obj.close()


##根据dom提取文章title和文章超链接
def getTitleAndUrl(newsHTML):
    resultList = []
    root = BeautifulSoup(newsHTML, "html.parser")
    tempa = root.find_all("a")
    for dom in tempa:
        kv = []
        href = dom.get("href")
        title = dom.string
        kv.append(title)
        kv.append(href)
        resultList.append(kv)
    return resultList


def getPageNewsSoup(htmlContent):
    return BeautifulSoup(htmlContent, "html.parser")

    ##http://news.carnoc.com/(cache/)?(list/){1}(\w)*(/\w)*.html


iteratorDrillData(getIndexResult("files/newslist-2017-04-27 .txt"), 3)