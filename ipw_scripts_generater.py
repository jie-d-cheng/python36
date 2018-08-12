#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2018/3/21 14:47
# Version: 0.1
# __author__: Jie Cheng D <jie.d.cheng@outlook.com>

import xlrd
import time

fileName = input("Please input your excel name:")

try:
    workbook = xlrd.open_workbook(fileName)
    sheetName = input("Please input your sheet name:")
except FileNotFoundError:
    print("File not found...")
    time.sleep(10)
    exit(0)

while sheetName not in workbook.sheet_names():
    sheetName = input("Sheet doesn't exist, try a another one:")
else:
    sheet2 = workbook.sheet_by_name(sheetName)

with open('script_{}.txt'.format(sheetName),'w') as f:
    for i in range(sheet2.nrows):
        record = sheet2.row_values(i)
        if record[0][0:4] == '_sip':
            f.write('create srvrecord {} -set container={};priority={};weight={};port={};target={}\n'.format(record[0],record[1],int(record[2]),int(record[3]),int(record[4]),record[5]))
        if record[4] == 's':
            f.write(
                'create naptrrecord {} -set container={};order={};preference={};flags="s";service="{}";regexp="";replacement={}\n'.format(
                    record[0], record[1], int(record[2]), int(record[3]), record[5], record[7])
                    )
        if str(record[2])[0:5] == '2001:':
            f.write('create aaaarecord {} -set container={};address={}\n'.format(record[0],record[1],record[2]))
    else:
        print("Script generated, please check it...")
        time.sleep(5)
        exit(0)




