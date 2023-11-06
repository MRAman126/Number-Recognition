# -*- coding: utf-8 -*-

import cv2
import numpy as np

from misc.ChainUnit import ChainUnit 

class Preprocessing(ChainUnit):
    threshold = 150

    def __log(self, msg):
        print "[Preprocessing] => ", msg

    def apply_blur(self, t):
        self.__log("Apply blur ... ")
        t.img = cv2.blur(t.img, (3,3))

    def apply_threshold(self, t) :
        self.__log("Apply threshold ... ")
        retval, t.img = cv2.threshold( t.img, self.threshold, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU )
        #threshold( t.img, t.img, 100, 255, THRESH_OTSU )

    def apply_denoise(self, t):
        self.__log("Apply denoise ... ")
        (contours, hierarchy) =  cv2.findContours( t.img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE )

        t.img = np.ones(t.img.shape, np.uint8) * 255
        color_parent = [0] * t.channels()
        color_child = [0] * t.channels()
        for i in range(len(contours)):
            if i == 0: continue
            area = cv2.contourArea(contours[i])
            if area > 100 and area < 10000:
                #print hierarchy
                if hierarchy[0,i, 3] == -1:
                    color = color_parent
                else:
                    color = color_child

                # cv2.drawContours( t.ref_img, contours, i, color, 1, 8, hierarchy, 0, None )
                cv2.drawContours( t.img, contours, i, color, -1, 8, hierarchy, 0, None )

    def apply_morphologyEx(self, t) :
        self.__log("Apply morphologyEx ... ")
        element = cv2.getStructuringElement( cv2.MORPH_CROSS, (3, 3), (1, 1))
        t.img = cv2.morphologyEx(t.img,  cv2.MORPH_OPEN, element)

    def prepare(self, timage):
        # ToDo(Make chain as in wiki.)
        self.apply_blur(timage)
        self.apply_threshold(timage)
        self.apply_morphologyEx(timage)
        self.apply_denoise(timage)

        timage.render()

    def handle(self, timage):
        print "Preprocessing..."
        self.prepare(timage)
        super(Preprocessing, self).handle(timage)