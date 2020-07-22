import numpy as np
import scipy.io as scio
import os

file1 = open("/home/amurtiger/Annotated_data/test_name.txt") 
file2 = open("/home/amurtiger/Annotated_data/train_name.txt") 

test_list = file1.readlines()
train_list = file2.readlines()
test = np.array((len(test_list),4))
train = np.array((len(train_list),4))

def haha(test_list):
    iter = 0
    temp = 0
    temp1 = 0
    temp2 = 0
    test = []
    for item in test_list:
        
        items = item.split('/')
        #print(items[0],items[5],items[6])
        if int(items[6]) == temp1 and int(items[7]) == temp2:
            iter += 1
        else:
            test_temp = []
            test_temp.append(temp)
            test_temp.append(iter)
            test_temp.append(temp1)
            test_temp.append(temp2)
            iter += 1
            temp1 = int(items[6])
            temp2 = int(items[7])
            temp = iter
            test.append(test_temp)
    del(test[0])
    return(np.array(test))

test = haha(test_list)
train = haha(train_list)

np.save('/home/amurtiger/Annotated_data/test_info.npy',test)
scio.savemat('/home/amurtiger/Annotated_data/test_info.mat',{'test':test})
np.save('/home/amurtiger/Annotated_data/train_info.npy',train)
scio.savemat('/home/amurtiger/Annotated_data/train_info.mat',{'train':train})
#print(np.array(test))