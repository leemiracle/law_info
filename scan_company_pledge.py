#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-27
@Author  : leemiracle
"""
import requests


def download_xls():
    file_path = ""
    url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate=2018.09.20&type=proportion'
    r = requests.get(url, stream=True)
    print(r.text)

def main():
    download_xls()


if __name__ == '__main__':
    main()
