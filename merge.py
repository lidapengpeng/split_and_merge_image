import cv2
import numpy as np
import functools

from pathlib import Path


def custom_sort(x, y):
    x = x.split(tag)[-1].split('.')[0].split('_')
    x = [int(i) for i in x]
    y = y.split(tag)[-1].split('.')[0].split('_')
    y = [int(i) for i in y]
    for i in range(len(x)):
        if x[i] > y[i]:
            return 1
        elif x[i] < y[i]:
            return -1
        elif i == len(x) - 1:
            return 0


tag = '/'  # 路径分隔符

data_root = Path('./split-image/')
temp_path = '2.jpg'

height = 416
width = 416

# overlap
over_x = 27
over_y = 27
h_val = height - over_x
w_val = width - over_y

images_path = data_root.glob('*')
# for path in images_path:
#     images_path = str(path).split('/', 1)[1]

images_path = [str(path) for path in images_path]
images_path = sorted(images_path, key=functools.cmp_to_key(custom_sort))
# print(images_path)

s = set()
for path in images_path:
    path = path.split(tag)[-1].split('_')
    s.add(int(path[0]))
# print(s)

output = []
for i in range(len(s)):
    output.append([])

for path in images_path:
    image = cv2.imread(path)
    path = path.split(tag)[-1].split('.')[0].split('_')
    if int(path[3]) == width:
        if int(path[1]) == 0:
            output[int(path[0])].append(image[:, :, :])
        else:
            output[int(path[0])].append(image[:, over_y:, :])
    else:
        output[int(path[0])].append(image[:, over_y:, :])

temp = []
for i in range(len(output)):
    t = np.concatenate(output[i], 1)
    if i == 0:
        temp.append(t[:, :, :])
    else:
        temp.append(t[over_x:, :, :])

temp = np.concatenate(temp, 0)
cv2.imwrite(temp_path, temp)

