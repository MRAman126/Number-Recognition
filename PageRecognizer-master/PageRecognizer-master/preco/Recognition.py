
from misc.ChainUnit import ChainUnit


class Recognition(ChainUnit):

    def handle(self, timage):
        print "Recognition"
        super(Recognition, self).handle(timage)