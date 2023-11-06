
class ChainUnit(object):
    __next = None

    def add(self, next):
        self.__next = next
        return next

    def handle(self, img):
        if self.__next:
            self.__next.handle(img)