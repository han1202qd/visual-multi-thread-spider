# -*- coding:utf-8 -*-
from PySide6.QtCore import QObject, Signal, Slot, QEventLoop, QTimer, QThread, QTime
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
import re
import os
import sys
import time

#====================================守护线程类=================================
class spythread(QThread):
    """守护线程类"""
    def __init__(self, parent=None, threads=None, wids=None):
        QThread.__init__(self, parent)
        self.form = parent
        self.spy = spywork(self,threads,wids)
        self.threads = threads

    def run(self):
        self.spy.spy()
        self.exec_()

    @Slot(list)
    def updatestatus(self,tlist):                   #监测线程、工作线程状态显示
        wtime = re.findall(r'\d+', tlist[1])
        if tlist[0] == 'spythread':                 #更新监测线程
            self.form.ui.label_8.setText('工作线程结束，用时[%dDay %d:%02d:%02d]'%(int(wtime[0]),int(wtime[1]),int(wtime[2]),int(wtime[3])))
            self.form.st.quit()
            self.form.st.wait()
            self.form.ui.label_8.setText('工作线程销毁，用时[%dDay %d:%02d:%02d]'%(int(wtime[0]),int(wtime[1]),int(wtime[2]),int(wtime[3])))
        else:
            self.updtable(tlist)                    #更新工作线程
        self.form.ui.label_8.setText('运行中，用时[%dDay %d:%02d:%02d]'%(int(wtime[0]),int(wtime[1]),int(wtime[2]),int(wtime[3])))
        self.form.ui.label_6.setText(str(self.form.ui.tableWidget.rowCount()))

    def updtable(self,clist):
        curtable = self.form.ui.tableWidget
        irows = curtable.rowCount()
        isfind = False
        if irows == 0:
            curtable.insertRow(irows)
            curtable.setItem(irows,0,QTableWidgetItem(str(clist[0])))
            curtable.setItem(irows,1,QTableWidgetItem(str(clist[1])))
        else:
            for irow in range(irows):
                curtext = curtable.item(irow,0).text()
                if curtext == str(clist[0]):
                    isfind = True
                    curtable.setItem(irow,1,QTableWidgetItem(str(clist[1])))
                    break
            if not isfind:
                curtable.insertRow(irows)
                curtable.setItem(irows,0,QTableWidgetItem(str(clist[0])))
                curtable.setItem(irows,1,QTableWidgetItem(str(clist[1])))

        #for irow in range(curtable.rowCount()):
        #    curtext = curtable.item(irow,0).text()
        #    if self.threads.get(curtext) is None:
        #        curtable.removeRow(irow)


#====================================守护工作类================================
class spywork(QObject):
    """守护工作类"""
    spysign = Signal(list)
    def __init__(self, parent=None,threads=None,wids=None):
        super(self.__class__, self).__init__(parent)
        self.spysign.connect(parent.updatestatus)
        self.threads = threads
        self.wids = wids

    def spy(self):
        self.time_s = time.time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.querystatus)
        self.timer.start(1000)

    def querystatus(self):
        time_c = time.time()
        ftime = time_c - self.time_s
        visual_time = self.time_convert(ftime)
        if self.threads:
            for key in list(self.threads.keys()):                 #字典删除项必须用列表化
                if self.threads[key].isRunning():
                    self.spysign.emit([key,'运行中，[%s]'%visual_time])
                if self.threads[key].isFinished():
                    self.spysign.emit([key,'结束,用时[%s]'%visual_time])
                    self.threads[key].quit()
                    self.threads[key].wait()
                    if re.search('thread',key): self.destroytab(key)
                    self.spysign.emit([key,'销毁,用时[%s]'%visual_time])
                    del self.threads[key]
        else:
            self.spysign.emit(['spythread','用时[%s]'%visual_time])

    def time_convert(self,time):
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        return "%dDay %d:%02d:%02d" % (d, h, m, s)

    def destroytab(self,tname):
        num = ''.join(re.findall(r'\d+', tname))
        tabname = u'tab' + num
        textname = u'text' + num
        linename = u'line' + num
        labelname = u'lab' + num
        listname = u'list' + num
        self.wids[tabname].deleteLater()
        del self.wids[tabname]
        del self.wids[textname]
        del self.wids[linename]
        del self.wids[labelname]
        del self.wids[listname]
        





