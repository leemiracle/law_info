#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-27
@Author  : leemiracle
"""

import os


def make_sure_path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    pass


if __name__ == '__main__':
    main()
