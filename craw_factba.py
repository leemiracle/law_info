#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-11-29
@Author  : leemiracle
"""
import time

import requests
from pyquery import PyQuery as pq
import json

from you_get.extractors.youtube import YouTube
from you_get.processor.ffmpeg import ffprobe_get_media_duration

# todo you_get common.getoutputfilename=自定义（覆盖），从而实现重命名
COUNT = 0

video_dic = dict()


# def analysis_transcript(string):
def analysis_transcript(url):
    global COUNT
    # e = pq(filename="Transcript.html")
    e = pq(url=url)
    all_ = []
    # al = e("div[class=media][class=topic-media-row][class=mediahover]")
    # al = e("div#resultsblock")
    al = e("div.media.topic-media-row.mediahover:not(.not-trump)")
    ret = []
    print(len(al))
    for l in al:
        print(COUNT)
        # id :编号
        body = str(l.xpath('.//div[@class="transcript-text-block"]/a')[0].text_content())  # 文本
        time_slice = str(l.xpath('.//div[@class="timecode-block"]')[0].text_content())  # 片段在视频中的起止时间
        youtube_uri = "https://www.youtube.com/embed/"
        dataset_id = str(l.xpath('.//div[@class="youtube-large"]')[0].attrib["data-id"])
        uri = youtube_uri + dataset_id  # youtube地址
        if uri not in video_dic:
            (filename, size) = download_youtube(uri)  # 本地存储的视频地址 # 视频总大小
            video_dic.update({uri: [filename, size]})
        tags = []
        e_tags = l.xpath('.//div[@class="tag-block"]/div')
        for t in e_tags:
            tag = str(t.text_content())
            tags.append(tag)
        # print(body)
        # print(time_slice)
        # print(tags)
        all_.append(l)
        dic = {
            "code": COUNT,
            'filename': video_dic[uri][0],
            'filesize': video_dic[uri][1],
            'factba_url': url,
            'youtube_url': youtube_uri,
            'tags': tags,
            "body": body,
            "time_slice": time_slice
        }
        ret.append(dic)
        COUNT += 1
    # print(dir(l))
    # for el in l.iterchildren():
    #     print(el)
    # print(len(all_))
    return ret


def download_youtube(uri):
    output_dir = "/home/ubuntu/luowenzhuo/tmp/"  # 目录
    # proxies = {
    #     "http": "socks5://127.0.0.1:1080",
    #     'https': 'socks5://127.0.0.1:1080'
    # }
    # req = requests.get("http://www.google.com", proxies=proxies)
    youtube_ = YouTube()
    youtube_.download_by_url(uri, output_dir=output_dir, merge=True)
    time.sleep(1)
    # youtube_.download_by_url("https://www.youtube.com/embed/72oEZIcJeGw?start=21&autoplay=1", output_dir=output_dir, merge=True)

    filename = output_dir + youtube_.title
    itags = [s['itag'] for s in youtube_.stream_types]
    size = 0
    for itag in itags:
        if itag in youtube_.streams and "size" in youtube_.streams[itag]:
            fmt = youtube_.streams[itag]["container"]  # 格式
            size = sizeof_fmt(youtube_.streams[itag]["size"])
            filename = filename + fmt
    return filename, size


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_media_duration(filename):
    s = ffprobe_get_media_duration(filename)
    print(s)


def main():
    e = pq(filename="Trump.html")
    all_ = []
    all_urls_ = set()
    for link in e('div.col-lg-9 small a'):
        s = link.attrib['href']
        if "factba.se/transcript" in s:
            # print(s)
            # req = requests.get(s)
            # txt = req.text
            # analysis_transcript(s)
            all_urls_.add(s)
    all_urls_ = list(all_urls_)
    print(all_urls_)
    for uri in all_urls_:
        dic = analysis_transcript(uri)
        all_.extend(dic)
    # for item in e('div.item div.well div.row'):
    #     iframe = item.xpath('//iframe')
    #     uri = iframe[0].attrib['src']
    #     anchor = item.xpath('//small/a')
    #     transcript = anchor[0].attrib['href']
    #     print(transcript)
    #     print(uri)

    write_json = json.dumps(all_)
    with open("trump_result.log", "w+") as f:
        f.write(write_json)
    # print(json.dumps(all_))


if __name__ == '__main__':
    main()
    # save_to_mysql()
