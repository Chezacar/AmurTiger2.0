import os
from glob import glob
import fnmatch


def get_things(root_dir):
    things = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            things.append(os.path.join(root, filename))
    
    return things

if __name__ == '__main__':
    train_folder = '/home/amurtiger/Annotated_data/train'
    test_folder = '/home/amurtiger/Annotated_data/test'
    train_pics = get_things(train_folder)
    test_pics = get_things(test_folder)

    train = open("/home/amurtiger/Annotated_data/train_name.txt",'w') 
    for train_pic in train_pics:
        #train_pic = os.path.split(train_pic)[1]
        train.write(str(train_pic) + '\r\n')
    train.close()
    
    test = open("/home/amurtiger/Annotated_data/test_name.txt",'w') 
    for test_pic in test_pics:
        #test_pic = os.path.split(test_pic)[1]
        test.write(str(test_pic) + '\r\n')
    test.close()

    
