#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import threading
import time
import queue


class Scanner():
    def __init__(self, url_path, file_path, num):
        self.url_path = url_path
        self.file_path = file_path
        self.num = num
        self.files = []
        self.urls = []
        self.result = []
        self.q = queue.Queue()
        self.head = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Cache-Control': 'no-cache',
        }
        self.loadFile(self.url_path, self.urls) #载入url列表
        self.loadFile(self.file_path, self.files) #载入字典列表
        self.savePathToQ()    #初始化队列

        for _ in range(self.num):
           threading.Thread(target=self.run).start()

    def loadFile(self, path, array):
        try:
            with open(path, "r", encoding='gbk') as file:
                for url in file.readlines():
                    str = url.replace('\n', '')
                    array.append(str)
        except IOError:
            print("not found file" + path)

    #初始化队列数据
    def savePathToQ(self):
        for url in self.urls:
            for dict in self.files:
                dict = dict.strip('/')
                data = {}
                data['host'] = url
                data['dict'] = dict
                self.q.put(data)

    def run(self):
        while not self.q.empty():
            data = self.q.get()
            try:
                response = requests.head(data['host'] + data['dict'], headers=self.head)
                time.sleep(0)
                print(response.url.replace('%0A', ' '), response.status_code)
                if response.status_code == 200 or response.status_code == 403:
                    self.result.append(data['host'] + data['dict'] + '\n')
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.ReadTimeout:
                pass
            except Exception as e:
                pass
        print('扫描结束-------------')
        self.saveResult()

    def saveResult(self):
        try:
            with open('./res.txt', 'w+', encoding='utf8') as file:
                file.writelines(self.result)
        except IOError:
            print("open file failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = '简单的多线程网站目录扫描--------'
    parser.add_argument('-u', '--url.txt', dest='url_path', help='要扫描的url列表文件', type=str)
    parser.add_argument('-f', '--scan_file_url', dest='scan_file_url', help='载入扫描的字典文件',
                        type=str)
    parser.add_argument('-t', '--thread', dest='thread', help='运行程序的线程数量', type=int, default=5)
    args = parser.parse_args()
    scanner = Scanner(args.url_path, args.scan_file_url, args.thread)
