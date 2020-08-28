
# coding: utf-8

# In[6]:


import cv2
import numpy
import os
import xml.etree.ElementTree as ET
import argparse
import ruamel.yaml
from tqdm import trange

class xml2txt():
    '''
    Usage:
        cls = list of class names you have defined ex : ['mask', 'coating',...]
        path = path to .xml files
        savePath = path to save .txt files      
    The converted .txt files will name after original .xml files' name
    '''
    def __init__(self, cls, path, savePath):
        self.cls = cls
        self.path = path
        self.save = savePath
    
    def _convert(self, size, box):
        dw = 1./(size[0])
        dh = 1./(size[1])
        x = (box[0] + box[1])/2.0 - 1
        y = (box[2] + box[3])/2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)
    
    def convert(self):

        files = os.listdir(self.path)
        l = len(files)
        print("Find {} files...".format(l))
        with trange(l, ascii=True) as t:
            for file, i in zip(files, t):
                t.set_description('{}/{}'.format(i + 1, l))
                filename = file.split('.xml')[0]
                in_file = open(os.path.join(self.path, file), encoding='utf-8')
                tree = ET.parse(in_file)
                root = tree.getroot()
                text_file = open(os.path.join(self.save, filename) + ".txt", "w")
                if root.find('size'):
                    size = root.find('size')
                    w = int(size.find('width').text)    
                    h = int(size.find('height').text)   

                    for obj in root.iter('object'):

                        difficult = obj.find('difficult').text
                        cls = obj.find('name').text
                        if cls not in classes or int(difficult)==1:
                            continue
                        cls_id = classes.index(cls)
                        xmlbox = obj.find('bndbox')

                        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                        bb = self._convert((w,h), b)
                        text_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')   
                text_file.close()
        t.close()
        print('Process done!!')


# In[10]:


if __name__ == '__main__':
    with open('classes.yaml') as fp:
        str_data = fp.read()
    classes = ruamel.yaml.load(str_data, Loader=ruamel.yaml.Loader)['names']
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type = str, default = './xml', help='path to .xml files')
    parser.add_argument('--savePath', type=str, default = './txt', help='path to save .txt files')
    opt = parser.parse_args()
    #print(opt) 
    converter = xml2txt(classes, opt.path, opt.savePath)
    converter.convert()

