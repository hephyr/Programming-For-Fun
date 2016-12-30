#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import shutil
from sys import argv
from getopt import getopt
from imghdr import what
try:
    from future.builtins import input
except ImportError:
    pass


usage = 'usage: rm [-f|-i] [-r] file ...'
Trash = os.path.expanduser('~/.Trash')


def isImg(file_name):
    try:
        if what(file_name) is None:
            return False
        else:
            return True
    except IOError:
        return False


def fileExists(args):
    for f in args:
        if not os.path.exists(f):
            return False
    return True


def deleteFile(f, trash_dir=''):
    trash_dir = os.path.join(Trash, trash_dir)
    try:
        shutil.move(f, trash_dir)
    except IOError:
        path, name = os.path.split(f)
        os.makedirs(os.path.join(trash_dir, path))
        shutil.move(f, trash_dir)
    except shutil.Error:
        now = time.strftime("%Y%m%d-%H:%M:%S", time.localtime())
        fn = os.path.split(f)[-1]
        fn, ext = os.path.splitext(fn)
        filename = '%s-%s%s' % (fn, now, ext)
        shutil.move(f, os.path.join(trash_dir, filename))


def removeFiles(recursion, force, cat, files):
    if not recursion:
        for f in files:
            if os.path.isdir(f) and os.listdir(f):
                print('rm: %s: Is a directory' % f)
                exit(1)
    for f in files[:]:
        abspath = os.path.abspath(f)
        if abspath.find(Trash) == 0:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
            files.remove(f)
    if cat:
        deepFirstSearch(files)
    else:
        for f in files:
            deleteFile(f)


def deepFirstSearch(files):
    while files:
        f = files.pop()
        if os.path.isdir(f) and os.listdir(f):
            examine = input('examine files in directory %s?' % f)
            if examine == 'y' or examine == 'Y':
                dir_files = [os.path.join(f, x) for x in os.listdir(f)]
                deepFirstSearch(dir_files)
                if not os.listdir(f):
                    re = input('remove %s?' % f)
                    if re == 'y' or re == 'Y':
                        os.removedirs(f)
        else:
            if isImg(f) and os.path.exists('/usr/local/bin/imgcat'):
                os.system('imgcat %s' % f)
            re = input('remove %s?' % f)
            if re == 'y' or re == 'Y':
                deleteFile(f)


def main():
    recursion = False
    force = True
    cat = False
    opts, args = getopt(argv[1:], "rfih", ["help"])
    if len(argv) == 1 or len(args) == 0 or not fileExists(args):
        print(usage)
        exit(1)
    if not os.path.exists(Trash):
        os.mkdir(Trash)
    for o, a in opts:
        if o == '-r':
            recursion = True
        # if o == '-f':
        #     force = True
        if o == '-i':
            cat = True
            force = False
        if o == '-h' or o == '--help':
            print(usage)
    removeFiles(recursion, force, cat, args)

if __name__ == '__main__':
    main()
