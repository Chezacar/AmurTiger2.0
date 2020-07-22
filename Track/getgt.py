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


def readXML(xmlpath):
    domTree = parse(xmlpath)
    # 文档根元素
    rootNode = domTree.documentElement

    obj = rootNode.getElementsByTagName("object")
    box = obj[0].getElementsByTagName("bndbox")
    xmin = box[0].getElementsByTagName("xmin")[0]
    xmin = xmin.childNodes[0].data
    ymin = box[0].getElementsByTagName("ymin")[0]
    ymin = ymin.childNodes[0].data
    xmax = box[0].getElementsByTagName("xmax")[0]
    xmax = xmax.childNodes[0].data
    ymax = box[0].getElementsByTagName("ymax")[0]
    ymax = ymax.childNodes[0].data

    bbox = [int(xmin), int(ymin), int(xmax), int(ymax)]
    return bbox

def findfile(dir, v_suffix, files):
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        if os.path.isfile(file):
            suffix = file.split('.')[-1]
            if suffix in v_suffix:
                files.append(file)
        else:
            findfile(file, v_suffix, files)
    return files

def getxml(filenames, idpath, gtname):
    for filename in filenames:
        picname = filename.split('/')[-1]
        picname = picname.strip('jpg') + 'xml'
        xmldir = filename.strip('jpg') + 'xml'
        # print(picname)
        try:
            bbox = readXML(xmldir)
        except:
            xmldir = os.path.join(idpath, picname)
            bbox = readXML(xmldir)
        with open(gtname, 'a') as f:
            content = str(bbox).strip('[').strip(']')
            f.write(content)
            f.write('\n')
            f.close()

if __name__ == '__main__':
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
                    with open(gtname, 'w') as f:
                        f.truncate()
                        f.close()

                    filenames = sorted(glob.glob(os.path.join(xlpath, "*.jpg")),
                                       key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
                    # print(filenames)

                    getxml(filenames, idpath, gtname)




