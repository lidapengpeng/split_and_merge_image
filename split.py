import cv2
import math
from pathlib import Path
import os


def split_one_image(one_image_path, out_split_image_path, width=416, height=416, over_x=27, over_y=27):
    """
    Description:用于切分图像，包含重叠区域
    Parameter:
    width、height: 切分后图像大小
    over_x、over_y: 图像overlap的区域
    """
    h_val = height - over_x
    w_val = width - over_y
    img_file_name = one_image_path.split('.')[0].split('/')[1]
    # Set whether to discard an image that does not meet the size
    mandatory = False
    img = cv2.imread(one_image_path)

    print(img.shape)
    # original image size
    original_height = img.shape[0]
    original_width = img.shape[1]

    max_row = float((original_height - height) / h_val) + 1
    max_col = float((original_width - width) / w_val) + 1

    # block number
    max_row = math.ceil(max_row) if mandatory is False else math.floor(max_row)
    max_col = math.ceil(max_col) if mandatory is False else math.floor(max_col)

    print(max_row)
    print(max_col)

    images = []
    for i in range(max_row):
        images_temp = []
        for j in range(max_col):
            temp_out_path = str(out_split_image_path)+'/'+img_file_name
            if not os.path.exists(temp_out_path):
                os.makedirs(temp_out_path)
            temp_path = temp_out_path + '/' + str(i) + '_' + str(j) + '_'
            if ((width + j * w_val) > original_width and (
                    i * h_val + height) <= original_height):  # Judge the right most incomplete part
                temp = img[i * h_val:i * h_val + height, j * w_val:original_width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            elif ((height + i * h_val) > original_height and (
                    j * w_val + width) <= original_width):  # Judge the incomplete part at the bottom
                temp = img[i * h_val:original_height, j * w_val:j * w_val + width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            elif (width + j * w_val) > original_width and (
                    i * h_val + height) > original_height:  # Judge the last slide
                temp = img[i * h_val:original_height, j * w_val:original_width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            else:
                temp = img[i * h_val:i * h_val + height, j * w_val:j * w_val + width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
        images.append(images_temp)

    print(len(images))


if __name__ == '__main__':
    out_path = Path('./split_image/')
    source_images_path = Path('./source_image/').glob('*.JPG')
    images_path = [str(path) for path in source_images_path]
    for path in images_path:
        split_one_image(path, out_path)
