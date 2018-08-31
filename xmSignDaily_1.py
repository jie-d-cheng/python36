#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/11/14 10:59
# Version: 0.1
# __author__: Jie Cheng D <jie.d.cheng@outlook.com>

import urllib2
import json
import time
import datetime


url = "http://www.miui.com/extra.php?mod=sign/index&op=sign"
user_agent= "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
cookie = "_ga=GA1.2.1317519001.1466046683; MIUI_2132_saltkey=VFG6e1fX; MIUI_2132_lastvisit=1509798549; MIUI_2132_visitedfid=389; UM_distinctid=15f87388b9eb60-0a37fd1791e26f-5e163117-100200-15f87388b9fb1b; __utmt=1; MIUI_2132_ulastactivity=496bX4h%2FKpit9R5uLRHLWXAJXEed7AryRMdtkiqgDpOZYXPniQQU9qU; MIUI_2132_auth=2c91W9AY%2BXdH6xuJiw2W4Mr556USi1%2Bw%2BsWn%2F%2FwJKFIaUA%2FSIINB; lastLoginTime=0618ChhcsUIX3hOS07sp%2FCED7yTJf1yWDYi063L1cSYM0pvXRf2N; MIUI_2132_sendmail=1; MIUI_2132_lastact=1510626399%09forum.php%09newindex; CNZZDATA2441309=cnzz_eid%3D316306679-1509801872-null%26ntime%3D1510621561; CNZZDATA30049650=cnzz_eid%3D707065922-1509801884-null%26ntime%3D1510622687; MIUI_2132_noticeTitle=1; __utma=230417408.1317519001.1466046683.1509802151.1510626341.6; __utmb=230417408.6.10.1510626341; __utmc=230417408; __utmz=230417408.1510626341.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_3c5ef0d4b3098aba138e8ff4e86f1329=1509802151,1510626338; Hm_lpvt_3c5ef0d4b3098aba138e8ff4e86f1329=1510626401"
headers = {"User-Agent": user_agent, "Cookie": cookie}
request = urllib2.Request(url=url,headers=headers)

def xmsign():
    stime = datetime.datetime.now()
    req = urllib2.urlopen(request).read()
    result = json.loads(req)
    return "{} -*- {}\n".format(stime, result.get("message").encode('utf-8'))

n = 0
with open(u"C:\\Users\\ejiecng\\Desktop\\scripts_py\\签名日志.txt","a+") as f:
    while n < 15:
        f.write(xmsign())
        time.sleep(0.03)
        n += 1
    else:
        f.write("{}\n".format("*" * 55))