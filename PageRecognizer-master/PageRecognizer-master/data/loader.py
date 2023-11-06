#!/usr/bin/python
#
# Store info about images data (name, hash) in MongoDB.
# Requirements:
# 1. pymongo
# 2. pillow

import os
import os.path
import optparse

from pymongo import MongoClient
from PIL import Image
from md5 import md5


def parse_input():
    usage = "usage: %prog [options] arg1"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--image", 
                    dest="path_to_image",
                    help="Path to image.",
                    metavar="path_to_image")
    parser.add_option("-d", "--dir", 
                    dest="path_to_images_dir",
                    help="Path to dir with images.", 
                    metavar="path_to_images_dir")

    (opts, args) = parser.parse_args()

    if (opts.path_to_images_dir is None) and (opts.path_to_image is None):
        parser.print_help()
        exit(-1)

    if opts.path_to_image:
        if not os.path.exists(opts.path_to_image):
            parser.error('image does not exists')

    if opts.path_to_images_dir:
        if not os.path.exists(opts.path_to_images_dir):
            parser.error('dir does not exists')

    return opts


def save_to_db(im_obj, cursor):
    if cursor.insert(im_obj):
        print "info: %s saved to db." % im_obj["filename"]
    else:
        print "error: can not save %s to db" % im_obj["filename"]


def save_to_fs(im, im_obj, imgs_storage="./imgs/"):

    if not os.path.exists(imgs_storage):
        os.makedirs(imgs_storage)

    if not os.path.isfile(imgs_storage + im_obj["img_md5"]):
        im.save(imgs_storage + im_obj["img_md5"], im_obj["format"])
        print "info: %s saved to fs." % im_obj["filename"]
    else:
        print "warning: %s already saved to fs." % im_obj["filename"]


def save_image(img_path, cursor):
    im = Image.open(img_path)

    im_obj = {
        "filename": im.filename.split('/')[-1],
        "img_md5": md5(im.tostring()).hexdigest(),
        "format": im.format,
        "size": im.size,
        "mode": im.mode,
    }

    if not cursor.find({"img_md5": im_obj["img_md5"]}).count():
        save_to_db(im_obj, cursor)
        save_to_fs(im, im_obj)
    else:
        print "warning: %s already exists." % im_obj["filename"]
        save_to_fs(im, im_obj)


def save_dir_of_images(dir_path, cursor):

    list_of_files = os.listdir(dir_path)

    for im_filename in list_of_files:
        img_path = dir_path + "/" + im_filename
        save_image(img_path, cursor)


if __name__ == '__main__':
    opts = parse_input()

    cursor = MongoClient('localhost', 27017).imageDB.images

    if opts.path_to_images_dir:
        save_dir_of_images(opts.path_to_images_dir, cursor)
    else:
        save_image(opts.path_to_image, cursor)

