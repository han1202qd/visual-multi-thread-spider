# -*- coding:utf-8 -*-
import requests
import random
import time
import os
import re
import types
import threading
from bs4 import BeautifulSoup
from lxml import etree
from PySide6.QtCore import QObject, Signal, Slot, QEventLoop, QThread
from PySide6.QtWidgets import QTableWidgetItem
from globalvar import globalvar

#====================================代理线程类=================================
class ProxyThread(QThread):
    """代理线程类"""
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.agent = Get_Proxy(self)
        self.form = parent.ui
        self.table = parent.ui.tableWidget_4
        self.cols = self.table.columnCount()
        self.rows = self.table.rowCount()
        self.irow = 0
        self.icol = 0


    def run(self):
        self.agent.get_proxy()
        #self.exec_()

    @Slot(str)
    def upd_proxy_result(self,text):                                    #更新IP获取状态文本框textEdit_3
        if re.search('开始获取代理',text):
            self.form.textEdit_3.clear()
            self.table.clear
        self.form.textEdit_3.append(text)

    @Slot(str)
    def upd_ip_table(self,text):                                        #更新IP表tableWidget_4
        if self.irow == 0 and self.rows == 0 : 
            self.table.insertRow(self.irow)
            self.rows += 1
        self.table.setItem(self.irow,self.icol,QTableWidgetItem(text))
        self.icol += 1
        if self.icol == self.cols : 
            self.irow += 1
            self.icol = 0
            self.table.insertRow(self.irow)



#====================================代理工作类================================= 
class Get_Proxy(QObject):
    """代理工作类"""
    
    proxy_text = Signal(str)
    ip_sign = Signal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',}
        self.timeout = 6
        self.proxy_text.connect(parent.upd_proxy_result)
        self.ip_sign.connect(parent.upd_ip_table)

    def get_proxy(self):                            #解析网页，并得到网页中的代理IP
        while not globalvar.ip_end:
            try:
                if not globalvar.ip_get_sign : 
                    QThread.sleep(1)
                    continue
                proxy_link = "http://192.168.16.228:5010/get_all/"
                self.printstr('开始获取代理[%s]'%proxy_link)
                req = requests.get(proxy_link, headers=self.header, timeout=self.timeout)
                if req:
                    for child in req.json():
                        proxy = child.get("proxy")  
                        globalvar.ip_queue.put(proxy)
                        globalvar.ip_count += 1                 #计数器
                        self.printip(proxy)
                self.printstr('已获取[%d]个代理IP'%globalvar.ip_count)
                globalvar.ip_get_sign = False
            except Exception as e:
                self.printstr(repr(e))

    def printstr(self,text):
        self.proxy_text.emit(text)

    def printip(self,text):
        self.ip_sign.emit(text)

 

