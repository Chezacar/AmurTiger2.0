import glob
import os
import pandas as pd
import argparse
import numpy as np
import cv2
import sys
sys.path.append('./')

from eco import ECOTracker
from PIL import Image

import argparse

def main(video_dir):
    # # 读入连续帧
    # # filenames为图片名
    filenames = sorted(glob.glob(os.path.join(video_dir, "img/*.jpg")),
           key=lambda x: int(os.path.basename(x).split('.')[0]))

    # frames包含连续帧数据
    # frames = [cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB) for filename in filenames]
    frames = [np.array(Image.open(filename)) for filename in filenames]
    height, width = frames[0].shape[:2]
    if len(frames[0].shape) == 3:
        is_color = True
    else:
        is_color = False
        frames = [frame[:, :, np.newaxis] for frame in frames]

    #读取bbox
    gt_bboxes = pd.read_csv(os.path.join(video_dir, "groundtruth_rect1.txt"), sep='\t|,| ',
            header=None, names=['xmin', 'ymin', 'width', 'height'],
            engine='python')

    #输出文件，此处需要修改
    title = video_dir.split('/')[-1]
    txtname = './results/' + video_dir[10:-1] + '.txt'
    #print(video_dir[10:-1])
    print(txtname)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # img_writer = cv2.VideoWriter(os.path.join('./videos', title+'.avi'),
    #         fourcc, 25, (width, height))

    # 开始跟踪
    tracker = ECOTracker(is_color)
    vis = True
    for idx, frame in enumerate(frames):
        if idx == 0:
            bbox = gt_bboxes.iloc[0].values
            tracker.init(frame, bbox)
            bbox = (bbox[0]-1, bbox[1]-1,
                    bbox[0]+bbox[2]-1, bbox[1]+bbox[3]-1)
            with open(txtname,'w') as f:
                content = str(np.round(bbox).astype(np.int16)).strip('[').strip(']')
                f.write(content)
                f.write('\n')
                f.close()
        elif idx < len(frames) - 1:
            bbox = tracker.update(frame, True, vis)
            with open(txtname,'a') as f:
                content = str(np.round(bbox).astype(np.int16)).strip('[').strip(']')
                f.write(content)
                f.write('\n')
                f.close()
        else: # last frame
            bbox = tracker.update(frame, False, vis)
            with open(txtname,'a') as f:
                content = str(np.round(bbox).astype(np.int16)).strip('[').strip(']')
                f.write(content)
                f.write('\n')
                f.close()

        # bbox xmin ymin xmax ymax
        frame = frame.squeeze()
        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frame = cv2.rectangle(frame,
                              (int(bbox[0]), int(bbox[1])),
                              (int(bbox[2]), int(bbox[3])),
                              (0, 255, 255),
                              1)
        #gt_bbox = gt_bboxes.iloc[idx].values
        #gt_bbox = (gt_bbox[0], gt_bbox[1],
        #           gt_bbox[0]+gt_bbox[2], gt_bbox[1]+gt_bbox[3])
        #frame = frame.squeeze()
        #frame = cv2.rectangle(frame,
        #                      (int(gt_bbox[0]-1), int(gt_bbox[1]-1)), # 0-index
        #                      (int(gt_bbox[2]-1), int(gt_bbox[3]-1)),
        #                     (0, 255, 0),
        #                      1)
        if vis and idx > 0:
            score = tracker.score
            size = tuple(tracker.crop_size.astype(np.int32))
            score = cv2.resize(score, size)
            score -= score.min()
            score /= score.max()
            score = (score * 255).astype(np.uint8)
            # score = 255 - score
            score = cv2.applyColorMap(score, cv2.COLORMAP_JET)
            pos = tracker._pos
            pos = (int(pos[0]), int(pos[1]))
            xmin = pos[1] - size[1]//2
            xmax = pos[1] + size[1]//2 + size[1] % 2
            ymin = pos[0] - size[0] // 2
            ymax = pos[0] + size[0] // 2 + size[0] % 2
            left = abs(xmin) if xmin < 0 else 0
            xmin = 0 if xmin < 0 else xmin
            right = width - xmax
            xmax = width if right < 0 else xmax
            right = size[1] + right if right < 0 else size[1]
            top = abs(ymin) if ymin < 0 else 0
            ymin = 0 if ymin < 0 else ymin
            down = height - ymax
            ymax = height if down < 0 else ymax
            down = size[0] + down if down < 0 else size[0]
            score = score[top:down, left:right]
            crop_img = frame[ymin:ymax, xmin:xmax]
            # if crop_img.shape != score.shape:
            #     print(left, right, top, down)
            #     print(xmin, ymin, xmax, ymax)
            score_map = cv2.addWeighted(crop_img, 0.6, score, 0.4, 0)
            frame[ymin:ymax, xmin:xmax] = score_map

        frame = cv2.putText(frame, str(idx), (5, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
        # img_writer.write(frame)
        cv2.imshow(title, frame)

        jpgpath = './results/' + video_dir[10:-1] + '/'
        print(jpgpath)
        if not os.path.exists(jpgpath):
            os.mkdir(jpgpath)

        cv2.imwrite(jpgpath + str(idx) + '.jpg', frame)

        cv2.waitKey(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_dir', type=str, default='sequences/Crossing/')
    args = parser.parse_args()
    main(args.video_dir)
