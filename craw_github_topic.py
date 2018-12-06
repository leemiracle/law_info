#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-12-3
@Author  : leemiracle
"""
import os

import requests
import subprocess
import time
from pyquery import PyQuery as pq

# topic = "nlp"
# topic = "awesome"
# topic = "crawler"
wait_craw_ = [
    "nlp",
    "awesome",
    "nlp",
    "crawler",
    "vue",
    "framework",
    "javascript",
    "python",
    "java",
    "cplusplus",
    "deep-learning",
    "machine-learning",
    "deep-neural-networks",
    "neural-network",
    "c",
]
# sub_direct = "vue"


def main():
    for topic in wait_craw_:
        direct = "/home/lwz/nlp_project/{sub_direct}".format(sub_direct=topic)
        if not os.path.exists(topic) and os.path.isdir(topic):
            os.mkdir(direct)
        uri = "https://github.com/topics/{topic}?o=desc&s=stars".format(topic=topic)
        req = requests.get(uri)
        s = req.text
        e = pq(s)
        for l in e("article"):
            link = l.xpath(".//div/h3/a")
            topics = l.xpath(".//div/h3/a")
            project_name = str(link[0].attrib["href"])
            cmd = "/usr/bin/git clone https://github.com{project_name}.git /home/lwz/nlp_project/{topic}/{name}".format(project_name=project_name,
                            name=project_name.split("/")[-1], topic=topic)
            print(cmd)
            try:
                subprocess.run(cmd, shell=True)
                time.sleep(1)
            except e:
                print(e)


if __name__ == '__main__':
    main()
