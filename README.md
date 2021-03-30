# Korean License Plate Generator

Run
```buildoutcfg
git clone https://github.com/yakhyo/Korean-License-Plate-Generate.git
python generate.py # to generate passanger car license plate images
python generate_truck.py # to generate truck license plate images
```

`assets` folder:

```buildoutcfg
assets
├── chars
    ├── a.jpg
    ├── ba.jpg
    ├── bae.jpg
    └── ...
├── chars_truck
    ├── a.jpg
    ├── ba.jpg
    ├── bae.jpg
    └── ...
├── nums
    ├── 0.jpg
    ├── 1.jpg
    ├── 2.jpg
    └── ...
├── region1
    ├── 001_bu.jpg
    ├── 002_chung.jpg
    ├── 003_chung.jpg
    └── ...
├── region2
    ├── 001_san.jpg
    ├── 002_buk.jpg
    ├── 003_nam.jpg
    └── ...
└── plates
    ├── type_a
        ├── plate_1jpg
        ├── plate_2.jpg
        ├── plate_3.jpg
        └── ... 
    └── type_b
        ├── plate_1jpg
        ├── plate_2.jpg
        ├── plate_3.jpg
        └── ...
    └── type_c
        ├── plate_1jpg
        ├── plate_2.jpg
        ├── plate_3.jpg
        └── ...
    └── type_d
        ├── plate_1jpg
        ├── plate_2.jpg
        ├── plate_3.jpg
        └── ...
└── names.txt
```
This code generates two types of passenger car and turck license plate images:

Type A:
<div align="center">

![License plate type 1](sample/image_a_0.jpg)

</div>

Type B
<div align="center">

![License plate type 2](sample/image_b_0.jpg)

</div>

Type C
<div align="center">

![License plate type 3](sample/image_ax_4.jpg)

</div>

Type D
<div align="center">

![License plate type 4](sample/image_dx_30.jpg)

</div>

`names.txt` consists from numbers and letter combinations:

`0 1 2 3 4 5 6 7 8 9 ga na da ra ma ba sa a cha ha geo neo deo reo meo beo seo eo cheo heo go no do ro mo bo so o cho ho gu nu du ru mu bu su u chu bae`

After running the `generate.py` file, `result` folder will appear:
```buildoutcfg
result
├── images
    ├── image_a_0.jpg
    ├── image_a_1.jpg
    ├── image_a_2.jpg
    └── ...
└── labels
    ├── image_a_0.txt
    ├── image_a_1.txt
    ├── image_a_2.txt
    └── ...
```

* Labels are prepared according to YOLO labelling format

To check the class distribution:

```buildoutcfg
python distrib.py
```

Reference

1. [https://github.com/qjadud1994/Korean-license-plate-Generator](https://github.com/qjadud1994/Korean-license-plate-Generator)