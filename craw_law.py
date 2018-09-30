#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-18
@Author  : leemiracle
"""
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyquery import pyquery as pq

ua = UserAgent()
user_agent = ua.chrome

headers = {
    'User-Agent': user_agent,
    'From': ''  # This is another valid field
}


def craw_country_law():
    # 维基法律列表:https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B3%95%E5%BE%8B%E5%88%97%E8%A1%A8
    base = 'https://www.chinacourt.org'
    base_uri = base + '/law.shtml'
    headers['From'] = base
    ret = requests.get(base_uri, headers=headers)  # index info

    doc = BeautifulSoup(ret.text, 'html.parser')
    projects = {'立法追踪': 'law_follow', '国家法律法规': "chinese_law", '地方法规': 'local_law', '司法解释': "explain_law", '中外条约': "law_between_chinese_and", '政策参考': 'policy_reference'}
    project = '政策参考'
    sub_uri = ''
    for link in doc.find_all('a'):
        if link.text == project:
            sub_uri = link.get('href')
            break
    uri = base + sub_uri
    headers['From'] = base
    country_doc = requests.get(uri, headers=headers)
    sub_doc = BeautifulSoup(country_doc.text, 'html.parser')
    # start_index = 1
    last_index = 1
    suffix = ''
    content_uri = ''
    for link in sub_doc.find_all('a'):
        if link.text == '尾页':
            last_uri_page = link.get('href')
            infos = last_uri_page.split('/')
            suffix = '.' + infos[-1].partition('.')[-1]
            content_uri = '/'.join(infos[:-1])
            last_index = int(infos[-1].partition('.')[0])
            break
    print(last_index)
    for i in range(625, 0, -1):
        uri = base + content_uri + '/' + str(i)+suffix
        print(uri)
        headers['From'] = base
        laws = requests.get(uri, headers=headers)
        soup = BeautifulSoup(laws.text, 'lxml')
        hrefs = soup.select('li > span > a')
        headers['From'] = uri
        for law_href in hrefs:
            try:
                law_uri = law_href.get('href')
                law_name = law_href.text
                print(law_name, law_uri)
                content = requests.get(base + law_uri, headers=headers)
                with open('{}/'.format(projects[project]) +law_name +'.shtml', "w") as f:
                    f.write(content.text)
            except Exception as e:
                pass
            time.sleep(0.5)

    # 国家法律法规/地方法规/司法解释/中外条约/政策参考

    # # https://www.chinacourt.org/law/more/law_type_id/MzAwNEAFAA%3D%3D/page/1.shtml
    # base_uri = 'https://www.chinacourt.org/law/more/law_type_id/MzAwNEAFAA%3D%3D/page/{page}.shtml'.format(page=1)
    # requests.get(base_uri)


def main():
    # 法律法规信息库: https://www.chinacourt.org/law.shtml
    # 党政机关公文处理工作条例(公文处理):http://www.gov.cn/zwgk/2013-02/22/content_2337704.htm
    # 中华人民共和国法律列表: https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B3%95%E5%BE%8B%E5%88%97%E8%A1%A8
    # 政府工作报告:http://www.gov.cn/guowuyuan/baogao.htm
    craw_country_law()


if __name__ == '__main__':
    main()
