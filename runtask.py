import re
import os
import time
import sys
from PySide6.QtCore import QObject, Signal, Slot, QThread, QTimer, QMutex, QMutexLocker
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from globalvar import globalvar

#====================================执行任务线程类=================================
class taskthread(QThread):
    """执行任务线程类"""
    def __init__(self, parent=None, tasks=None, threads=None):
        QThread.__init__(self, parent)
        self.form = parent
        self.taskw = taskwork(self,tasks,threads)
        self.tasks = tasks


    def run(self):
        self.taskw.start_work()
        self.exec_()

    @Slot(str)
    def updtext(self,ustr):                     #主线程窗口的信息新增（线程名、未分配、总分配）
        if ustr != 'upd':return
        curtable = self.form.ui.tableWidget_5       #tableWidget_5为任务显示表格
        irows = curtable.rowCount()
        sn,fn = 0, 0
        for task_key in self.tasks:
            isfind = False
            sn += self.tasks[task_key][0]
            fn += self.tasks[task_key][1]
            if irows == 0:
                curtable.insertRow(irows)
                curtable.setItem(irows,0,QTableWidgetItem(str(task_key)))
                curtable.setItem(irows,1,QTableWidgetItem(str(self.tasks[task_key][0])))
                curtable.setItem(irows,2,QTableWidgetItem(str(self.tasks[task_key][1])))
                curtable.setItem(irows,3,QTableWidgetItem(str(self.tasks[task_key][2])))

            else:
                for irow in range(irows):
                    curtext = curtable.item(irow,0).text()
                    if curtext == str(task_key):
                        isfind = True
                        curtable.setItem(irow,1,QTableWidgetItem(str(self.tasks[task_key][0])))
                        curtable.setItem(irow,2,QTableWidgetItem(str(self.tasks[task_key][1])))
                        curtable.setItem(irow,3,QTableWidgetItem(str(self.tasks[task_key][2])))
                        break
                if not isfind:
                    curtable.insertRow(irows)
                    curtable.setItem(irows,0,QTableWidgetItem(str(task_key)))
                    curtable.setItem(irows,1,QTableWidgetItem(str(self.tasks[task_key][0])))
                    curtable.setItem(irows,2,QTableWidgetItem(str(self.tasks[task_key][1])))
                    curtable.setItem(irows,3,QTableWidgetItem(str(self.tasks[task_key][2])))

        #for drow in range(curtable.rowCount()):            #如果任务字典中不存在此线程，则从表格删除，暂时考虑不需要删除，因为最后要看状态
        #    droptext = curtable.item(drow,0).text()
        #    if self.tasks.get(droptext) is None:
        #        curtable.removeRow(drow)
        self.form.ui.label_13.setText(str(sn))
        self.form.ui.label_15.setText(str(fn))
        self.form.ui.label_25.setText(str(globalvar.record_count))
        self.form.ui.label_26.setText(str(globalvar.record_queue.qsize()))
        self.form.ui.label_30.setText(str(globalvar.excel_success_count - 1))       #减去EXCEL标题行
        self.form.ui.label_32.setText(str(globalvar.excel_fault_count - 1))         #减去EXCEL标题行
        self.form.ui.label_35.setText(str(globalvar.success_queue.qsize()))
        self.form.ui.label_37.setText(str(globalvar.fault_queue.qsize()))

#====================================执行任务工作类=================================
class taskwork(QObject):
    """执行任务工作类"""

    tasksign = Signal(str)

    def __init__(self, parent=None, tasks=None, threads=None):
        super(self.__class__, self).__init__(parent)
        self.tasks = tasks
        self.threads = threads
        self.tasksign.connect(parent.updtext)

    def start_work(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_task)
        self.timer.start(2000)


    def get_task(self):                             #从tablewidget_3获取并分配任务给tasks字典
        for key in list(self.threads.keys()):
            if re.search(r'thread\d+',key):
                if self.tasks.get(key) is None:
                    self.tasks[key] = [0,0,0]           #[成功数，失败数，总数]
        if len(self.tasks) == 0 : return
        self.printstr('upd')
            
    def printstr(self,ustr):
        self.tasksign.emit(ustr)





