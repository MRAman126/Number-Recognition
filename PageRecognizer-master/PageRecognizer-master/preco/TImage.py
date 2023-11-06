
import cv2


class TImage(object):
    window_height = 800.0

    def __init__(self, path_to_img):
        super(TImage, self).__init__()
        #print path_to_img

    
        #img = cv2.imread(path_to_img, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        img = cv2.imread(path_to_img)

        """try:
            if not img.all():
                raise IOError("No image data \n")
        except AttributeError:
            raise IOError("No image data \n")"""

        self.ref_img = img

        self.img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY );
        self.channels = lambda: 1 if len(self.img.shape) == 2 else self.img.shape[2]

    def render(self, window_name="main", img = None):
        if img == None:
            img = self.img
        scale = self.window_height / img.shape[0]

        cv2.destroyAllWindows()
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC))
        cv2.waitKey(0)