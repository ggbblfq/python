#-*- coding:utf-8 -*-
import re
import requests
from lxml import html
import urllib3
import oss2

#url = 'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1460997499750_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%B0%8F%E9%BB%84%E4%BA%BA'
#url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=苹果电脑&ct=201326592&v=flip'
#url = 'http://creative.quanjing.com/creative/#汽车背景-室内空间明亮'

#html = requests.get(url).text
#pic_url = re.findall('"objURL":"(.*?)",',html,re.S)

#pic_url = re.findall('<a.*?href="([^"]*)".*?>([\S\s]*?)</a>',html,re.S)

page = requests.get('https://unsplash.com/',headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' })

tree = html.fromstring(page.text)

#intro_raw = tree.xpath('//*[@class="media"]/img/@scr')
intro_raw = tree.xpath('//*[@class="cV68d"]//@style')

#print('图片地址:',intro_raw)
i = 0
for each in intro_raw:
    #替换一些多余的字符串
    each = each.replace('background-image:url("','')
    each = each.replace(');width:0;height:0', '')
    # arr = each.split('?')
    # each = arr[0]
    #打印地址
    print (each)
    try:
        pic= requests.get(each, timeout=20)
    except requests.exceptions.ConnectionError:
        print ('【错误】当前图片无法下载')
        continue
    # string = 'pictures\\'+str(i) + '.jpg'
    # fp = open(string,'wb')
    # fp.write(pic.content)
    # fp.close()

    string = 'pictures\\' + str(i) + '.jpg'
    name = str(i) + '.jpg'
    auth = oss2.Auth('xxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxx')
    bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'xxxxxxxxxx')
    # with open(string, 'wb') as fileobj:
    result = bucket.put_object(name, pic.content)
    print('http status: {0}'.format(result.status))

    i += 1

def fetch_links(furl,burl,stag,etag):
    '''''
    抓取网页新闻
    @param furl 抓取网页地址
    @param burl 网页链接的baseurl,比如凤凰网的链接:<a href="/news/guoji/dir?cid=14&amp;mid=7sdLRL">国际</a>, 根据baseurl可返回<a href="http://i.ifeng.com/news/guoji/dir?cid=14&amp;mid=7sdLRL">国际</a>
    @param stag 抓取网页链接的开始标签
    @param etag 抓取网页链接的结束标签
    @return 加了baseurl的链接列表
    说明: 正则表达式中 '.*?', 采用非贪婪模式匹配多个字符
    '''
    req = urllib3.Request(furl)
    fd = urllib3.urlopen(req)
    content = fd.read()
    fd.close()
    m = re.findall(stag+'.*?'+etag,content)
    return  [j.replace('<a href="', '<a href="'+burl) for j in m]