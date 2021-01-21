# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:02:52 2021

@author: McLaren
"""

from Doujinshi import *
import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import win32api
import psutil


def read_download_list():
    with open(os.path.join(os.path.abspath('.'), 'download_list.txt'), "r") as f:
        data = f.readlines()
        return data


def gen_download_list(url):
    new_list = E_filter(url)
    new_list.decode().save_download_list()


def download():
    def proc_exist(process_name):
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                return True
        return False

    if not proc_exist('v2rayN.exe'):
        win32api.ShellExecute(0, 'open', 'C:\\v2ray-windows-64\\v2rayN.exe', '', '', 0)
        time.sleep(5)
    start = time.time()
    download_list = read_download_list()
    limit = 150 if len(download_list) >= 150 else len(download_list)
    for i in range(limit):
        if download_list[i].find('http') == -1:
            continue
        file = Doujinshi(download_list[i].strip('\n'))
        try:
            file.decode().save_all()
        except SystemExit as ex:
            print('Error 509 - Reach limit of 5000 pages. %d doujinshi have downloaded.' % (i + 1))
            logger.warning('509 - Reach limit of 5000 pages.')
            sys.exit(0)
        except:
            logger.error('Fail download ' + download_list[i].strip('\n'))
    end = time.time()
    print('Finish download {} doujinshi.'.format(limit) + ' Total time cost: %d minus %d seconds.'
          % ((end - start) // 60, (end - start) % 60))


def main(scheduled_time=None):
    if scheduled_time is not None:
        scheduler = BlockingScheduler()
        scheduled_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        scheduler.add_job(download, 'date', run_date=scheduled_time)
        print('Download task scheduled at ' + scheduled_time)
        scheduler.start()
    else:
        download()


if __name__ == '__main__':
    gen_download_list('https://exhentai.org/?f_cats=264&f_search=parody%3A%22himouto+umaru-chan%24%22+lang%3A%22chinese%22')
    # main()
