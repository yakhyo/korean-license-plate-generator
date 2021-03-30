import os
import random
import cv2
import numpy as np


class ImageGenerator:
    def __init__(self, save_path, plates_path, nums_path, chars_path, regions1, regions2, transparent=False):
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
        self.Char = list()
        for file_ in file_list:
            img_path = os.path.join(file_path, file_)
            if transparent:
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                trans_mask = img[:, :, 3] == 0
                img[trans_mask] = [255, 255, 255, 255]
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                img = cv2.imread(img_path)

            self.Char.append(img)
            self.char_list.append(file_[0:-4])

        # Load Regions
        file_path = regions1
        file_list = os.listdir(file_path)

        self.region1_list = list()
        self.Regions1 = list()
        for file_ in file_list:
            img_path = os.path.join(file_path, file_)
            if transparent:
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                trans_mask = img[:, :, 3] == 0
                img[trans_mask] = [255, 255, 255, 255]
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                img = cv2.imread(img_path)

            self.Regions1.append(img)
            self.region1_list.append(file_[0:-4])

        file_path = regions2
        file_list = os.listdir(file_path)

        self.region2_list = list()
        self.Regions2 = list()
        for file_ in file_list:
            img_path = os.path.join(file_path, file_)
            if transparent:
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                trans_mask = img[:, :, 3] == 0
                img[trans_mask] = [255, 255, 255, 255]
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                img = cv2.imread(img_path)

            self.Regions2.append(img)
            self.region2_list.append(file_[0:-4])

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

    def Type_C(self, num, save=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number]
        region_1 = [cv2.resize(region, (44, 60)) for region in self.Regions1]
        region_2 = [cv2.resize(region, (44, 60)) for region in self.Regions2]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.Char]
        count_a = 0
        for p in self.list_:
            plate = cv2.imread(os.path.join(self.plate, p))
            for i, Iter in enumerate(range(num)):
                f = open(f'./result/labels/image_ax_{count_a}.txt', 'a')
                Plate = cv2.resize(plate, (335, 170))

                label = str()
                # row -> y , col -> x
                row, col = 8, 76
                x1, y1 = col, row
                # region
                label += self.region1_list[i % 16][4:]
                Plate[row:row + 60, col:col + 44, :] = self.add(Plate[row:row + 60, col:col + 44, :],
                                                                self.random_bright(region_1[i % 16]))

                col += 44
                x2, y2 = col, y1 + 60
                x_r, y_r = (x1 + x2) / (2 * 335), (y1 + y2) / (2 * 170)
                w_r, h_r = (44 / 335), (60 / 170)
                class_name = names.index(self.region1_list[i % 16][4:])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x3, y1 = x2, y1
                label += self.region2_list[i % 16][4:]
                Plate[row:row + 60, col:col + 44, :] = self.add(Plate[row:row + 60, col + 44:col + 88, :],
                                                                self.random_bright(region_2[i % 16]))
                col += 44
                x4, y2 = col, y2
                x_r, y_r = (x3 + x4) / (2 * 335), (y1 + y2) / (2 * 170)
                w_r, h_r = (44 / 335), (60 / 170)
                class_name = names.index(self.region2_list[i % 16][4:])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 8
                x5, y1 = col, y1
                # number 1
                rand_int = random.randint(8, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 60, col:col + 44, :] = self.add(Plate[row:row + 60, col:col + 44, :],
                                                                self.random_bright(number1[rand_int]))
                col += 44
                x6, y2 = col, y2
                x_r, y_r = (x5 + x6) / (2 * 335), (y1 + y2) / (2 * 170)
                w_r, h_r = (44 / 335), (60 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x7, y1 = col, y1
                # number 2
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 60, col:col + 44, :] = self.add(Plate[row:row + 60, col:col + 44, :],
                                                                self.random_bright(number1[rand_int]))
                x8, y2 = col + 44, y2
                x_r, y_r = (x7 + x8) / (2 * 335), (y1 + y2) / (2 * 170)
                w_r, h_r = (44 / 335), (60 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                row, col = 72, 8

                x9, y3 = col, row
                # character 3
                label += self.char_list[i % 5]
                Plate[row:row + 62, col:col + 64, :] = self.add(Plate[row:row + 62, col:col + 64, :],
                                                                self.random_bright(char[i % 5]))
                col += 64
                x10, y4 = col, y3 + 62
                x_r, y_r = (x10 + x9) / (2 * 335), (y3 + y4) / (2 * 170)
                w_r, h_r = (64 / 335), (62 / 170)
                class_name = names.index(self.char_list[i % 5])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x11, y3 = x10, y3
                # number 4
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 90, col:col + 64, :] = self.add(Plate[row:row + 90, col:col + 64, :],
                                                                self.random_bright(number2[rand_int]))
                col += 64
                x12, y5 = col, row + 90
                x_r, y_r = (x12 + x11) / (2 * 335), (y3 + y5) / (2 * 170)
                w_r, h_r = (64 / 335), (90 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x13, y3 = x12, y3
                # number 5
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 90, col:col + 64, :] = self.add(Plate[row:row + 90, col:col + 64, :],
                                                                self.random_bright(number2[rand_int]))
                col += 64
                x14, y5 = col, y5
                x_r, y_r = (x14 + x13) / (2 * 335), (y3 + y5) / (2 * 170)
                w_r, h_r = (64 / 335), (90 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x15, y3 = col, y3
                # number 6
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 90, col:col + 64, :] = self.add(Plate[row:row + 90, col:col + 64, :],
                                                                self.random_bright(number2[rand_int]))
                col += 64
                x16, y5 = col, y5
                x_r, y_r = (x16 + x15) / (2 * 335), (y3 + y5) / (2 * 170)
                w_r, h_r = (64 / 335), (90 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x17, y3 = col, y3
                # number 7
                rand_int = random.randint(0, 9)
                label += self.number_list[rand_int]
                Plate[row:row + 90, col:col + 64, :] = self.add(Plate[row:row + 90, col:col + 64, :],
                                                                self.random_bright(number2[rand_int]))
                x18, y5 = col + 64, y5
                x_r, y_r = (x18 + x17) / (2 * 335), (y3 + y5) / (2 * 170)
                w_r, h_r = (64 / 335), (90 / 170)
                class_name = names.index(self.number_list[rand_int])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                Plate = self.random_bright(Plate)
                if save:
                    txt = f'image_ax_{count_a}'
                    cv2.imwrite(self.save_path + txt + ".jpg", Plate)
                else:
                    cv2.imshow(label, Plate)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                count_a += 1
                f.close()

    def Type_D(self, num, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number]
        char = [cv2.resize(char, (60, 83)) for char in self.Char]
        region_1 = [cv2.resize(region, (60, 42)) for region in self.Regions1]
        region_2 = [cv2.resize(region, (60, 42)) for region in self.Regions2]
        count_d = 0
        for p in self.list_:
            plate = cv2.imread(os.path.join(self.plate, p))
            for i in range(num):
                f = open(f'./result/labels/image_dx_{count_d}.txt', 'a')
                Plate = cv2.resize(plate, (520, 110))
                label = "Z"
                # row -> y , col -> x

                row, col = 13, 25
                x_0, y_0 = 25, 13
                # region
                label += self.region1_list[i % 16][4:]
                Plate[row:row + 42, col:col + 60, :] = self.add(Plate[row:row + 42, col:col + 60, :],
                                                                self.random_bright(region_1[i % 16]))

                x_1, y_1 = x_0 + 60, y_0 + 42
                x_r, y_r = (x_0 + x_1) / (2 * 520), (y_0 + y_1) / (2 * 110)
                w_r, h_r = (60 / 520), (42 / 110)
                class_name = names.index(self.region1_list[i % 16][4:])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                x_2, y_2 = x_0, y_0 + 42

                Plate[row + 42:row + 84, col:col + 60, :] = self.add(Plate[row + 42:row + 84, col:col + 60, :],
                                                                     self.random_bright(region_2[i % 16]))

                x_3, y_3 = x_1, y_0 + 84

                x_r, y_r = (x_2 + x_3) / (2 * 520), (y_2 + y_3) / (2 * 110)
                w_r, h_r = (60 / 520), (42 / 110)
                class_name = names.index(self.region2_list[i % 16][4:])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += 60
                # number 1
                x1, y1 = col, row
                rand_int = random.randint(8, 9)
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
                label += self.char_list[i % 5]
                Plate[row:row + 83, col:col + 60, :] = self.add(Plate[row:row + 83, col:col + 60, :],
                                                                self.random_bright(char[i % 5]))
                x4, y2 = x3 + 60, y2
                x_r, y_r = (x3 + x4) / (2 * 520), (y1 + y2) / (2 * 110)
                w_r, h_r = (60 / 520), (83 / 110)
                class_name = names.index(self.char_list[i % 5])
                txt = f'{class_name} {x_r} {y_r} {w_r} {h_r}\n'
                f.write(txt)

                col += (40 + 36)
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
                    cv2.imwrite(self.save_path + "image_dx_" + str(count_d) + ".jpg", Plate)
                    count_d += 1
                else:
                    pass


if __name__ == '__main__':

    with open('./assets/names.txt', 'r') as file:
        names = file.readlines()

    names = [i.strip() for i in names]
    print(names)

    if not os.path.exists('./result'):
        os.mkdir('./result')
    if not os.path.exists('./result/images'):
        os.mkdir('./result/images')
    if not os.path.exists('./result/labels'):
        os.mkdir('./result/labels')

    TruckNP_type_1 = ImageGenerator(save_path='./result/images/',
                                    plates_path='./assets/plates/type_c',
                                    nums_path='./assets/nums/',
                                    chars_path='./assets/chars_truck/',
                                    regions1='./assets/region1/',
                                    regions2='./assets/region2/')

    TruckNP_type_2 = ImageGenerator(save_path='./result/images/',
                                    plates_path='./assets/plates/type_d',
                                    nums_path='./assets/nums/',
                                    chars_path='./assets/chars_truck/',
                                    regions1='./assets/region1/',
                                    regions2='./assets/region2/')

    num_img = 5

    TruckNP_type_1.Type_C(num_img, save=True)
    TruckNP_type_2.Type_D(3 * num_img, save=True)
