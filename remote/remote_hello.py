#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2018/8/23 17:42
# Version: 0.1
# __author__: Jie Cheng D <jie.d.cheng@outlook.com>

import argparse
import socket
import time
import re

parser = argparse.ArgumentParser(description="This is a TSP CPU load monitoring script.")
parser.add_argument('-s','--server', default='10.168.21.99', help="TSP server address which you are going to monitor.default server is 10.168.21.99")
parser.add_argument('-c','--count',default=3, type=int, help="the times you want to check. type int. default counter is 3")
parser.add_argument('-i','--interval',default=1, type=int, help='the interval time between two checking messages. type int. default interval is 1')
args = parser.parse_args()


fil = re.compile(r'(Proc.*)')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.server, 10000))
result = dict()
for c in range(args.count):
	s.send(b'ekm\n')
	d = s.recv(1024)
	time.sleep(args.interval)
	x = d.decode()
	infoList = re.findall(fil, x)
	result[str(c)] = infoList
	for i in infoList:
		j = i.split(':')
		print(f"{j[0]} traffic load: {j[-1].split(' ')[1]}")
	else:
		print('#'*30)
else:
	bladeNum = len(infoList)
	for y in range(bladeNum):
		n = 0
		for key in result.keys():
			n += int(result.get(key)[y].split(' ')[-2])
		else:
			print(f"{infoList[y].split(':')[0]} averaged traffic load in past {args.count*args.interval}s: {n/args.count:.2f}%\n")
s.close()


