# -*- coding:utf-8 -*-
import requests
import re
import os
import time
import random
import sys
import pdfkit

#分割线内为ebook_convert所需
import queue                
import threading
import subprocess
# ----------------------

from urllib.parse import urlparse
from pathlib import Path
from contextlib import closing
from bs4 import BeautifulSoup
from lxml import etree
from PySide6.QtCore import Qt, QObject, Signal, Slot, QEventLoop, QTimer, QThread, QMutex, QMutexLocker
from PySide6.QtWidgets import QTextEdit, QProgressBar, QLabel, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
from PySide6.QtGui import QColor
from globalvar import globalvar

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By


#====================================下载线程类=================================
class WorkerThread(QThread):
    """下载线程类"""
    def __init__(self, parent=None, tasks=None):
        QThread.__init__(self, parent)
        self.form = parent
        self.down = download(self,tasks)
    def run(self):
        self.down.url_router()
        #self.exec_()

    @Slot(list)
    def getsign(self,tlist):            #子线程Tab窗口下载textedit内容更新
        numlist = re.findall(r'\d+', tlist[0])
        num = int(numlist[0])
        curtextname = 'text' + str(num)
        curtext = self.form.findChild(QTextEdit,curtextname)
        if re.search('当前位于线程',tlist[1]):
            curtext.clear()
        curtext.append(tlist[1])

    @Slot(list)
    def getlistsign(self,plist):        #子线程Tab窗口label progressbar状态更新，
        numlist = re.findall(r'\d+', plist[0])
        num = int(numlist[0])
        curlabname = 'lab' + str(num)
        curprogname = 'prog' + str(num)

        curlab = self.form.findChild(QLabel,curlabname)
        curprog = self.form.findChild(QProgressBar,curprogname)

        if re.search('下载完成',str(plist[4])):
            curlab.setText("[%s],已下载[%d]K,共[%d]K,%s"%(str(plist[1]),int(plist[2]),int(plist[3]),str(plist[4])))
        else:
            curlab.setText("正在下载[%s],已下载[%d]K,共[%d]K,下载速度[%s]K/S"%(str(plist[1]),int(plist[2]),int(plist[3]),str(plist[4])))
        curprog.setMaximum(int(plist[3]))
        curprog.setValue(int(plist[2]))

    @Slot(list)
    def upddownlist(self,dlist):        #子线程窗口list列表填充
        numlist = re.findall(r'\d+', dlist[0])
        num = int(numlist[0])   
        listname = 'list' + str(num)
        listwin = self.form.findChild(QListWidget,listname)
        listwin.addItem(dlist[1])

    @Slot(list)
    def updCurRow(self,clist):          #子线程窗口list列表添加及颜色更新
        numlist = re.findall(r'\d+', clist[0])
        num = int(numlist[0])   
        listname = 'list' + str(num)
        listwin = self.form.findChild(QListWidget,listname)
        items = listwin.findItems(clist[2], Qt.MatchExactly)
        if items:
            item = items[0]
            if clist[1] == 'rein' : 
                listwin.takeItem(listwin.row(item))             #如果重进队列，则在列表中删除
            else:
                if clist[1] == 'begin' : item.setBackground(QColor('blue'))
                if clist[1] == 'success' : item.setBackground(QColor('green'))
                if clist[1] == 'fault' : item.setBackground(QColor('red'))
                item.setForeground(QColor('white'))
                listwin.visualItemRect(item)

    @Slot(list)
    def updRecList(self,ilist):         #接受子线程成功失败记录ID，并更新页面分析窗口的记录列表状态
        table = self.form.ui.tableWidget_3
        row = int(ilist[2]) - 1            #此处确定接受回来的key值就是表的行值(因为表格行是从0开始，key是从1开始，所以要-1)
        cols = table.columnCount()
        for col in range(cols):
            try:
                if ilist[1] == 'success':
                    if col == 8 : table.setItem(row,col,QTableWidgetItem(ilist[3]))
                    table.item(row,col).setBackground(QColor('green'))
                if ilist[1] == 'fault':
                    if col == 8 : table.setItem(row,col,QTableWidgetItem(self.getTextEditMsg(ilist[0])))
                    table.item(row,col).setBackground(QColor('red'))
                if ilist[1] == 'rein':
                    table.item(row,col).setBackground(QColor('black'))
                table.item(row,col).setForeground(QColor('white'))
            except:
                continue

    def getTextEditMsg(self,threadname):
        numlist = re.findall(r'\d+', threadname)
        num = int(numlist[0])
        textname = 'text' + str(num)
        curtext = self.form.findChild(QTextEdit,textname)
        return curtext.toPlainText()


