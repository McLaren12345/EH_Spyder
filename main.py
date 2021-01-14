# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:02:52 2021

@author: McLaren
"""

from Doujinshi import *
import os


def read_download_list():
    with open(os.path.join(os.path.abspath('.'), 'download_list.txt'), "r") as f:
        data = f.readlines()
        return data


def main():
    download_list = read_download_list()
    for doujinshi in download_list:
        file = Doujinshi(doujinshi.strip('\n'))
        try:
            file.decode().save_all()
        except:
            logger.error('Fail download' + doujinshi)


if __name__ == '__main__':
    main()
