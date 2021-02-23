# Korean License Plate Generator

```buildoutcfg
git clone ....
```
`assets` folder tree:
```buildoutcfg
assets
├── chars
    ├── a.jpg
    ├── ba.jpg
    ├── bae.jpg
    └── ...
├── nums
    ├── a.jpg
    ├── ba.jpg
    ├── bae.jpg
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
```

This code generates `result` folder:

```buildoutcfg
python generate.py
```

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
To check the class distribution
```buildoutcfg
python distrib.py
```
