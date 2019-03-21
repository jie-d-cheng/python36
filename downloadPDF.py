#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
@author: Jie Cheng 
@contact: jie.d.cheng@outlook.com
@file: downloadPDF.py
@time: 2019/03/13
@version: 0.2
"""

import requests
import json
import time
import re
import os

class DownlaodAll:
    def __init__(self, comoanyID):
        self.url = "http://www.neeq.com.cn/disclosureInfoController/infoResult.d" \
"o?callback=jQuery18308204703489144538_1552308087676"
        self.companyID = comoanyID
        self.url_pf = 'http://www.neeq.com.cn'
        if not os.path.exists('tmp'):
            os.makedirs('tmp')

    def postData(self, page=0):
        self.post_data = {"disclosureType": 5,
             "page": page,
             "companyCd": self.companyID,
             "isNewThree": 1,
             "startTime": "",
             "endTime": "",
             "keyword": "关键字",
             "xxfcbj": ""}


    def getInfo(self):
        self.postData()
        response = requests.post(self.url, data=self.post_data)
        notifications = re.findall(r'{.*}', response.text)
        info_dict = json.loads(notifications[0])
        self.totalElements = info_dict['listInfo']['totalElements']
        self.totalPages = info_dict['listInfo']['totalPages']

    def startDownload(self):
        self.getInfo()
        print(f'搜索到{self.totalElements}个文件，共{self.totalPages}页，准备开始下载...')

        for i in range(self.totalPages):
            self.postData(page=i)
            response = requests.post(self.url, data=self.post_data)
            notifications = re.findall(r'{.*}', response.text)
            info_dict = json.loads(notifications[0])
            info_download = info_dict['listInfo']['content']
            for j,k in enumerate(info_download):
                current = k
                filename = f'{current["publishDate"]}__{current["disclosureTitle"].replace(":", "__")}.pdf'
                pdf = requests.get(f'{self.url_pf}{current["destFilePath"]}')
                with open(f'./tmp/{filename}', 'wb') as f:
                    f.write(pdf.content)
                print(f'第{i+1}页第{j+1}个文件下载完成!!!')
                time.sleep(2)
        else:
            input('所有文件下载完成，按任意键退出。')


if __name__ == '__main__':
    comID = input('请输入公司代码：')
    downloadIt=DownlaodAll(comID)
    downloadIt.startDownload()
