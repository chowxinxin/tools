"""
字典加网页收录
"""
import dns.resolver
import queue
import threading
import requests
from lxml import etree

#字典
def run(url):
    subdomain = q.get()
    str_list = [subdomain, url]
    ch = '.'

    try:
        A = dns.resolver.resolve( ch.join(str_list), "A")
        for i in A.response.answer:
            print(i)
    except Exception as e:
        pass


def loadFile():
    with open('./domain.txt', 'r', encoding='gbk') as file:
        for i in file.readlines():
            str = i.replace('\n', '')
            q.put(str)

#爬行
def crawl():
    while not q2.empty():
        rep = requests.get(q2.get(), headers=header)
        code = etree.HTML(rep.text)
        div = code.xpath('//div[@class="f13 c-gap-top-xsmall se_st_footer user-avatar"]')
        for element in div:
            a = element.xpath('./a[1]')
            for attr in a:
                domain = attr.xpath('@href')
                reps = requests.get(domain[0], headers=header)
                print(reps.url)

if __name__ == '__main__':

    q = queue.Queue()
    loadFile()
    url ="https://www.baidu.com/s?wd=site:zhongkrg.cn&pn="
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    q2 = queue.Queue()
    for i in range(100):
        q2.put(url + str(i * 10))

    #开启线程
    for _ in range(20):
        threading.Thread(target=run, args=("zhongkrg.cn",)).start()
        threading.Thread(target=crawl).start()
