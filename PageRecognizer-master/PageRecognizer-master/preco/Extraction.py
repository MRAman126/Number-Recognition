# -*- coding: utf-8 -*-

import operator

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt

from misc.ChainUnit import ChainUnit



class Extraction(ChainUnit):

    check_point=None
    target_rects=[]
    image_shapes=None

    def handle(self, timage):
        print "Extraction"
        self.image_shapes = timage.img.shape
        # V1
        # self.findTargetRects(timage)

        # V2
        blank_image = np.zeros(self.image_shapes, np.uint8)
        blank_image = cv2.cvtColor( blank_image, cv2.COLOR_GRAY2BGR );

        target_rects = self.find_contours_bounding_rects(timage.img)

        pagination_rects = self.find_pagination_regard_rects(target_rects, 2)

        timage.img = cv2.cvtColor( timage.img, cv2.COLOR_GRAY2BGR );
        for i,rect in enumerate(pagination_rects):

            self.draw_rect(rect, timage.img, color=[0,0,250])

        timage.render()

        super(Extraction, self).handle(timage)

    def kmeans(self, rects):
        """
        Input: List of rects
        OUTPUT: List of clusters. 
        Use opencv kmeans.
        """
        points = np.vstack([ list(item[:2]) for item in rects])

        temp, classified_points, centroids = cv2.kmeans(data=np.array(points, np.float32), 
                                            K=2, 
                                            bestLabels=None,
                                            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), 
                                            attempts=1, 
                                            flags=cv2.KMEANS_PP_CENTERS)   # KMEANS_RANDOM_CENTERS KMEANS_PP_CENTERS

        return classified_points, centroids

    def classify_rects(self, rects_generator):
        """
        Input: List of rects
        OUTPUT: (List of labeled rects, centroids)
        """
        classified_points, centroids = self.kmeans(rects_generator)
        labled_rects = zip(rects_generator, classified_points)
        #TODO: make label 1 as pagination label
        return labled_rects, centroids

    def calculate_pagination_label(self, centroids):
        """
        Input: centroids
        OUTPUT: Pagination label 0 or 1
        Algo based on calculating distance between top right corner and each centroid.
        """
        tr_point = np.array((self.image_shapes[1], 0))
        centroids = [np.array(c) for c in centroids]

        # pagination_label = 0 if ((centroids[0][0] > centroids[1][0]) and (centroids[0][1] < centroids[1][1])) else 1
        pagination_label = 0 if (np.linalg.norm(tr_point-centroids[0]) < np.linalg.norm(tr_point-centroids[1])) else 1

        return pagination_label

    def find_pagination_regard_rects(self, target_rects, iterations):
        """
        Input: List of rects
        OUTPUT: List of pagination regard rects
        """
        if iterations==0:
            return target_rects

        labled_rects, centroids = self.classify_rects(target_rects)

        pagination_label = self.calculate_pagination_label(centroids)
        target_labled_rects = list(filter(lambda x: x[1] == pagination_label, labled_rects))

        pagination_rects = [item for item, a in target_labled_rects]

        # print np.std([item[:2] for item in pagination_rects])

        return self.find_pagination_regard_rects(pagination_rects, iterations-1)

    def find_contours_bounding_rects(self, gray_scale_img):
        """
        Input: Grayscale MAT
        OUTPUT: List of filtered bounding rects 
        # OUTPUT: Generator of filtered bounding rects list
        """
        contours, hierarchy = cv2.findContours(gray_scale_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(gray_scale_img, contours, -1, [255], -1, maxLevel=1)

        target_bound_rects = []

        for contour in contours:
            area = cv2.contourArea(contour)
            length = cv2.arcLength(contour, closed=True)

            # Check for compactness ( area and length ratio)
            if float(length) > 0 and 10 > (float(area) / float(length)) > 2:
                contour_poly = cv2.approxPolyDP(contour, 4 , True)
                bound_rect = cv2.boundingRect(contour_poly)
                (w, h) = bound_rect[2:]

                # Width and height ratio
                if 0.1 < (float(w) / float(h)) < 7:
                    # yield bound_rect
                    target_bound_rects.append(bound_rect)

        return target_bound_rects

    def __log(self, msg):
        print "[Preprocessing] => ", msg

    def draw_rect(self, rect, img, color=[255, 0, 255]):
        (w, h) = rect[2:]
        # (top left angle, bottom right angle)
        (tl, br) = (rect[:2], tuple(map(operator.add, rect[:2], (w, h))))
        cv2.rectangle(img, tl, br, color, 2, 8, 0);

    def checkTargetArea(self, point):
        if ((point[0] > self.check_point[0]) and (point[1] < self.check_point[1])):
            return True
        else:
            return False

    def findTargetRects(self, t):
        self.__log("Detecting contours...")

        # Create RGB blank image
        blank_image = np.zeros(t.img.shape, np.uint8)
        blank_image = cv2.cvtColor( blank_image, cv2.COLOR_GRAY2BGR );

        (h, w, c) = blank_image.shape

        # Draw pagination search area
        target_area = ((2* w/3), 0, w/3, h/5)
        self.check_point = (target_area[0],target_area[3])

        # self.draw_rect(target_area, blank_image)

        # Compute contours
        contours, hierarchy = cv2.findContours(t.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(blank_image, contours, -1, [255, 255, 255], -1, maxLevel=1)
        # cv2.drawContours(t.img, contours, -1, [255], -1, maxLevel=1)

        for contour in contours:
            area = cv2.contourArea(contour)
            length = cv2.arcLength(contour, closed=True)

            # Check for compactness ( area and length ratio)
            if float(length) > 0 and 10 > (float(area) / float(length)) > 2:
                contour_poly = cv2.approxPolyDP(contour, 4 , True)
                bound_rect = cv2.boundingRect(contour_poly)
                (w, h) = bound_rect[2:]

                # Width and height ratio
                if 0.1 < (float(w) / float(h)) < 7:
                    # if (self.checkTargetArea(bound_rect[:2])):
                    # self.draw_rect(bound_rect, blank_image)
                        # cv2.drawContours(blank_image, contour, -1, [255, 255, 255], -1, maxLevel=1)

                    self.target_rects.append(bound_rect)

        # t.render(img=blank_image)

        self.narrowSearchArea(t, blank_image)

    def narrowSearchArea(self, t, blank_image):

        classified_points = self.cluster(self.target_rects)
        labled_rects = zip(self.target_rects, classified_points)
        target_labled_rects = list(filter(lambda x: x[1] == 0, labled_rects))

        target_rects = [item for item, a in target_labled_rects]

        for rect, allocation in target_labled_rects:
            if allocation == 0:
                color = (255,0,0)
            elif allocation == 1:
                color = (0,0,255)
            elif allocation == 2:
                color = (0,255,0)
            self.draw_rect(rect, blank_image, color=color)

        t.render(img=blank_image)
