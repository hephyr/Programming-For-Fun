import os
from imghdr import what as isImg
from sys import argv
from getopt import getopt
from PIL import Image, ImageDraw, ImageFont, ImageFilter

use_help = '''PhotoPlusNum [-r for dir][-h --help][-g Gaussian Blur][-p plus num] source'''


def photoPlusNum(img, num=99):
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    myfont = ImageFont.truetype('/Users/Zephyr/Library/Fonts/Sauce Code Powerline Medium.otf', 100)
    draw.text((img.size[0]-150, 0), text=str(num), font=myfont, fill='#e60000')
    out = Image.alpha_composite(img, txt)
    return out


def photoGaussianBlur(img):
    return img.filter(ImageFilter.GaussianBlur(radius=5))


def editPhoto(method, img_name, *args, **kwargs):
    in_file = os.path.splitext(img_name)
    img = Image.open(img_name).convert('RGBA')
    out = method(img, *args, **kwargs)
    out.save('edit_%s.jpeg' % in_file[0], 'jpeg')


def main(argv):
    if len(argv) == 1:
        print(use_help)
        exit(0)
    hasdir = False
    method = photoGaussianBlur
    opts, args = getopt(argv[1:], "hpr:", ["help"])
    for o, a in opts:
        if o == '-h' or o == '--help':
            print(use_help)
        elif o == '-r':
            os.chdir(a)
            hasdir = True
            files = os.listdir('.')
        elif o == '-g':
            method = photoGaussianBlur
        elif o == '-p':
            method = photoPlusNum
    if hasdir:
        for img_name in files:
            editPhoto(method, img_name)
    else:
        editPhoto(method, args[0])



if __name__ == '__main__':
    main(argv)
