# -*- coding: utf-8 -*-
"""
    nana01219
    2020-07-13
    readXML:读取标注文件内的bbox信息
    cutpic:切bbox
"""
from xml.dom.minidom import parse
import cv2
import os

rootdir = './train'
resultdir = './train_bbox'
suffix = ['jpg']


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

def cutpic(imgpath, bbox, resultpath):
    img = cv2.imread(imgpath)
    cropped = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imwrite(resultpath, cropped)

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

if __name__ == '__main__':
    files = findfile(rootdir, suffix, [])
    # every pic
    for file in files:
        name = file.split('.')[-2]
        # print(name)
        resultdir2 = resultdir + name[0:-11]
        if not os.path.exists(resultdir2):
            os.makedirs(resultdir2)
        #    print(resultdir2)
        result = resultdir + name + '.jpg'
        # print(result)
        # print(name)
        if not os.path.exists(result):
            try:
                xmldir = os.path.join(rootdir, file.split('/')[2], name.split('/')[-1]+'.xml')
            #    print(xmldir)
                bbox = readXML(xmldir)
            except:
                xmldir = '.' + name + '.xml'
            #    print(xmldir)
                bbox = readXML(xmldir)
            cutpic(file, bbox, result)

        #print(name)

