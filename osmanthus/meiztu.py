# @author medivh
# -*- coding:utf8 -*-
# 创建时间 2021/3/14 13:35

import requests
import random
from bs4 import BeautifulSoup
import re, os, os.path
import time

# 网址
meiztu_base_url = 'https://www.mzitu.com/'
# 选择器
# 分类页总页码
topic_page_numbers_selector = 'body > div.main > div.main-content > div.pagination > div > a.page-numbers'
# 主页显示列表
post_list_selector = '#pins > li'

# 图集总页码
subject_page_numbers_selector = 'body > div.main > div.content > div.pagenavi > a'
# 图集 标题
subject_name_selector = 'body > div.main > div.content > h2'
# 图集 分类
subject_classify_selector = 'body > div.main > div.content > div.main-meta > span:nth-child(1) > a'
# 图集 日期
subject_date_selector = 'body > div.main > div.content > div.main-meta > span:nth-child(2)'


# 图片下载地址
pic_download_selector = 'body > div.main > div.content > div.main-image > p > a > img'
# title选择器
simple_classify_selector_1 = '#menu-nav > li'
simple_classify_selector_2 = 'body > div.main > div.main-content > div.subnav > a'

# 专题选择器
topic_selector = 'body > div.main > div.main-content > div.postlist > dl > dd > a'
topic_url = 'https://www.mzitu.com/zhuanti/'

# 请求超时
time_out = 5
# 保存文件的根目录
root_path = 'D:\\MeiZiTu\\'

# 爬取间隔 毫秒
interval_lower_limit = 1000
interval_upper_limit = 1200

#休息间隔
rest_interval = 60

# 图片扩展名
extension_name = '.jpg'
sess = requests.session()
sess.keep_alive = False
def get_random_header():
    my_headers = [
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 '
        'Safari/533.21.1']
    return random.choice(my_headers)


def get_request(target_url,sleep=True):
    """

    :param target_url:
    :param sleep:
    :return:
    """
    header = {"User-Agent": get_random_header(),
              'authority': 'www.mzitu.com',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'cache - control': 'max - age = 0',
              'cookie': 'Hm_lvt_cb7f29be3c304cd3bb0c65a4faa96c30=1615809726,1615848017,1615897665,1615990290; Hm_lpvt_cb7f29be3c304cd3bb0c65a4faa96c30=1615990290',
              'dnt': '1',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'none',
              'sec-fetch-user': '?1',
              'upgrade-insecure-requests': '1',
              'sec-fetch-site': 'same-origin'
              # 'Referer': 'http://www.mzitu.com'
              }
    if sleep:
        sleep = random.randint(interval_lower_limit, interval_upper_limit) / 1000
        # print('等待 %s s' % sleep)
        time.sleep(sleep)
    r = requests.get(target_url, headers=header, timeout=time_out)
    return r

