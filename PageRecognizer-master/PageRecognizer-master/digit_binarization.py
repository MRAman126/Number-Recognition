

import cv2
import optparse
import os.path
import numpy as np


def render(img, window_name="main"):
        cv2.destroyAllWindows()
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, img)
        cv2.waitKey(0)


def parse_input():
    usage = "usage: %prog [options] arg1"
    parser = optparse.OptionParser(usage)
    parser.add_option("-i", "--image", dest="path_to_image",
                  help="Path to image.", metavar="path_to_image")

    (options, args) = parser.parse_args()

    if (options.path_to_image is None):
        parser.print_help()
        exit(-1)
    elif not os.path.exists(options.path_to_image):
        parser.error('image does not exists')

    return options


def apply_filters(img):
    """
    Применение фильтров с целью эффективной бинаризации изображения.

    Вход: Gray Scale изображение
    Выход: Бинаризованное изображение
    """
    # edges = cv2.Canny(image=img,
    #               threshold1=100,
    #               threshold2=255,
    #               L2gradient=False)

    img = cv2.adaptiveThreshold(img, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 23, 10)

    img = cv2.GaussianBlur(img, (5, 5), 0)

    # element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3), (1, 1))
    # edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, element)

    retval, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU )

    return img


def find_contours(img):
    """
    Поиск и отбор контуров на бинаризованном изображении.

    Вход: Бинаризованное изображение
    Выход: Бинаризованное изображение, Массив контуров
    """
    contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    squares=[]
    for cnt in contours:
        length = cv2.arcLength(cnt, closed=True)
        cnt = cv2.approxPolyDP(cnt, 0.02*length, True)
        area = cv2.contourArea(cnt)

        # C  compactness ( area and length ratio)
        if area > 60:
            squares.append(cnt)
            # bound_rect = cv2.boundingRect(cnt)
            # (w, h) = bound_rect[2:]

    return img, squares

def apply_denoise(img, zero_img):
    """
    Поиск контуров по определенным критериям и отрисовка их на пустом изображении.

    Вход: Бинаризованное изображение, Пустое изображение
    Вызох: Изображение с отрисованными контурами
    """
    (contours, hierarchy) =  cv2.findContours(img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE )

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i]) 
        length = cv2.arcLength(contours[i], closed=True) 

        if area > 40 and area < 400:
            cv2.drawContours( zero_img, contours, i, (255, 255, 255), -1, 8, hierarchy, 0, None )

    return zero_img

if __name__ == '__main__':
    opts = parse_input()

    img = cv2.imread(opts.path_to_image)

    gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    zero_img = np.zeros(img.shape, dtype=img.dtype)

    img = apply_filters(gray_scale_img)
    render(img)


    
    img, contoures = find_contours(img)

   
    cv2.drawContours(zero_img, contoures, -1,
                    (255, 255, 255),
                    -1) 
    render(img)


 
    zero_img = apply_denoise(img, zero_img)
    render(zero_img)



