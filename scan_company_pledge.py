#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-27
@Author  : leemiracle
"""
import datetime

import requests
import os
import pandas as pd

from util.date_util import find_trade_week_first_day
from util.path_util import make_sure_path_exist

current_path = os.getcwd()
file_path = "stock_pledge"
path = os.path.join(current_path, file_path)
index = "质押比例(%)"


def download_xls(date='2018.09.14'):
    url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate={date}&type=proportion'.format(date=date)
    r = requests.get(url, stream=True)
    # print(r.text)
    absolute_path = path + '/{date}.xls'.format(date=date)
    make_sure_path_exist(path)
    with open(absolute_path, 'wb') as f:
        f.write(r.content)


def last_week_pledge_change(delta=0, download=False, arrange=1):
    current_date = datetime.date.today() + datetime.timedelta(days=-7*delta)
    last_two_week_date = current_date + datetime.timedelta(days=-7*arrange)
    days = find_trade_week_first_day(last_two_week_date, current_date)
    if len(days) <= 1:
        last_two_week_date += datetime.timedelta(days=-7)
        days = find_trade_week_first_day(last_two_week_date, current_date)
    if download:
        for day in days:
            download_xls(day)
    df_list = []
    for day in days:
        df = parse_xls(day)
        df_list.append(df)
    a = df_list[-1]
    # print(a.keys().tolist())
    # print("质押笔数(笔) 最多:")
    # b1 = a[a['质押笔数(笔)'] == a['质押笔数(笔)'].max()]
    # print("{}".format(b1.values.tolist()[0]))  # 温氏股份
    # print("无限售股份质押数量(万):")
    # b2 = a[a['无限售股份质押数量(万)'] == a['无限售股份质押数量(万)'].max()]
    # print(b2.values.tolist()[0])  # 包钢股份
    # print("有限售股份质押数量(万):")
    # b3 = a[a['有限售股份质押数量(万)'] == a['有限售股份质押数量(万)'].max()]
    # print(b3.values.tolist()[0])  # 三六零
    # print("质押比例（%）:")
    # b4 = a[a['质押比例（%）'] == a['质押比例（%）'].max()]
    # print(b4.values.tolist()[0])  # 银亿股份

    b = df_list[-2]
    # 差值
    result = pd.concat([a, b], axis=1, keys=['s1', 's2'])
    s1 = result['s1']
    s2 = result['s2']
    result['pledge_rate'] = s1['质押比例（%）'] - s2['质押比例（%）']
    max_value = result['pledge_rate'].max()
    min_value = result['pledge_rate'].min()
    if max_value>0:
        max_pledge = result[result['pledge_rate'] == max_value]
        print("增加质押最多的:{}".format(max_value))
        print(max_pledge['s1'].values.tolist())
    if min_value < 0:
        min_pledge = result[result['pledge_rate'] == min_value]
        print("解质押最多的:{}".format(min_value))
        print(min_pledge['s1'].values.tolist())


def parse_xls(date):
    file_name = '{}.xls'.format(date)
    absolute_path = os.path.join(path, file_name)
    df = pd.read_excel(absolute_path, header=2)
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    df.set_index('证券代码', inplace=True)
    # print(df[df[index] == df[index].max()])
    return df


def main():
    # last_week_pledge_change(delta=2, download=True, arrange=20)
    for i in range(0, 20):
        last_week_pledge_change(delta=i)


if __name__ == '__main__':
    main()
