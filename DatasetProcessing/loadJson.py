# -*- coding: UTF-8 -*-
import json
import os
from PIL import Image as Image
import pickle
import sys
# 原始图片数据存放的地址
root_dir = '/home/amurtiger/hdb'

# copy了钱锐的函数
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

# 其实就是主函数
def getJson(path, reid):
    file = open(path, "rb")
    fileJson = json.load(file)

    for line in fileJson:
        # 分别获得entityid和图片路径
        imgpath = fileJson[line]['imgpath']
        if (not '济南' in imgpath) and (not '大连' in imgpath):
            continue
        imgpath = os.path.join(root_dir, imgpath)
        
        (imgpath, ext) = os.path.splitext(imgpath)
        (video, frameID) = os.path.split(imgpath)
        frameID = int(frameID)

#        (useless, videoID) = os.path.split(useless)
        for entityDict in fileJson[line]['anno']:
            entity = entityDict['entityid']
            if entity not in reid:
                reid[entity] = dict()
                reid[entity]['video'] = []
                reid[entity]['key'] = []
                reid[entity]['keypoint'] = []
                reid[entity]['bbox'] = []
            reid[entity]['video'].append(video)
            reid[entity]['key'].append(frameID)
            try:
                reid[entity]['keypoint'].append(entityDict['keypoint'])
            except:
                reid[entity]['keypoint'].append([])
            reid[entity]['bbox'].append(entityDict['bbox'])

    return        

if __name__ == '__main__':
    path = "./unianno.json"
    reid = dict()
    getJson(path, reid)
    with open('reid.pkl', 'wb') as f:
        pickle.dump(reid, f)