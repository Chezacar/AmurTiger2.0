# -*- coding: utf-8 -*-
"""
    nana01219 王潇航
    2020-07-15
    本脚步对jpg，寻找对应的标注文件，并将标注信息写为txt
    readXML:读取标注文件内的bbox信息
    cutpic:切bbox
    getxml:寻找对应的xml文件并读取为txt
"""
from xml.dom.minidom import parse
import cv2
import os
from eco import ECOTracker
from PIL import Image
import glob
import os
import pandas as pd
import argparse
import numpy as np
import sys
import pickle

picroot = '../train'
resultdir = './train_bbox'
v_suffix = ['jpg']

for file1 in os.listdir(picroot):
    # 遍历所有文件
    idpath = os.path.join(picroot, file1)
    # print(idpath)
    # 跟踪
    for file2 in os.listdir(idpath):
        xlpath = os.path.join(idpath, file2)
        if os.path.isdir(xlpath):
            gtname = os.path.join(xlpath, 'gt.txt')

            # 清空文件内容，防止已经有了此文件
            with open(gtname, 'r') as ftxt:
                lines = ftxt.readlines()
                for idx, line in enumerate(lines):
                    lines[idx] = list(eval(line))
                # print(lines)
                ftxt.close()

            sortgt = os.path.join(xlpath, 'det.txt')
            frame = 0
            with open(sortgt, 'w') as f:
                f.truncate()
                for line in lines:
                    frame = frame+1
                    line.insert(0, -1)
                    line.insert(0, frame)
                    content = str(line).strip('[').strip(']')
                    f.write(content)
                    f.write('\n')
                f.close()
                    # print(line)


