from __future__ import print_function, division
import os
import sys
import subprocess
import pickle

with open('reid.pkl', 'rb') as f:
    reid = pickle.load(f, encoding='bytes')

suffix = ['mp4', 'mov', 'MP4', 'MOV', 'mts', 'MTS']

root_dir1 = './20181008-WWF东北虎数据/大连野生动物园'
root_dir2 = './20181008-WWF东北虎数据/济南野生动物园'
dst_dir = './20181008-WWF东北虎数据/video'

def findfile(dir, v_suffix, files):
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        if os.path.isfile(file):
            if f in v_suffix:
                files.append(file)
            #suffix = file.split('.')[-1]
            #if suffix in v_suffix:
            #    files.append(file)
        else:
            findfile(file, v_suffix, files)
    return files

def video_process(video_file_path, dst_path):
    cmd = 'ffmpeg -i \"{}\" \"{}/image_%05d.jpg\"'.format(video_file_path, dst_path)
    subprocess.call(cmd, shell=True)
            
if __name__ == '__main__':
    names = []
    mapping = dict()
    for i in reid:
        videos = reid[i]['video']
        for video in videos:
            name = video.split('/')[-1]
            name = name.split('-')[0]
            names.append(name)
    names = list(set(names))
    
    f = findfile(root_dir1, names, [])
    f = findfile(root_dir2, names, f)
    for i, video in enumerate(f):
        mapping[video.split('/')[-1]] = i
        video_dir = os.path.join(dst_dir, 'video', str(i).zfill(5))
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        video_process(video, video_dir)
    
    for _, ele in reid.items():
        for i in range(len(ele['video'])):
            ele['video'][i] = mapping[ele['video'][i].split('/')[-1].split('-')[0]]
    with open('./reid2.pkl', 'wb') as f:
        reid = pickle.dump(reid, f)