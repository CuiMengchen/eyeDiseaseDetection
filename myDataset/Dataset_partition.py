# Dataset partition

import os
import random
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument('--labels_path', default='labels', type=str, help='input labels folder path')
parser.add_argument('--txt_list_path', default='ImageSets/Main', type=str, help='output txt list path')
opt = parser.parse_args()

trainval_percent = 1.0  
train_percent = 0.8    # train set ratio
val_percent = 0.1      # val set ratio
test_percent = 0.1     # test set ratio
labelspath = opt.labels_path
txtlistpath = opt.txt_list_path
total_labels = os.listdir(labelspath)
if not os.path.exists(txtlistpath):
    os.makedirs(txtlistpath)

num = len(total_labels)
list_index = range(num)
tv = int(num * trainval_percent)
trainval = random.sample(list_index, tv)

train_size = int(tv * train_percent)
val_size = int(tv * val_percent)

train_indices = random.sample(trainval, train_size)
list_index = list(set(list_index) - set(train_indices))

val_indices = random.sample(list_index, val_size)
test_indices = list(set(list_index) - set(val_indices))

# 创建训练、验证、测试和trainval的TXT文件
train_file = open(os.path.join(txtlistpath, 'train.txt'), 'w')
val_file = open(os.path.join(txtlistpath, 'val.txt'), 'w')
test_file = open(os.path.join(txtlistpath, 'test.txt'), 'w')
trainval_file = open(os.path.join(txtlistpath, 'trainval.txt'), 'w')

# 将文件名写入相应的TXT文件
for i in train_indices:
    filename = total_labels[i][:-4]
    train_file.write(filename + '\n')
    # 可以选择将文件复制到训练集文件夹
    # copyfile(os.path.join(labelspath, total_labels[i]), os.path.join('train_folder', total_labels[i]))

for i in val_indices:
    filename = total_labels[i][:-4]
    val_file.write(filename + '\n')

for i in test_indices:
    filename = total_labels[i][:-4]
    test_file.write(filename + '\n')

for i in trainval:
    filename = total_labels[i][:-4]
    trainval_file.write(filename + '\n')

# 关闭文件
train_file.close()
val_file.close()
test_file.close()
trainval_file.close()
