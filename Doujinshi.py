# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:02:52 2021

@author: McLaren
"""

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import threading
import configparser
import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': '__cfduid=d0665d2559063760e94951467e6f85e901610423569; ipb_member_id=5666431; ipb_pass_hash=4e29adc0443606aee2947e7903e9c3b9; sk=giw0bfxmqti2za4qbd6q4mi2swfn; event=1610590658; nw=1',
    'Upgrade-Insecure-Requests': '1'}

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(os.path.abspath('.'), 'log.txt'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def save_file(reference, url, path):
    try:
        response = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(response.content)
            f.flush()
    except:
        logger.warning('Fail download ' + reference + ' - ' + path.split('/')[-1])


def get_img_url(url):
    site_2 = requests.get(url, headers=headers)
    content_2 = site_2.text
    soup_2 = BeautifulSoup(content_2, 'lxml')
    imgs = soup_2.find_all(id="img")
    for img in imgs:
        picSrc = img['src']
        return picSrc


def get_img_on_single_page(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    return divs


class Doujinshi:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.pages = 0
        self.divs = 0
        self.download_dir = ""
        self.max_thread = 15
        self.config_file = configparser.ConfigParser()
        self.config_file.read(os.path.join(os.path.abspath('.'), 'config.ini'))
        self.init_config()

    def init_config(self):
        self.download_dir_init()
        self.max_thread_init()

    def max_thread_init(self):
        try:
            max_thread = self.config_file.get('sysinfo', 'max_threading')
            if max_thread == '':
                self.max_thread = 15
            else:
                self.max_thread = int(max_thread)
        except Exception as ex:
            self.max_thread = 15

    def download_dir_init(self):
        try:
            self.download_dir = self.config_file.get('dirpath', 'dirpath')
            if self.download_dir == '':
                self.download_dir = os.path.abspath('.') + '/Download'
        except Exception as ex:
            self.download_dir = os.path.abspath('.') + '/Download'

        if not self.download_dir.endswith('/'):
            self.download_dir = self.download_dir + '/'

    def title_regular(self):
        self.title = self.title.split('>')[1].split('<')[0].replace('?', ''). \
            replace('/', ' ').replace(':', ' ').replace('*', '').replace('\\', ' ')

    def decode(self):
        site = requests.get(self.url, headers=headers)
        content = site.text
        soup = BeautifulSoup(content, 'lxml')
        self.pages = int(soup.find('div', id='gdd').find_all(class_="gdt2")[5].string.split(' ')[0])
        self.title = str(soup.find('h1', id='gj').get_text) \
            if str(soup.find('h1', id='gj').get_text).split('>')[1].split('<')[0] != '' \
            else str(soup.find('h1', id='gn').get_text)
        self.title_regular()
        self.divs = soup.find_all(class_='gdtm')
        # 超过40page的图片会分页，要继续读取后续的页
        for i in range((self.pages - 1) // 40):
            self.divs.extend(get_img_on_single_page(self.url + '?p=' + str(i + 1)))

        return self

    # 多线程下载
    def save_all_img_thread(self):
        pool = []
        page = 0
        print('Start downloading ' + self.title)
        for div in tqdm(self.divs):
            picUrl = div.a.get('href')
            page = page + 1
            t = threading.Thread(target=save_file,
                                 args=(self.url, get_img_url(picUrl),
                                       self.download_dir + self.title + '/' + str(page) + '.jpg'))
            pool.append(t)
            t.start()
            while True:
                if len(threading.enumerate()) < self.max_thread:
                    break

        for x in pool:
            x.join()

    def save_all(self):
        if os.path.exists(self.download_dir + self.title):
            logger.info(self.url + ' has already been downloaded')
            print('This Doujinshi has already been downloaded')
        else:
            os.makedirs(self.download_dir + self.title)
            self.save_all_img_thread()


if __name__ == '__main__':
    test = Doujinshi('https://e-hentai.org/g/1673340/f0af79843d/')
    test.decode().save_all()
