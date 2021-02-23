import os

classes = []
annotations = [file for file in os.listdir('./result/labels/')]
for file in annotations:
    with open(os.path.join('./result/labels/', file)) as ann:
        lines = ann.readlines()
    for line in lines:
        classes.append(line.split(' ')[0])

result = sorted([int(i) for i in list(set(classes))])
with open('names.txt') as n:
    names = n.readlines()

for i in range(len(names)):
    print(names[i].strip(), classes.count(str(i)))