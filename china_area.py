#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-19
@Author  : leemiracle
"""
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
user_agent = ua.chrome

headers = {
    'User-Agent': user_agent,
    'From': ''  # This is another valid field
}


def above_xian_area_code():
    # 标准国家代码: https://zh.wikipedia.org/wiki/ISO_3166-1
    # 维基百科:
    # 中国行政区划: http://quhua.meililz.com/daima/daima-xian.php?sd=%E6%B9%96%E5%8D%97%E7%9C%81&xd=%E6%A0%AA%E6%B4%B2%E5%B8%82&cd=%E8%8C%B6%E9%99%B5%E5%8E%BF
    people = "http://www.mca.gov.cn/article/sj/xzqh/2018/"  # 行政区域划分  http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20180708230813.html
    "http://www.mca.gov.cn/article/sj/tjbz/b/"  # 国民经济行业划分 : http://www.stats.gov.cn/tjsj/tjbz/hyflbz



def crawl_area_name():
    sheng_flag = 'sheng.php'
    xian_flag = 'sheng.php'
    xiang_flag = 'xiang.php'
    base = 'http://quhua.meililz.com/'
    headers['From'] = base
    ret = requests.get(base, headers=headers)
    doc = BeautifulSoup(ret.text, 'html.parser')
    xian_dic = set()
    sheng_dic = set()
    for link in doc.find_all('a'):
        if sheng_flag in link.get('href'):
            sheng_dic.add(sheng_dic)
    prefix = 'xingzhengquhua/'
    for link in sheng_dic:
        uri = base + prefix+ link
        ret = requests.get(uri, headers=headers)
        doc = BeautifulSoup(ret.text, 'html.parser')


def main():
    """
    github项目: https://github.com/modood/Administrative-divisions-of-China
    :return:
    """
    region = {
        "华北": ["北京", "天津", "河北", "山西", "内蒙古"],
        "东北": ["辽宁", "吉林", "黑龙江"],
        "华东": ["上海", "江苏", "浙江", "安徽", "福建", "江西", "山东"],
        "华中": ["河南", "湖北", "湖南"],
        "华南": ["广东", "广西", "海南"],
        "西南": ["重庆", "四川", "贵州", "云南", "西藏"],
        "西北": ["陕西", "甘肃", "青海", "宁夏", "新疆"],
        "港澳台": ["香港", "澳门", "台湾"],
    }

def area_name_entity():
    xing_zheng = ['省', '市', '自治区', '区', '直辖市', '特别行政区', '副省级市辖新区', '地级市', '副省级城市', '副省级市', '地区', '自治州', '盟', '县', '自治县', '县级市', '旗', '自治旗', '市辖区', '林区',
     '特区', '镇', '乡', '民族乡', '苏木', '民族苏木', '街道办事处', '居委会', '村委会']


if __name__ == '__main__':
    main()
