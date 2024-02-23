

import os.path
import optparse

from preco.Preprocessing import Preprocessing
from preco.Extraction import Extraction
from preco.Recognition import Recognition
from preco.TImage import TImage
from preco.misc.ChainUnit import ChainUnit


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


if __name__ == '__main__':
    opts = parse_input()

    timage = TImage(opts.path_to_image)

    chain = ChainUnit()
    chain \
        .add(Preprocessing()) \
        .add(Extraction()) \
        .add(Recognition() \
    )
    chain.handle(timage)
