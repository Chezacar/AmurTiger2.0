# -*- coding: utf-8 -*-
"""
    nana01219 王潇航
    2020-07-15
    本脚步将图片转为sort形式
"""
import glob
import os
import shutil

picroot = '../train'
resultdir = '../train_sort'
v_suffix = ['jpg']

for file1 in os.listdir(picroot):
    # 遍历所有文件
    idpath = os.path.join(picroot, file1)
    idpath2 = os.path.join(resultdir, file1)
    # print(idpath)
    # 跟踪
    for file2 in os.listdir(idpath):
        xlpath = os.path.join(idpath, file2)

        if os.path.isdir(xlpath):
            xlpath2 = os.path.join(idpath2, file2)
            if not os.path.exists(xlpath2):
                os.makedirs(xlpath2)
            gtname = os.path.join(xlpath, 'gt.txt')
            gtname2 = os.path.join(xlpath2, 'gt.txt')
            shutil.copy(gtname, gtname2)
            detname = os.path.join(xlpath, 'det.txt')
            detname2 = os.path.join(xlpath2, 'det.txt')
            shutil.copy(detname, detname2)
            filenames = sorted(glob.glob(os.path.join(xlpath, "*.jpg")),
                               key=lambda x: int(os.path.basename(x).split('.')[0].split('_')[-1]))
            for i, file in enumerate(filenames):
                iname = '%06d.jpg'%(i+1)
                jpgname2 = os.path.join(xlpath2, iname)
                shutil.copy(file, jpgname2)


