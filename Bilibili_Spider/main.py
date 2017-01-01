#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import mysql.connector
from json import loads
from os import getenv
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup



def getTitle(av):
    url = 'http://www.bilibili.com/video/av%s/' % av
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        div_title = soup.find('div', {'class': 'v-title'})
        title = div_title.h1.text
        return title, True
    except BaseException:
        return str(soup.title), False


def getStat(av):
    url = 'http://api.bilibili.com/archive_stat/stat?aid=%s' % av
    r = requests.get(url)
    stat = loads(r.text)
    return stat['data']


def spider(av):
    conn = mysql.connector.connect(user='root',
                                   password=getenv('mysql_pass'),
                                   database='Bilibili')
    title, isvideo = getTitle(av)
    if isvideo:
        stat = getStat(av)
        cursor = conn.cursor(buffered=True)
        sql = 'INSERT INTO Video_Rank (num, name, reply, coin, favorite, his_rank, share, now_rank, danmaku, view) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (av, title, stat['reply'], stat['coin'], stat['favorite'], stat['his_rank'], stat['share'], stat['now_rank'], stat['danmaku'], stat['view']))
        print(av)
        conn.commit()
        cursor.close()
    else:
        print(title)


def getStart():
    conn = mysql.connector.connect(user='root',
                                   password=getenv('mysql_pass'),
                                   database='Bilibili')
    cursor = conn.cursor(buffered=True)
    sql = 'SELECT num from Video_Rank ORDER BY num DESC LIMIT 1'
    cursor.execute(sql)
    high = cursor.fetchall()
    cursor.close()
    if high:
        return int(high[0][0]) + 1
    else:
        return 11

def main():
    begin = getStart()
    #p = Pool(4)
    #p.map(spider, range(begin, 7000))
    #p.close()
    #p.join()
    for i in range(begin, 7000):
        spider(i)

if __name__=='__main__':
    main()
