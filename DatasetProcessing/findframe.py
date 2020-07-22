import pickle
import os
import sys
import subprocess

root_dir = './20181008-WWF东北虎数据/video/video'
dst_dir = '/home/amurtiger/Tiger/video'
#root_dir = './somescripts'
#dst_dir = './results'
with open('reid2.pkl', 'rb') as f:
    reid = pickle.load(f, encoding='bytes')

def compute_frame(key, total, neighbor):
    start = max(key, 1)
    end = min(key+neighbor, total+1)
    return start, end

for idx in reid:
    # 切片目的地
    if not os.path.exists(os.path.join(dst_dir, str(idx))):
        os.makedirs(os.path.join(dst_dir, str(idx)))

    video = reid[idx]['video']
    key = reid[idx]['key']
    bbox = reid[idx]['bbox']

    assert len(video) == len(key)
    assert len(key) == len(bbox)

    #with open(os.path.join(dst_dir, str(idx), 'gt.pkl'), 'wb') as f:
    #    bbox = pickle.dump(bbox, f)

    for i in range(len(video)):
        # path目标视频图片所在地
        path = os.path.join(root_dir, str(video[i]).zfill(5))
        total_frame = len(os.listdir(path))

        # 切片目的地
        if not os.path.exists(os.path.join(dst_dir, str(idx), str(i))):
            os.makedirs(os.path.join(dst_dir, str(idx), str(i)))
        start, end = compute_frame(key[i], total_frame, neighbor=16)

        with open(os.path.join(dst_dir, str(idx), str(i), 'gt.pkl'), 'wb') as f:
            pickle.dump(bbox[i], f)


        # 切片
        for frame in range(start, end):
            cmd = 'cp {} {}'.format(os.path.join(path, 'image_'+str(frame).zfill(5)+'.jpg'), 
                      os.path.join(dst_dir, str(idx), str(i)))
            subprocess.call(cmd, shell=True)