def printCurrentTime():
    print('CurrentTime：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),end='\t')

def get_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_url_soup(soup_url,sleep=True):
    r = get_request(soup_url,sleep)
    return get_soup(r.text)


def get_local_html_soup(html_name):
    file = open(html_name, 'rb+')
    return BeautifulSoup(file.read(), 'html.parser')


def create_directory(subject):
    """
    # 根据主题创建目录
    :param subject: 主题
    :return: 目录名称
    """
    try:
        dir_name = root_path + re.sub('[\/:*?"<>|]','\'',subject)
        printCurrentTime()
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print('文件夹 [%s] 创建成功！' % dir_name)
        else:
            print('文件夹 [%s] 已存在！' % dir_name)
        return dir_name
    except Exception as e:
        printCurrentTime()
        print('文件夹创建失败', e)


# 保存单个文件
def save_pic(pic_url, filename):
    try:
        if os.path.exists(filename) and os.path.getsize(filename):
            printCurrentTime()
            print('文件 [%s] 已存在！' % filename)
        else:
            with open(filename, 'wb') as fb:
                pic_download_url = get_url_soup(pic_url).select(pic_download_selector)[0]['src']
                fb.write(get_request(pic_download_url).content)
                printCurrentTime()
                print('图片 [%s] 保存成功！' % filename)
    except Exception as e:
        printCurrentTime()
        print('文件保存失败', e)


def getSimpleClassify():
    """
    获取简单的分类
    :return:
    """
    soup = get_local_html_soup('index.html')
    for item in soup.select(simple_classify_selector_2)[0:3]:
        print('Title: %s, url: %s' % (item.string, item['href']))
    for item in soup.select(simple_classify_selector_1)[1:5]:
        print('Title: %s, url: %s' % (item.a['title'], item.a['href']))


def getTopics():
    """
    专题分类
    :return:
    """
    # soup = get_url_soup(topic_url)
    soup = get_local_html_soup('topic.html')
    for item in soup.select(topic_selector):
        print('Topic: %s, url: %s' % (item.img['alt'], item['href']))


def get_total_page(page_url):
    """
    获取总页码数
    :param page_url: 目标url
    :param is_main_page: 是否是主页
    :return: 总页码值
    """
    base_sp = get_url_soup(page_url,False)
    page = base_sp.select(subject_page_numbers_selector if re.match('\d', page_url.split('/')[-1]) else topic_page_numbers_selector)
    if page:
        return page[-2].string
    else:
        return 1

def getAllSubjectsUnderTopic(topicUrl,total = 0):
    """
    获取总分类url
    :param total: 要爬取的页数，默认为0， 爬取全部
    :param topicUrl:
    :return:
    """
    total_page = int(get_total_page(topicUrl))
    if total and total < total_page:
        total_page = total

    urls = []
    for i in range(1,total_page + 1):
        print('---- 第 %s 页 -----' % i)
        targetUrl = topicUrl + 'page/' + str(i)
        base_sp = get_url_soup(targetUrl,False)
        postList = base_sp.select(post_list_selector)
        for item in postList:
            print(item.a.img['alt']+ ':' +item.a['href'])
            urls.append(item.a['href'])
    return urls


def getPicPackageToLocal(base_url):
    """
    单个图集爬取
    :param base_url:当前图集url
    :return:
    """
    sub_url = base_url + '/'
    #单个 图集 标题
    soup = get_url_soup(base_url)
    subject = soup.select_one(subject_name_selector).string
    classify = soup.select_one(subject_classify_selector).string
    #日期 例：['发布于', '2021-03-12', '23:05']
    date = soup.select_one(subject_date_selector).string.split(' ')
    subject = '[' + classify + '] ' + subject
    total_page = get_total_page(base_url)
    printCurrentTime()
    print('当前标题：%s, 共 %s 页' % (subject, total_page))
    directory_name = create_directory(subject + '_' + total_page + 'p')
    for i in range(1, int(total_page) + 1):
        try:
            file_name = directory_name + '/' + str(i) + extension_name
            pic_url = sub_url + str(i)
            save_pic(pic_url, file_name)
        except Exception as e:
            print(e)
            haveARest(rest_interval)


def haveARest(second):
    printCurrentTime()
    print('休息 %s s……' % second)
    time.sleep(second)

def getTopicPics(topicUrl,start=0, total=1):
    """
    获取当前专题所有
    :param start:
    :param topicUrl: 专题url
    :param total: 爬取页数 ，默认值1
    :return:
    """

    urls = getAllSubjectsUnderTopic(topicUrl,total)
    for url in urls[start:]:
        try:
            getPicPackageToLocal(url)
        except Exception as e:
            print(e)
            haveARest(rest_interval)

if __name__ == '__main__':
    pass
    # getSimpleClassify()
    # getPicPackageToLocal('https://www.mzitu.com/231042')

    best = 'https://www.mzitu.com/best/'
    hot = 'https://www.mzitu.com/hot/'
    latest = 'https://www.mzitu.com/'
    getAllSubjectsUnderTopic(best)
    # getTopicPics('',0,0)
    # getTopicPics('',0,0)
    # getTopicPics('',0,0)
    # getTopicPics('https://www.mzitu.com/tag/meitun/',6)
    # getAllSubjectsUnderTopic('https://www.mzitu.com/tag/meitun/',6)
    # getTopics()
    # getPicPackageToLocal(meiztu_base_url + '231935')
    # print(page)
    # getMeizituCatagory(picurl)
    # dirname = create_file('test')
    # save_pic(picurl,os.path.join(dirname,'1.jpg'))
    # pic_src = get_soup(picurl)
    # print(pic_src)
