import cv2
import math
from pathlib import Path

file_name = "1.png"
save_path = './split-image'  # create dir split
Path(save_path).mkdir(parents=True, exist_ok=True)

# block size
height = 416
width = 416

# overlap （如果不想重叠，可以置为0）
over_x = 27
over_y = 27
h_val = height - over_x
w_val = width - over_y

# Set whether to discard an image that does not meet the size
mandatory = False
img = cv2.imread(file_name)

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
        temp_path = save_path + '/' + str(i) + '_' + str(j) + '_'
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
        elif (width + j * w_val) > original_width and (i * h_val + height) > original_height:  # Judge the last slide
            temp = img[i * h_val:original_height, j * w_val:original_width, :]
            temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
            cv2.imwrite(temp_path, temp)
            images_temp.append(temp)
        else:
            temp = img[i * h_val:i * h_val + height, j * w_val:j * w_val + width, :]
            temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
            cv2.imwrite(temp_path, temp)
            images_temp.append(temp)  # The rest of the complete

    images.append(images_temp)

print(len(images))
