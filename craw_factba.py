#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-11-29
@Author  : leemiracle
"""
import datetime
import time

import requests
from pyquery import PyQuery as pq
import json

from you_get.extractors.youtube import YouTube
from you_get.processor.ffmpeg import ffprobe_get_media_duration

# todo you_get common.getoutputfilename=自定义（覆盖），从而实现重命名
COUNT = 0

video_dic = dict()

proxies = {
  "http": "socks5://127.0.0.1:1080",
  "https": "socks5://127.0.0.1:1080",
}


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

def parse_factba_json(q="trump", media="video", length=500):
    count = 0
    not_slug_num = 0
    filter_number = 0

    page = 1
    ret = dict()
    factba_base_uri = "https://factba.se/transcript/{slug}"
    already_done = set()

    # endate_time = datetime.datetime.utcnow()
    endate_time = datetime.datetime.strptime("2018-01-25", "%Y-%m-%d")
    enddate = str(endate_time)
    interval = 15
    # data = None
    limit = "1980-01-01"
    while limit <= enddate:
        enddate = str(endate_time).split(" ")[0]
        startdate = str(endate_time-datetime.timedelta(days=interval)).split(" ")[0]

        next_sum_record = length
        combo_number = 0
        page = 1
        while next_sum_record >= 0:
            uri = "https://factba.se/json/json-20170612.php?q={q}&media={media}&type=&startdate={startdate}&enddate={enddate}&sort=desc&f=&t=se&l={length}&p={page}"\
                .format(q=q, media=media, length=length, page=page, startdate=startdate, enddate=enddate)
            r = requests.get(uri, proxies=proxies)
            try:
                result = r.text
                # print(result)
                result = json.loads(result)
                data = result["combo"]["data"]
                combo_number = result["combo"]["filtered"]
                next_sum_record = combo_number - page*length
            except Exception as e:
                print(str(e))
                print("Exception: {}".format(result))
                page += 1
                continue

            # print(len(data))
            if data:
                page += 1
                for dic in data:
                    count += 1
                    # print("count: {}".format(count))
                    if "slug" not in dic:
                        not_slug_num += 1
                        print("error:{}".format(json.dumps(dic)))
                        continue
                    slug = dic["slug"]
                    record_title = dic["record_title"]
                    youtube_url = dic["url"]
                    factba_uri = factba_base_uri.format(slug=slug)
                    # print(factba_uri)
                    if (factba_uri not in already_done) and analysis_check_(factba_uri):
                        ret.update({factba_uri : {
                            'youtube_url': youtube_url,
                            "title": record_title
                        }})
                        # print("ret: {}".format())
                        time.sleep(0.3)
                    already_done.add(factba_uri)
            else:
                break
        filter_number+=combo_number
        print("时间间隔：{} {}, {}, {}, {}, {}".format(startdate, enddate, count, not_slug_num, len(ret.keys()), filter_number))
        endate_time = endate_time-datetime.timedelta(days=interval)
        finally_ret = json.dumps(ret)
        with open("video_trump.json", "w+") as f:
            f.write(finally_ret)


def analysis_check_(url):
    s = requests.get(url, proxies=proxies)
    e = pq(s.text)
    not_al = e("div.media.topic-media-row.mediahover.not-trump")
    number_not = len(not_al)
    al = e("div.media.topic-media-row.mediahover:not(.not-trump)")
    number_ = len(al)
    # print(number_, number_not)
    rate = float(number_)/float(number_+number_not) if number_>0 else 0
    return rate > 0.9


def concat_json():
    paths = os.listdir("./")
    ret = dict()
    for s in paths:
        if "video_trump" in s and s.endswith(".json"):
            with open(s, "r+") as f:
                txt = f.read()
            json_ = json.loads(txt)
            ret.update(json_)
    print(len(ret))
    ret = json.dumps(ret)
    with open("trump_result.json", "w+") as f:
        f.write(ret)

def download_():
    global output_filename
    file_num = 127
    ret = dict()
    has_not_trump_ = dict()
    with open("trump_result.json", "r+") as f:
        json_ = f.read()
        json_ = json.loads(json_)
    keys = sorted(list(json_.keys()))
    try:
        for i, k in enumerate(keys):
            v = json_[k]
            title = v["title"].strip()
            uri = v["youtube_url"]
            file_name = format(file_num, "06d")
            output_filename = file_name
            if title.startswith("Weekly Address"):
                (_, size) = download_youtube(uri, proxies=None)
                file_num += 1
                e = pq(url=k)
                al_not = e("div.media.topic-media-row.mediahover.not-trump")
                if len(al_not) == 0:
                    # print(k)
                    al = e("div.media.topic-media-row.mediahover:not(.not-trump)")
                    contents = []
                    for l in al:
                        d = decompress_content(l)
                        contents.append(d)
                    ret.update({
                        file_name: {
                            "youtube_url": uri,
                            "title": title,
                            "size": size,
                            "contents": contents,
                            "factba_uri": k
                        }
                    })
                else:
                    contents = []
                    for l in al_not:
                        d = decompress_content(l)
                        contents.append(d)
                    has_not_trump_.update({
                        file_name: {
                            "youtube_url": uri,
                            "title": title,
                            "size": size,
                            "contents": contents,
                            "factba_uri": k
                        }
                    })
    except Exception as e:
        print(e)
    finally:
        with open("trump_video_result.json", "w+") as f:
            json_ret_ = json.dumps(ret)
            f.write(json_ret_)
        with open("trump_has_not_video_result.json", "w+") as f:
            has_not_trump_ = json.dumps(has_not_trump_)
            f.write(has_not_trump_)


def decompress_content(element):
    body = str(element.xpath('.//div[@class="transcript-text-block"]/a')[0].text_content())  # 文本
    time_slice = str(element.xpath('.//div[@class="timecode-block"]')[0].text_content())  # 片段在视频中的起止时间
    tags = []
    e_tags = element.xpath('.//div[@class="tag-block"]/div')
    for t in e_tags:
        tag = str(t.text_content())
        tags.append(tag)
    return {"time_slice":time_slice, "body":body, "tags": tags}


if __name__ == '__main__':
    main()
    # save_to_mysql()
