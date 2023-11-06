#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import optparse
import cv2
import numpy
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


from preco.TImage import TImage

from classifier import classify

from digit_binarization import apply_filters


if __name__ == '__main__':
    files_list = ['1.png', '2.png', '3.png', '4.png'] #'1.png', '2.png', '3.png',
    
    for file in files_list:
        timage = TImage(file)
        cv2.imshow('image', timage.img)
        cv2.waitKey(0)
        img_filtered = cv2.resize(apply_filters(timage.img), (28, 28))
        max_value = range(10)
        index = range(10)
        for angle in xrange(-10, 50, 5):
            #print img_filtered.shape
            rot_mat = cv2.getRotationMatrix2D((img_filtered.shape[0]/2, img_filtered.shape[1]/2), angle, 1)
            img_rotated = cv2.warpAffine(img_filtered, rot_mat, (img_filtered.shape[0], img_filtered.shape[1]),flags=cv2.INTER_LINEAR)
            #print img_rotated.shape
            img_scaled = cv2.resize(img_rotated, (28, 28))
            cv2.imshow('scale', img_rotated)
            cv2.waitKey(0)
            z = [px / 255.0 for px in img_scaled.flatten('C').tolist()]
            #print z
            probs = classify(z)
            #print probs
            max_value[angle / 5] = max(probs)
            if max_value[angle / 5] < 0.5:
                index[angle / 5] = -1
            else:
                index[angle / 5] = probs.index(max_value[angle / 5])
        img = Image.open(file)
        draw = ImageDraw.Draw(img)
        
        max_value_overall = max(max_value)
        if max_value_overall < 0.5:
            s = 'ERROR'
        else:
            s = 'DIGIT: %i' % index[max_value.index(max_value_overall)]
        print s
        font = ImageFont.truetype("ARIAL.TTF", 20)
        draw.text((0, 0), s, (0, 255, 0), font=font)
        img.save('sample-out.jpg')
        cv2.imshow('image', TImage('sample-out.jpg').img)
        cv2.waitKey(0)
