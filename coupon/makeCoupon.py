#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from random import randint
from string import uppercase, digits
from getopt import getopt


def makeCoupon(place=5):
    chars = uppercase + digits
    s = ''
    for i in range(place):
        s += chars[randint(0, len(chars)-1)]
    return s


def main():
    place = 5
    count = 200
    result = []
    opts, args = getopt(argv[1:], "hp:c:", ["help"])
    for o, a in opts:
        if o == '-p':
            place = int(a)
        elif o == '-c':
            count = int(a)
        elif o == '-h' or o == '--help':
            print '[-p][-c]'
            exit(0)
    while count > 0:
        s = makeCoupon(place)
        if s not in result:
            result.append(s)
            count -= 1
    for i in result:
        print i


if __name__ == '__main__':
    main()
