# -*- coding: utf-8 -*-
"""
    nana01219 王潇航
    2020-07-15
    cal_IOU:计算两个bbox的IOU
    eco_IOU：计算eco的结果

"""

import os
import numpy as np
import matplotlib.pyplot as plt



picroot = '../train'
sortroot = '../train_sort'

def cal_IOU(box, ref):
    inter = (np.minimum(ref[0]+ref[2], box[0]+box[2])-np.maximum(ref[0], box[0]))*(np.minimum(ref[1]+ref[3], box[1]+box[3])-np.maximum(ref[1], box[1]))
    union = ref[2]*ref[3] + box[2]*box[3] - inter
    return inter / union

def eco_IOU(gtname, ecoresult):
    # tracker = ECOTracker(is_color)
    # 读取gt的bbox
    iou = []
    with open(gtname, 'rb') as ftxt:
        lines = ftxt.readlines()
        for idx, line in enumerate(lines):
            lines[idx] = list(eval(line))
        #print(lines)
        ftxt.close()
    # 读取跟踪的bbox
    with open(ecoresult, 'r') as f2:
        results = f2.readlines()
        for idx, line in enumerate(results):
            a = ','.join(line.split())
            results[idx] = list(eval(a))
            iou.append(cal_IOU(lines[idx], results[idx]))
        f2.close()

    # print(results)
    return iou

def sort_IOU(gtname, sortname):
    iou = []
    myif = True
    seq_dets = np.loadtxt(sortname, delimiter=',')
    seq_dets[:, 4:6] += seq_dets[:, 2:4]
    seq_num = seq_dets.shape[0]
    with open(gtname, 'rb') as ftxt:
        lines = ftxt.readlines()
        gt_num = len(lines)
        for idx, line in enumerate(lines):
            lines[idx] = list(eval(line))
        #print(lines)
        ftxt.close()
    for i in range(seq_num):
        # print(seq_dets[i, 2:6], lines[int(seq_dets[i, 0])-1])
        # dets[:, 2:4] += dets[:, 0:2]
        iou.append(cal_IOU(seq_dets[i, 2:6], lines[int(seq_dets[i, 0])-1]))
    if gt_num-seq_num != 0:
        myif = False

    return iou, gt_num-seq_num, myif

def plotth(a):
    x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 0.99]
    y = np.zeros(len(x))
    for i in a:
        for n, j in enumerate(x):
            if i > x[n]:
                y[n] += 1
    y /= len(a)
    # plt.plot(x, y)
    # plt.show()
    return x, y


if __name__ == "__main__":
    iou1 = []
    iou2 = []
    dis_num2 = 0
    xlnum = 0
    xldis = 0
    for file1 in os.listdir(picroot):
        # 遍历所有文件
        idpath = os.path.join(picroot, file1)
        idpath2 = os.path.join(sortroot, file1)
        # print(idpath)

        for file2 in os.listdir(idpath):
            xlpath = os.path.join(idpath, file2)
            if os.path.isdir(xlpath):
                xlnum += 1
                xlpath2 = os.path.join(idpath2, file2)
                gtname = os.path.join(xlpath, "gt.txt")
                ecoresult = os.path.join(xlpath, "ecoresult.txt")
                sortresult = os.path.join(xlpath2, "sortresult.txt")
                iou = eco_IOU(gtname, ecoresult)
                iou1.extend(iou)
                iou, dis_num, myif = sort_IOU(gtname, sortresult)
                if not myif:
                    xldis += 1
                iou2.extend(iou)
                dis_num2 = dis_num2 + dis_num

    average1 = sum(iou1) / len(iou1)
    print('ECO: average iou is {}'.format(average1))
    x1, y1 = plotth(iou1)

    average2 = sum(iou2) / len(iou2)
    print('SORT: average iou is {}'.format(average2))
    x2, y2 = plotth(iou2)

    print('SORT: number of disappeared frames is {}'.format(dis_num2))
    print('SORT: possibility of disappear is {}'.format(dis_num2/(dis_num2+len(iou2))))
    print('SORT: number of wrong tracker is {}'.format(xldis))
    print('SORT: possibility of wrong tracker is {}'.format(xldis/(xldis+xlnum)))

    plt.figure()
    plt.plot(x1, y1, label="ECO")
    plt.plot(x1, y2, label="SORT")
    plt.xlabel('overlap Threshold')
    plt.ylabel('proportion')
    plt.show()

