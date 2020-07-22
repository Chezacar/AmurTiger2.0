import numpy as np
data = np.load('/Users/chezacar/Downloads/train_info.npy')
print(data)
data = np.delete(data,0,axis = 0)
np.save('train_info.npy',data)