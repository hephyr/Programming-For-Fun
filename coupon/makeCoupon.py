#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from os import getenv
from sys import argv
from random import choice
from string import digits, ascii_uppercase as uppercase

import mysql.connector
from getopt import getopt


def makeCoupon(place=5):
    chars = uppercase + digits
    s = ''
    for i in range(place):
        s += choice(chars)
    return s


def printThose(count, place):
    result = []
    while count > 0:
        s = makeCoupon(place)
        if s not in result:
            result.append(s)
            count -= 1
    for i in result:
        print(i)


def mysqlThose(count, place):
    conn = mysql.connector.connect(user='root',
                                   password=getenv('mysql_pass'),
                                   database='Coupon')
    cursor = conn.cursor(buffered=True)
    while count > 0:
        s = makeCoupon(place)
        sql = 'SELECT Coupon FROM Coupon WHERE Coupon = %s'
        cursor.execute(sql, (s,))
        if cursor.fetchall == []:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = 'INSERT INTO Coupon (coupon, datetime) values (%s, %s)'
            cursor.execute(sql, (s, now))
            count -= 1
    conn.commit()
    cursor.close()


def main():
    place = 5
    count = 20
    method = printThose
    opts, args = getopt(argv[1:], "hp:c:", ["help", "mysql"])
    for o, a in opts:
        if o == '-p':
            place = int(a)
        elif o == '-c':
            count = int(a)
        elif o == '--mysql':
            method = mysqlThose
        elif o == '-h' or o == '--help':
            print('[-p][-c]')
            exit(0)
    method(count, place)

if __name__ == '__main__':
    main()
