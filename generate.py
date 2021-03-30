import os
import random
import cv2
import numpy as np


class ImageGenerator:
    def __init__(self, save_path, plates_path, nums_path, chars_path, transparent=False):
        self.save_path = save_path
        # Plate
        self.list_ = os.listdir(plates_path)

        self.plate = plates_path

        # Load Numbers
        file_path = nums_path
        file_list = os.listdir(file_path)
        self.Number = list()
        self.number_list = list()
        for file_ in file_list:
            img_path = os.path.join(file_path, file_)
            if transparent:
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                trans_mask = img[:, :, 3] == 0
                img[trans_mask] = [255, 255, 255, 255]
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                img = cv2.imread(img_path)

            self.Number.append(img)
            self.number_list.append(file_[0:-4])

        # Load Chars
        file_path = chars_path
        file_list = os.listdir(file_path)
        self.char_list = list()
        self.Char1 = list()
        for file_ in file_list:
            img_path = os.path.join(file_path, file_)
            if transparent:
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                trans_mask = img[:, :, 3] == 0
                img[trans_mask] = [255, 255, 255, 255]
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                img = cv2.imread(img_path)

            self.Char1.append(img)
            self.char_list.append(file_[0:-4])

    @staticmethod
    def add(background_image, char):
        roi = background_image
        img2gray = cv2.cvtColor(char, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
        img2_fg = cv2.bitwise_and(char, char, mask=mask_inv)
        dst = cv2.add(img1_bg, img2_fg)

        return dst

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

    def Type_A(self, num, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.Char1]
        count_a = 0
        for p in self.list_:
            plate = cv2.imread(os.path.join(self.plate, p))
            for i in range(num):
                f = open(f'./result/labels/image_a_{count_a}.txt', 'a')
                Plate = cv2.resize(plate, (520, 110))
                label = "Z"
                # row -> y , col -> x

                row, col = 13, 35
                # number 1
                x1, y1 = col, row
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x2, y2 = x1 + 56, y1 + 83
                x_r, y_r = (x1 + x2) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 56
                x2, y1 = x2, y1
                # number 2
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x3, y2 = x2 + 56, y2
                x_r, y_r = (x2 + x3) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 56
                x3, y1 = x3, y1
                # character 3
                label += self.char_list[i % 40]
                Plate[row:row + 83, col:col + 60, :] = self.add(Plate[row:row + 83, col:col + 60, :],
                                                                self.random_bright(char[i % 40]))
                x4, y2 = x3 + 60, y2
                x_r, y_r = (x3 + x4) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (60 / 520), (83 / 110)
                class_name = names.index(self.char_list[i % 40])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += (60 + 36)
                x4, y1 = col, y1
                # number 4
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x5, y2 = x4 + 56, y2
                x_r, y_r = (x4 + x5) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 56
                x5, y1 = x5, y1
                # number 5
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x6, y2 = x5 + 56, y2
                x_r, y_r = (x5 + x6) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 56
                x6, y1 = x6, y1
                # number 6
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x7, y2 = x6 + 56, y2
                x_r, y_r = (x6 + x7) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 56
                x7, y1 = x7, y1
                # number 7
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 56, :] = self.add(Plate[row:row + 83, col:col + 56, :],
                                                                self.random_bright(number[rand_int]))
                x8, y2 = x7 + 56, y2
                x_r, y_r = (x7 + x8) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (56 / 520), (83 / 110)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)
                col += 56
                f.close()

                if save:
                    cv2.imwrite(self.save_path + "image_a_" + str(count_a) + ".jpg", Plate)
                    count_a += 1
                else:
                    pass

    def Type_B(self, num, save=False):
        number = [cv2.resize(number, (45, 83)) for number in self.Number]
        char = [cv2.resize(char1, (49, 70)) for char1 in self.Char1]
        count_b = 0
        for p in self.list_:
            plate = cv2.imread(os.path.join(self.plate, p))
            for i in range(num):
                f = open(f'./result/labels/image_b_{count_b}.txt', 'a')
                Plate = cv2.resize(plate, (355, 155))
                label = ''
                row, col = 45, 15  # row + 83, col + 45

                # number 1
                x1, y1 = col, row
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 45, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                self.random_bright(number[rand_int]))

                x2, y2 = x1 + 45, y1 + 83
                x_r, y_r = (x1 + x2) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 45
                x2, y1 = x2, y1
                # number 2
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 45, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                self.random_bright(number[rand_int]))
                x3, y2 = x2 + 45, y2
                x_r, y_r = (x2 + x3) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 45
                x3, y1 = x3, y1
                # number 3
                label += self.char_list[i % 40]
                Plate[row + 12:row + 82, col + 2:col + 49 + 2, :] = self.add(
                    Plate[row + 12:row + 82, col + 2:col + 49 + 2, :],
                    self.random_bright(char[i % 40]))

                x4, y2 = x3 + 49, y2
                x_r, y_r = (x3 + x4) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (49 / 355), (70 / 155)
                class_name = names.index(self.char_list[i % 40])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 49 + 2
                x4, y1 = col, y1
                # number 4
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col + 2:col + 45 + 2, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                        self.random_bright(number[rand_int]))

                x5, y2 = x4 + 45 + 2, y2
                x_r, y_r = (x4 + x5) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)
                col += 45 + 2
                x5, y1 = col, y1
                # number 5
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 45, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                self.random_bright(number[rand_int]))
                x6, y2 = x5 + 45, y2
                x_r, y_r = (x5 + x6) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)
                col += 45
                x6, y1 = x6, y1

                # number 6
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 45, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                self.random_bright(number[rand_int]))

                x7, y2 = x6 + 45, y2
                x_r, y_r = (x6 + x7) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)
                col += 45
                x7, y1 = x7, y1

                # number 7
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 83, col:col + 45, :] = self.add(Plate[row:row + 83, col:col + 45, :],
                                                                self.random_bright(number[rand_int]))
                x8, y2 = x7 + 45, y2
                x_r, y_r = (x7 + x8) / (2 * 355), (y1 + y2) / (2 * 155)
                w_r, h_r = (45 / 355), (83 / 155)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)
                col += 45
                f.close()

                if save:
                    cv2.imwrite(self.save_path + "image_b_" + str(count_b) + ".jpg", Plate)
                    count_b += 1
                    # cv2.imwrite(self.save_path + label + ".jpg", Plate)  # If you want to save labels as image name
                else:
                    print('Images are not saved')


if __name__ == '__main__':

    with open('./assets/names.txt', 'r') as file:
        names = file.readlines()

    names = [i.strip() for i in names]

    if not os.path.exists('./result'):
        os.mkdir('./result')
    if not os.path.exists('./result/images'):
        os.mkdir('./result/images')
    if not os.path.exists('./result/labels'):
        os.mkdir('./result/labels')

    Type_A1 = ImageGenerator(save_path='./result/images/',
                             plates_path='./assets/plates/type_a',
                             nums_path='./assets/nums/',
                             chars_path='./assets/chars/')

    Type_B1 = ImageGenerator(save_path='./result/images/',
                             plates_path='./assets/plates/type_b',
                             nums_path='./assets/nums/',
                             chars_path='./assets/chars/')

    num_img = 120

    Type_A1.Type_A(num_img, save=True)
    print("Type 1 finish")
    Type_B1.Type_B(num_img, save=True)
    print("Type 2 finish")
