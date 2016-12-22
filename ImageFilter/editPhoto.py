import os
from imghdr import what
from sys import argv
from getopt import getopt
from PIL import Image, ImageDraw, ImageFont, ImageFilter

use_help = '''editPhoto [-h][-g] source'''


def photoGaussianBlur(img, radius=5):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def photoContour(img):
    return img.filter(ImageFilter.CONTOUR)


def photoDetail(img):
    return img.filter(ImageFilter.DETAIL)


def photoEdge_Enhance(img):
    return img.filter(ImageFilter.EDGE_ENHANCE)


def photoEdge_Enhance_More(img):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE)


def photoEmboss(img):
    return img.filter(ImageFilter.EMBOSS)


def photoFind_Edges(img):
    return img.filter(ImageFilter.FIND_EDGES)


def photoSmooth(img):
    return img.filter(ImageFilter.SMOOTH)


def photoSmooth_More(img):
    return img.filter(ImageFilter.SMOOTH_MORE)


def photoSharpen(img):
    return img.filter(ImageFilter.SHARPEN)


def photoUnsharpMask(img):
    return img.filter(ImageFilter.UnsharpMask())


def isImg(file_name):
    try:
        if what(file_name) is None:
            return False
        else:
            return True
    except IOError:
        return False


def editPhoto(method, img_name, path=os.curdir, *args):
    in_file = os.path.splitext(img_name)
    img = Image.open(img_name).convert('RGBA')
    out = method(img, *args)
    save_file = os.path.join(path, 'edit_%s.jpg' % in_file[0])
    out.save(save_file, 'jpeg')


def main(argv):
    if len(argv) == 1:
        print(use_help)
        exit(0)
    hasdir = False
    method = photoGaussianBlur
    opts, args = getopt(argv[1:], "hgcdeimfstvu", ["help"])
    for o, a in opts:
        if o == '-h' or o == '--help':
            print(use_help)
        elif o == '-g':
            method = photoGaussianBlur
        elif o == '-c':
            method = photoContour
        elif o == '-d':
            method = photoDetail
        elif o == '-e':
            method = photoEdge_Enhance
        elif o == '-i':
            method = photoEdge_Enhance_More
        elif o == '-m':
            method = photoEmboss
        elif o == '-f':
            method = photoFind_Edges
        elif o == '-s':
            method = photoSmooth
        elif o == '-t':
            method = photoSmooth_More
        elif o == '-v':
            method = photoSharpen
        elif o == '-u':
            method = photoUnsharpMask

    file_name = args[0]
    args = args[1:]
    if os.path.isdir(file_name):
        os.chdir(file_name)
        if not os.path.exists('edit'):
            os.mkdir('edit')
        files = [x for x in os.listdir('.') if isImg(x)]
        for img_name in files:
            editPhoto(method, img_name, path='edit')
    else:
        editPhoto(method, file_name)


if __name__ == '__main__':
    main(argv)