#====================================下载工作类=================================
class download(QObject):
    """下载工作类"""
    newText = Signal(list)          #更新子线程窗口textedit
    newList = Signal(list)          #更新子线程窗口label progressbar
    CurRowSign = Signal(list)       #子线程窗口list列表下载状态颜色更新
    RecIdSign = Signal(list)        #子线程成功、失败记录ID发送
    downlist = Signal(list)         #子线程窗口list列表添加
    IpSign = Signal(list)            #已使用代理信号
    def __init__(self, parent=None, tasks=None):
        super(self.__class__, self).__init__(parent)
        self.__head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',}
        self.encoding = 'utf-8'                                 #默认获取内容的编码
        self.__htmpath = r"D:\GitHub\pyside\pdf_spider\htm"
        self.__otherpath = r"D:\GitHub\pyside\pdf_spider\other"
        self.__pdfpath = r"D:\GitHub\pyside\pdf_spider\pdf"
        #self.__web_url = "https://www.ebooksgratuits.com/html/"
        self.__web_url = 'https://www.gutenberg.org'
        self.domain = "www.ebooksgratuits.com"
        self.__timeout = 10
        self.__maxtries = 10
        self.tasks = tasks
        self.newText.connect(parent.getsign)
        self.newList.connect(parent.getlistsign)
        #self.listcount.connect(parent.upd_taskstatus)
        self.downlist.connect(parent.upddownlist)
        self.CurRowSign.connect(parent.updCurRow)
        self.RecIdSign.connect(parent.updRecList)
        self.IpSign.connect(parent.form.upd_iptable_status)
        self.proxy_valid = False                                 #当前代理是否有效
        self.url_reinque = False                                #当前URL是否重进队列

    # 判断格式
    def url_router(self):
        threadname = str(QThread.currentThread().objectName())  
        while not globalvar.doc_end:
            if globalvar.must_change_ip:                                #不使用代理的情况下，手动更换IP
                self.printstr('请手动更换IP')
                QThread.sleep(1)
                continue

            self.printstr("当前位于线程[%s],当前任务启动时间[%s]" %( threadname, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) ))
            try:
                url_info = globalvar.url_queue.get()
            except:
                self.printstr('[URL队列]为空，请等待')                                          #抛出异常则对列为空
                QThread.sleep(1)
                continue
            self.printdownlist( [ '[%s][%s]'%(url_info[1],url_info[7]) ] )

            down_url = url_info[7]
            self.printCurRow(['begin','[%s][%s]'%(url_info[1],down_url)])

            c_url = down_url.split('?')[0]
            fname_list = os.path.basename(c_url).split('.')          #将链接如'https://www.gutenberg.org/ebooks/1.epub.images?session_id=3d3cdb155b95d62628033cc52af36ec48f19ca0b'格式化为列表：['1', 'epub', 'images']
            path = None
            
            ext = fname_list[1]
            if ext in ['htm','html']:                                                               #HTML无需使用代理
                self.proxies = {}
                path = self.get_download_htm(c_url)
            else:                                                                           #下载文件才使用代理  
                if globalvar.use_proxy:
                    self.proxies = self.get_proxy()
                    self.printstr("开始使用代理[%s]" % self.proxies)
                else:
                    self.proxies = {}
                path = self.get_download_other(c_url)
            
            if not os.path.exists(str(path)): path = None

            if path is None:
                if self.url_reinque:                                                #重进队列处理
                    globalvar.url_queue.put(url_info)
                    self.printCurRow(['rein','[%s][%s]'%(url_info[1],down_url)])
                    self.printRecId(['rein',url_info[1],''])
                    self.url_reinque = False
                else:
                    self.printCurRow(['fault','[%s][%s]'%(url_info[1],down_url)])
                    globalvar.fault_queue.put(url_info[1])
                    self.tasks[threadname][1] += 1                      #失败数增加
                    self.printRecId(['fault',url_info[1],'None'])
                    self.tasks[threadname][2] += 1                          #总数增加
            else:
                self.printCurRow(['success','[%s][%s]'%(url_info[1],down_url)])
                globalvar.success_queue.put(url_info[1])
                self.tasks[threadname][0] += 1                      #成功数增加
                self.printRecId(['success',url_info[1],path])
                self.tasks[threadname][2] += 1                          #总数增加
            QThread.sleep(random.randint(30,60))                   #线程随机休眠，一防止被禁，二如果本条记录下载失败，槽函数能够来得及处理相应的textedit中的失败信息

    def get_proxy(self):
        check_url = "https://" + self.domain
        status = False
        if self.proxy_valid and self.proxies != {}:                                        #代理有效，则不需取代理，继续使用即可
            status = True
            proxies = self.proxies
        while not status:
            try:
                proxy = globalvar.ip_queue.get()
            except:
                self.printstr('[代理队列]为空，请等待')         #抛出异常则对列为空
                QThread.sleep(1) 
                continue
            proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
            self.printstr("开始测试代理[%s]" % proxies)
            try:
                r = requests.get(check_url, headers=self.__head, proxies=proxies, timeout=self.__timeout)       # 发送测试请求
                if r.status_code == 200:
                    self.printstr("代理[%s]可用" % proxy)
                    status = True
                    self.proxy_valid = True                         #默认代理有效
                    self.IpSign.emit(['True',proxy])
            except Exception as e:
                self.printstr("代理[%s]不可用，继续测试下一个代理:/t[%s]" %(proxy,repr(e)))
                self.IpSign.emit(['False',proxy])
        return proxies

    # 获取真实HTML地址，获取并写入文件,转为pdf
    def get_download_htm(self,url):
        pdf_path = None
        try:
            self.printstr('准备获取[%s]' %url)
            htm_ob, is_get, true_url = self.down_file( url)
            if is_get:
                fname,ext = os.path.splitext(os.path.basename(true_url))
                file_name = '%s%s'%(fname, ext)
                path = os.path.join(self.__htmpath , file_name)
                up_html = self.get_htm_pic_url( true_url, file_name, htm_ob )
                path = self.write_file( path, up_html )
                pdf_path = self.html_pdf( path )
            else:
                self.printstr('没有获取HTML内容，不进行写文件操作')
        except Exception as e:
            self.printstr('发生错误：\t %s' %repr(e))
        return pdf_path

    # 断点续传中负责获取链接的方法
    def get_file_obj(self, down_link, offset, istream):
        i,webPage,is_get = 0,None,False
        headers = self.__head
        headers['Accept-Encoding'] = None
        headers['Range'] = 'bytes=%d-' % offset
        while (not is_get) and (i < self.__maxtries):
            try:
                webPage = requests.get(down_link, stream=istream, headers=headers, proxies=self.proxies, timeout=self.__timeout)
                status_code = webPage.status_code
                if status_code in [200, 206]:
                    is_get = True
                elif status_code == 416:
                    i += 1
                    self.printstr("第[%d]次：%s文件数据请求区间错误,status_code:%s" % (i, down_link, status_code))
                else:
                    i += 1                    
                    self.printstr("第[%d]次：[%s]链接出错,status_code:%s" % (i, down_link, status_code))
                    time.sleep(5)
            except Exception as e:
                i += 1
                self.printstr("第[%d]次：[%s]链接错误:%s" % (i, down_link, repr(e)))
                time.sleep(5)
            if i == self.__maxtries:
                self.printstr("达到最大重试次数，停止获取.")
        return webPage, is_get

    # 下载文件内容
    def down_file(self,url):
        time_s = time.time()
        i, content_length, content_size, is_ok = 0, 0, 0, False
        fullcontent, true_url = b'', ''
        while (not is_ok) and (i < self.__maxtries):
            try:
                req, is_get = self.get_file_obj( url, content_size, True)
                if is_get:
                    true_url = req.url
                    fname_list = os.path.basename(true_url).split('.')
                    name = '%s.%s'%(fname_list[0], fname_list[1])
                    ret = req.headers
                    if fname_list[1] in ['htm','html'] : self.encoding = req.apparent_encoding                       # 获取目标的编码格式
                    if "content-length" in ret.keys():                          # 如果有长度，则获取长度
                        if  content_length < int(ret['content-length'])/1024: content_length = int(ret['content-length'])/1024
                        self.printlist([name,content_size/1024,content_length,0])
                    else:
                        content_length = None
                    start_time = time.time()                                    # 请求开始的时间
                    temp_size = 0                                               # 上秒的下载大小
                    for content in req.iter_content(chunk_size=1024):
                        if content:
                            fullcontent += content
                            content_size = len(fullcontent)                            # 统计已下载大小
                            if time.time() - start_time > 1:
                                start_time = time.time()                            # 重置开始时间
                                speed = content_size - temp_size                    # 每秒的下载量
                                if content_length:
                                    self.printlist([name,content_size/1024,content_length,speed/1024])
                                else:
                                    self.printlist([name,content_size/1024,content_size/1024,speed/1024])
                                temp_size = content_size                            # 重置已下载大小
                        else:
                            i += 1
                            self.printstr("第[%d]次:获取chunk内容为空,退出循环,重新获取" %i)
                            break
                    else:                                                       # for语句正常结束，则下载成功
                        #if len(fullcontent) < 1000 :
                        #    if re.search(r"Quota de l'adresse IP dépassé",fullcontent.decode(self.encoding)):       #IP被禁，无法下载
                        #        self.printstr("目标文件因IP配额，禁止下载")
                        #        if globalvar.use_proxy:
                        #            self.proxy_valid = False                                                        #代理失效
                        #            self.url_reinque = True                                                         #重进队列标志
                        #        else:
                        #            self.printstr("当前IP配额已满，请手动切换VPN")
                        #            self.url_reinque = True
                        #            globalvar.must_change_ip = True
                        #        return b'',False,name

                        time_e = time.time()
                        if content_length:
                            self.printlist([name,content_size/1024,content_length,'下载完成,用时[%.0f]秒'%(time_e-time_s)])
                            self.printstr("下载完成[%s]\t已下载[%d]KB/[%d]KB\t共耗时[%.0f]秒\t" %(name,content_size/1024,content_length,time_e-time_s))
                        else:
                            self.printlist([name,content_size/1024,content_size/1024,'下载完成,用时[%.0f]秒'%(time_e-time_s)])
                            self.printstr("下载完成[%s]\t已下载[%d]KB\t共耗时[%.0f]秒\t" %(name,content_size/1024,time_e-time_s))
                        is_ok = True
                else:
                    i += 1
                    self.printstr("第[%d]次:获取request内容为空,重新获取" %i)
            except Exception as e:
                i += 1
                self.printstr("第[%d]次:下载失败\t:[%s],准备第[%d]次重试" %(i,repr(e),i+1))
            if i == self.__maxtries:
                self.printstr("达到最大重试次数，停止获取.")
                self.printstr("达到最大重试次数，停止获取.")
        return fullcontent,is_ok,true_url

    # 获取htm文件中的图片，保存，替换链接
    def get_htm_pic_url(self, url, filename, req):
        if self.encoding is None : self.encoding = 'utf-8'
        pic_soup = BeautifulSoup(req.decode(self.encoding),'lxml')
        html_encoding = self.encoding               #把编码规则赋值给本地变量，否则会被图片下载时覆盖
        imgs = pic_soup.find_all('img')
        ahrefs = pic_soup.find_all('a')
        if imgs:
            fname,ext = os.path.splitext(filename)
            path_str = os.path.join(self.__htmpath , fname)
            img_link_path = os.path.dirname(url)
            for img in imgs:
                src = img.get("src") # 取图片的可用url
                if len(src)>0:
                    img_url = img_link_path + '/' + src
                    path = os.path.join(path_str , img_url.split('/')[-1])
                    l_src = self.download_pic( path , img_url ) # 下载图片
                    if l_src is None : continue
                    img['src'] = "file:///" + l_src.replace("\\","/")  # 更新为本地图片路径
        if ahrefs:
            ahref_path = os.path.join(self.__htmpath , filename)
            for ahref in ahrefs:
                a_src = ahref.get("href")
                if a_src:
                    if ahref_path is None:continue
                    ahref['href'] = "file:///" + ahref_path.replace("\\","/") + a_src
        html = pic_soup.encode(html_encoding) # 重新编译网页源码
        return html

    # 图片下载和保存
    def download_pic(self,path,url):
        pic_path = None
        p_req, is_get, true_url = self.down_file( url)
        if is_get:
            self.write_file( path, p_req)
            pic_path = path
        else:
            self.printstr('没有获取图片文件，不进行写文件操作')
        return pic_path


    # 写入文件
    def write_file(self,path,content):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True) # 自动创建目录
            with open(path,"wb") as f:
                    self.printstr('准备写入[%s]\t' %path)
                    f.write(content) 
                    self.printstr('写入[%s]完成\t' %path)
            f.close
        except Exception as e:
            self.printstr('写文件[%s]发生错误：%s' %(str(path),repr(e)))
            path = None
        return path

    # 下载非HTM格式文档
    def get_download_other(self,url):
        self.printstr("正在获取目标文件链接...")
        pdfpath = None
        self.printstr("准备下载目标文件链接：\t %s" %url)
        pdf_req, is_get, t_url = self.down_file( url)
        if is_get:
            fname, ext = os.path.splitext( os.path.basename(t_url) )
            file_name = '%s%s'%(fname,ext)
            if ext == ".pdf":
                path = os.path.join(self.__pdfpath , file_name)
            else:
                path = os.path.join(self.__otherpath , file_name)
            path = self.write_file( path, pdf_req)
            if os.path.exists(str(path)):
                if ext in ['.epub','.mobi']:
                    self.printstr('准备ebook转换PDF:[%s]'%path)
                    pdfpath = self.ebook_convert(path, 60)
                    if os.path.exists(str(pdfpath)): 
                        stat = "转换[%s]成功,目标路径[%s]" %(path, pdfpath)
                    else:
                        stat = "转换[%s]失败,没有发现目标文件存在" %path
                    self.printstr(stat)
                else:
                    pdfpath = path
            else:
                self.printstr('没有发现文件[%s]，可能写入失败'%path)
        else:
            self.printstr('没有获取目标文件，不进行写文件操作')
        return pdfpath

    def html_pdf(self,path):
        filepath = None
        try:
            path_wkpdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 工具路径
            cfg = pdfkit.configuration(wkhtmltopdf=path_wkpdf)
            options = {'--enable-local-file-access': '--enable-local-file-access',
                        '--outline': '--outline',
                        '--quiet': '--quiet'}
           # 将html文件转为pdf
            filename = path.split("\\")[-1].split(".")[0]+".pdf"
            filepath = os.path.join(self.__pdfpath,filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True) # 自动创建目录
            pdfkit.from_file(path, filepath, configuration=cfg, options = options)
            if os.path.exists(str(filepath)):
                self.printstr("转换[%s]成功,目标路径[%s]" %(path, filepath))
            else:
                raise Exception("没有生成目标文件")
        except Exception as e:
            self.printstr("%s转为PDF出错:\t%s"%(path,repr(e)))
            filepath = None
        return filepath

    def ebook_convert(self,book_path,timeout):           # epub mobi都可以
        filename = os.path.basename(book_path)
        name, ext = os.path.splitext(filename)
        pdfpath = os.path.join(self.__pdfpath, name+'.pdf')
        os.makedirs(os.path.dirname(pdfpath), exist_ok=True) # 自动创建目录
        try:
            process = subprocess.Popen(['ebook-convert', book_path, pdfpath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            t_beginning = time.time() 
            seconds_passed = 0
            que = queue.Queue()
            t_stdout = threading.Thread(target=self.t_read_stdout, args=(process, que))
            t_stdout.daemon = True
            t_stdout.start()
            i = 1
            while process.poll() is None or not que.empty():
                seconds_passed = time.time() - t_beginning 
                if timeout and seconds_passed > timeout: 
                    process.terminate() 
                    raise TimeoutError('转换超时错误',timeout) 
                try:
                    output = que.get(timeout=.5)
                except Exception as e:
                    self.printstr('读取队列发生错误:%s'%repr(e))
                    continue
                if not output:  continue
                text = output.decode('utf-8').replace(u'\n','').replace(u'\r','')
                #if re.search('',text):
                self.printstr('%d:%s'%(i,text))
                i += 1
            t_stdout.join()
        except Exception as e:
            self.printstr('转换发生错误:%s'%repr(e))
            pdfpath = None
        return pdfpath

    def t_read_stdout(self, process, que):
        for output in iter(process.stdout.readline, b''):
            que.put(output)
        return

    def printstr(self,text):
        tlist = [str(QThread.currentThread().objectName()),str(text)]
        self.newText.emit(tlist)

    def printlist(self,plist):
        plist.insert(0,str(QThread.currentThread().objectName()))
        self.newList.emit(plist)

    def printdownlist(self,dlist):
        dlist.insert(0,str(QThread.currentThread().objectName()))
        self.downlist.emit(dlist)

    def printCurRow(self,clist):
        clist.insert(0,str(QThread.currentThread().objectName()))
        self.CurRowSign.emit(clist)

    def printRecId(self,ilist):
        ilist.insert(0,str(QThread.currentThread().objectName()))
        self.RecIdSign.emit(ilist)


