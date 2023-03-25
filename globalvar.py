# -*- coding:utf-8 -*-
from PySide6.QtCore import QObject, QMutex
import queue 

#================全局变量=================
class globalvar(QObject):
    
    mutex = QMutex()

    record_queue = queue.Queue()    #待处理记录队列
    success_queue = queue.Queue()   #成功记录队列
    fault_queue = queue.Queue()     #失败记录队列

    excel_end = False               #文档保存是否结束
    must_change_ip = False          #是否强制切换IP

    record_count = 0                #读入表格的记录总数
    excel_success_count = 0         #excel成功记录已保存计数器
    excel_fault_count = 0           #excel失败记录已保存计数器

    url = ''                        #初始URL

    def __init__(self):
        super().__init__()



