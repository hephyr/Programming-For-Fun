#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from imghdr import what
from sys import argv
from getopt import getopt
from PIL import Image, ImageFont, ImageFilter

use_help = '''getwallpaper [-h] source'''


def blur(filename, path=os.curdir, out_width=2560, out_hight=1440, *args):
    img = Image.open(filename).convert('RGBA')
    width, hight = img.size
    if float(width)/hight > 16.0/9:
        w = hight * 16.0/9
        out = img.crop((width/2 - w/2, 0, width/2 + w/2, hight))
    else:
        h = width * 9.0/16
        out = img.crop((0, hight/2 - h/2, width, hight/2 + h/2))
    out = out.resize((out_width, out_hight))
    out = out.filter(ImageFilter.GaussianBlur(radius=66))
    out.paste(img, (out_width/2 - width/2, out_hight/2 - hight/2))
    out_name = os.path.join(path, os.path.splitext(filename)[0]+'_BLUR.jpg')
    out.save(out_name, 'jpeg')


def main(argv):
    if len(argv) == 1:
        print(use_help)
        exit(0)
    opts, args = getopt(argv[1:], 'hw', [])
    width = 2560
    hight = 1440
    for o, a in opts:
        if o == '-h':
            hight = a
        if o == '-w':
            width = a
    for file_name in args:
        if os.path.isdir(file_name):
            os.chdir(file_name)
            if not os.path.exists('edit'):
                os.mkdir('edit')
            files = [x for x in os.listdir('.') if isImg(x)]
            for img_name in files:
                blur(file_name, out_width=width, out_hight=hight, path='edit')
            os.chdir('..')
        else:
            blur(file_name, out_width=width, out_hight=hight)
        

if __name__ == '__main__':
    main(argv)
