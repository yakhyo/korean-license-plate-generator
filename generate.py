import os
import random
import uuid

import cv2
import numpy as np


class ImageGenerator:
    def __init__(self, save_dir, plates_dir, nums_dir, chars_dir):
        self.save_dir = save_dir
        self.plates_dir = plates_dir

        # create directories to save images and labels
        for name in "labels", "images":
            os.makedirs(os.path.join(self.save_dir, name), exist_ok=True)

        # load number
        self.numbers = []
        self.number_list = []
        for filename in os.listdir(nums_dir):
            img = cv2.imread(os.path.join(nums_dir, filename))
            self.numbers.append(img)
            self.number_list.append(filename.split(".")[0])

        # load character
        self.char_list = []
        self.chars = []
        for filename in os.listdir(chars_dir):
            img = cv2.imread(os.path.join(chars_dir, filename))
            self.chars.append(img)
            self.char_list.append(filename.split(".")[0])

    @staticmethod
    def add(plate, char):
        img2gray = cv2.cvtColor(char, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img1 = cv2.bitwise_and(plate, plate, mask=mask)
        img2 = cv2.bitwise_and(char, char, mask=mask_inv)
        output = cv2.add(img1, img2)

        return output

    @staticmethod
    def random_bright(img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        img = np.array(img, dtype=np.float64)
        random_bright = .5 + np.random.uniform()
        img[:, :, 2] = img[:, :, 2] * random_bright
        img[:, :, 2][img[:, :, 2] > 255] = 255
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

        return img

    def type_a(self, num):
        numbers = [cv2.resize(number, (56, 83)) for number in self.numbers]
        chars = [cv2.resize(char, (60, 83)) for char in self.chars]

        for p in os.listdir(self.plates_dir):
            plate = cv2.imread(os.path.join(self.plates_dir, p))
            for i in range(num):
                unique_id = str(uuid.uuid1())
                with open(f"{self.save_dir}/labels/{unique_id}.txt", "a") as f:
                    Plate = cv2.resize(plate, (520, 110))
                    # row -> y , col -> x
                    row, col = 13, 35

                    # number 1
                    x1, y1 = col, row
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x2, y2 = x1 + 56, y1 + 83
                    x_center_norm, y_center_norm = (x1 + x2) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 56
                    x2, y1 = x2, y1
                    # number 2
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x3, y2 = x2 + 56, y2
                    x_center_norm, y_center_norm = (x2 + x3) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 56
                    x3, y1 = x3, y1
                    # character 3
                    patch = Plate[row:row + 83, col:col + 60, :]
                    Plate[row:row + 83, col:col + 60, :] = self.add(patch, self.random_bright(chars[i % 40]))

                    x4, y2 = x3 + 60, y2
                    x_center_norm, y_center_norm = (x3 + x4) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (60 / 520), (83 / 110)

                    cls_idx = names.index(self.char_list[i % 40])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += (60 + 36)
                    x4, y1 = col, y1
                    # number 4
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x5, y2 = x4 + 56, y2
                    x_center_norm, y_center_norm = (x4 + x5) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 56
                    x5, y1 = x5, y1
                    # number 5
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x6, y2 = x5 + 56, y2
                    x_center_norm, y_center_norm = (x5 + x6) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 56
                    x6, y1 = x6, y1
                    # number 6
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x7, y2 = x6 + 56, y2
                    x_center_norm, y_center_norm = (x6 + x7) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 56
                    x7, y1 = x7, y1
                    # number 7
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 56, :]
                    Plate[row:row + 83, col:col + 56, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x8, y2 = x7 + 56, y2
                    x_center_norm, y_center_norm = (x7 + x8) / (2 * 520), (y1 + y2) / (2 * 110)
                    width_norm, height_norm = (56 / 520), (83 / 110)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                cv2.imwrite(f"{self.save_dir}/images/{unique_id}.jpg", Plate)

    def type_b(self, num):
        numbers = [cv2.resize(number, (45, 83)) for number in self.numbers]
        chars = [cv2.resize(char, (49, 70)) for char in self.chars]
        for p in os.listdir(self.plates_dir):
            plate = cv2.imread(os.path.join(self.plates_dir, p))
            for i in range(num):
                unique_id = str(uuid.uuid1())
                with open(f"{self.save_dir}/labels/{unique_id}.txt", 'a') as f:
                    Plate = cv2.resize(plate, (355, 155))
                    row, col = 45, 15  # row + 83, col + 45

                    # number 1
                    x1, y1 = col, row
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col:col + 45, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x2, y2 = x1 + 45, y1 + 83
                    x_center_norm, y_center_norm = (x1 + x2) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 45
                    x2, y1 = x2, y1
                    # number 2
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col:col + 45, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x3, y2 = x2 + 45, y2
                    x_center_norm, y_center_norm = (x2 + x3) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 45
                    x3, y1 = x3, y1
                    # number 3
                    patch = Plate[row + 12:row + 82, col + 2:col + 49 + 2, :]
                    Plate[row + 12:row + 82, col + 2:col + 49 + 2, :] = self.add(
                        patch, self.random_bright(chars[i % 40]))

                    x4, y2 = x3 + 49, y2
                    x_center_norm, y_center_norm = (x3 + x4) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (49 / 355), (70 / 155)
                    cls_idx = names.index(self.char_list[i % 40])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 49 + 2
                    x4, y1 = col, y1
                    # numbers 4
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col + 2:col + 45 + 2, :] = self.add(patch,
                                                                            self.random_bright(numbers[rand_int]))

                    x5, y2 = x4 + 45 + 2, y2
                    x_center_norm, y_center_norm = (x4 + x5) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 45 + 2
                    x5, y1 = col, y1
                    # number 5
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col:col + 45, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x6, y2 = x5 + 45, y2
                    x_center_norm, y_center_norm = (x5 + x6) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 45
                    x6, y1 = x6, y1
                    # number 6
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col:col + 45, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x7, y2 = x6 + 45, y2
                    x_center_norm, y_center_norm = (x6 + x7) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                    col += 45
                    x7, y1 = x7, y1
                    # number 7
                    rand_int = random.randint(0, 9)
                    patch = Plate[row:row + 83, col:col + 45, :]
                    Plate[row:row + 83, col:col + 45, :] = self.add(patch, self.random_bright(numbers[rand_int]))

                    x8, y2 = x7 + 45, y2
                    x_center_norm, y_center_norm = (x7 + x8) / (2 * 355), (y1 + y2) / (2 * 155)
                    width_norm, height_norm = (45 / 355), (83 / 155)

                    cls_idx = names.index(self.number_list[rand_int])
                    f.write(f'{cls_idx} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n')

                cv2.imwrite(f"{self.save_dir}/images/{unique_id}.jpg", Plate)


if __name__ == '__main__':

    with open('./assets/names.txt', 'r') as file:
        names = [name.strip() for name in file.readlines()]

    if not os.path.exists('./result'):
        os.mkdir('./result')
    if not os.path.exists('./result/images'):
        os.mkdir('./result/images')
    if not os.path.exists('./result/labels'):
        os.mkdir('./result/labels')

    Type_A1 = ImageGenerator(save_dir='./result/',
                             plates_dir='./assets/plates/type_a',
                             nums_dir='./assets/nums/',
                             chars_dir='./assets/chars/')

    Type_B1 = ImageGenerator(save_dir='./result/',
                             plates_dir='./assets/plates/type_b',
                             nums_dir='./assets/nums/',
                             chars_dir='./assets/chars/')

    num_img = 120

    Type_A1.type_a(num_img)
    print("Type 1 finish")
    Type_B1.type_b(num_img)
    print("Type 2 finish")
