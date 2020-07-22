ecotrack:ECO跟踪算法，需要用到自带的eco包
sort：SORT跟踪算法
getbbox：读取xml文件中的标注信息，剪帧
getgt、getsortgt：分别将读取的标注信息转换为两种跟踪方法的对应数据格式，最后输出的txt文件
movepic：将图片转为SORT数据集的格式。（原本是ECO）格式
ioucalc：计算两种算法的overlap，对比效果
