import scipy.io as sio

'''# python创建一个mat文件
x = [[1, 2, 3], [4, 5, 6]]
y = [4, 5, 6]
z = [7, 8, 9]
sio.savemat('saveddata.mat', {'x': x,'y': y,'z': z}'''

f = sio.loadmat('./tracks_test_info.mat')
tti = f['track_test_info']
tmp_id = 0

line_num_in_test = []

for i in range(tti.shape[0]):
    identity = tti[i][2]
    if tmp_id != identity:
        tmp_id = identity
        if i > 0:
            line_num_in_test.append(i)
        line_num_in_test.append(i + 1)

line_num_in_test.append(tti.shape[0])

sio.savemat('query_IDX.mat', {'query_IDX': line_num_in_test})

'''
while True:
    content = f.readline()
    if content == '':
        break
    i = i + 1
    z2 = content[7:11]
    t = content[12:15]
    # print(z2)
    if z2 != z or t == '001':
        z = z2
        y.append(i-1)
        if not id == "00-1":  # 对id为-1的情况单独考虑
            y.append(int(id))
        else:
            y.append(-1)
        y.append(int(cam))
        id = content[0:4]
        cam = content[5]
        x.append(y)
        y = [i]
# 最后一个tracklet还没有写入循环就退出了
y.append(i)
y.append(int(id))
y.append(int(cam))
x.append(y)
#print(x)
sio.savemat('tracks_train_info.mat', {'x': x})  # 修改输出文件名
'''

