import cv2
import numpy as np
import functools
import os
from pathlib import Path


def custom_sort(x, y):
    x = x.split('/')[2].split('.')[0].split('_', 6)
    new_x = x[3:]
    x = [int(i) for i in new_x]
    y = y.split('/')[2].split('.')[0].split('_', 6)
    new_y = y[3:]
    y = [int(i) for i in new_y]
    for i in range(len(x)):
        if x[i] > y[i]:
            return 1
        elif x[i] < y[i]:
            return -1
        elif i == len(x) - 1:
            return 0


def merge_one_image(one_image_path, out_split_image_path, width=416, height=416, over_x=27, over_y=27):
    """
    Description:用于合并图像，包含重叠区域
    Parameter:
    width、height: 原始输入图像大小
    over_x、over_y: 图像overlap的区域
    """
    little_img_path = Path(one_image_path).glob('*')
    images_path = [str(path) for path in little_img_path]
    images_path = sorted(images_path, key=functools.cmp_to_key(custom_sort))

    s = set()
    for path in images_path:
        path = path.split('/')[2].split('.')[0].split('_', 6)
        s.add(int(path[3]))

    output = []
    for i in range(len(s)):
        output.append([])

    for image_path in images_path:
        image = cv2.imread(image_path)
        image_path = image_path.split('/')[-1].split('.')[0].split('_')
        if int(image_path[6]) == width:
            if int(image_path[4]) == 0:
                output[int(image_path[3])].append(image[:, :, :])
            else:
                output[int(image_path[3])].append(image[:, over_y:, :])
        else:
            output[int(image_path[3])].append(image[:, over_y:, :])

    temp = []
    for i in range(len(output)):
        t = np.concatenate(output[i], 1)
        if i == 0:
            temp.append(t[:, :, :])
        else:
            temp.append(t[over_x:, :, :])

    temp = np.concatenate(temp, 0)
    output_img_name = one_image_path.split('/')[2] + '.jpg'
    cv2.imwrite(out_split_image_path+'/'+output_img_name, temp)


if __name__ == '__main__':
    if not os.path.exists('./merge_image/'):
        os.makedirs('./merge_image/')
    out_path = str(Path('./merge_image/'))
    source_images_path = os.listdir('./split_image')
    for path in source_images_path:
        input_path = './split_image/' + path + '/'
        merge_one_image(input_path, out_path)
