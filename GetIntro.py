# -*- coding:utf-8 -*-
import re
import openpyxl
import os
import time
import random
import emoji
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from PySide6.QtCore import Qt, QObject, Signal, Slot, QEventLoop, QTimer, QThread, QMutex, QMutexLocker
from PySide6.QtWidgets import QTextEdit, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
from PySide6.QtGui import QColor

from globalvar import globalvar


#====================================下载线程类=================================
class WorkerThread(QThread):
    """获取信息线程类"""
    def __init__(self, parent=None, tasks=None):
        QThread.__init__(self, parent)
        self.form = parent
        self.amazon = AmazonGet(self,tasks)
    def run(self):
        self.amazon.main()
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
    def getlistsign(self,plist):        #子线程Tab窗口label lineedit状态更新，
        numlist = re.findall(r'\d+', plist[0])
        num = int(numlist[0])
        curlabname = 'lab' + str(num)
        curlinename = 'line' + str(num)

        curlab = self.form.findChild(QLabel,curlabname)
        curline = self.form.findChild(QLineEdit,curlinename)

        curlab.setText(plist[1])
        curline.setText(plist[2])

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
                    if col == 9 : table.setItem(row,col,QTableWidgetItem(ilist[3]))
                    table.item(row,col).setBackground(QColor('green'))
                    table.item(row,col).setForeground(QColor('white'))
                if ilist[1] == 'fault':
                    if col == 9 : table.setItem(row,col,QTableWidgetItem(self.getTextEditMsg(ilist[0])))
                    table.item(row,col).setBackground(QColor('red'))
                    table.item(row,col).setForeground(QColor('white'))
                if ilist[1] == 'rein':
                    if col == 9 : table.setItem(row,col,QTableWidgetItem(self.getTextEditMsg(ilist[0])))
                    table.item(row,col).setBackground(QColor('yellow'))
            except:
                continue

    def getTextEditMsg(self,threadname):
        numlist = re.findall(r'\d+', threadname)
        num = int(numlist[0])
        textname = 'text' + str(num)
        curtext = self.form.findChild(QTextEdit,textname)
        return curtext.toPlainText()



#====================================下载工作类=================================
class AmazonGet(QObject):
    """工作类"""
    newText = Signal(list)          #更新子线程窗口textedit
    newList = Signal(list)          #更新子线程窗口label lineedit
    CurRowSign = Signal(list)       #子线程窗口list列表下载状态颜色更新
    RecIdSign = Signal(list)        #子线程成功、失败记录ID发送
    downlist = Signal(list)         #子线程窗口list列表添加
    IpSign = Signal(list)            #已使用代理信号

    def __init__(self, parent=None, tasks=None):
        super(self.__class__, self).__init__(parent)
        self.tasks = tasks
        self.newText.connect(parent.getsign)
        self.newList.connect(parent.getlistsign)
        #self.listcount.connect(parent.upd_taskstatus)
        self.downlist.connect(parent.upddownlist)
        self.CurRowSign.connect(parent.updCurRow)
        self.RecIdSign.connect(parent.updRecList)
        self.stop_word = ["Kindle","Optical Character Recognition","This is a reproduction","make these classics available again for future generations to enjoy"]

    def driver_init(self,language):
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--lang=%s'%language)
        #chrome_options.add_argument('--headless')                 # 无窗口模式
        chrome_options.add_argument('--disable-software-rasterizer')            #解决ERROR:gpu_init.cc(426) Passthrough is not supported, GL is swiftshader错误
        chrome_options.add_argument('--ignore-certificate-errors')              #忽略证书错误
        chrome_options.add_argument('-ignore-ssl-errors')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')                            # 禁止硬件加速，避免严重占用cpu
        #chrome_options.add_argument('--disk-cache-dir=d:/chrome_cache')          # 自定义缓存目录
        #chrome_options.add_argument('–disk-cache-size= 20971520')           # 20M cache
        chrome_options.add_argument("disable-web-security")                     # 关闭安全策略
        chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 1})     # 禁止图片加载
        chrome_options.add_argument('disable-infobars')                         # 隐藏"Chrome正在受到自动软件的控制
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])        # 设置开发者模式启动，该模式下webdriver属性为正常值,忽略无用日志，包括usb设备报错
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"')     # 模拟移动设备
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"       #手动指定本机电脑使用的浏览器位置    
        driver=webdriver.Chrome(executable_path=r"chromedriver.exe", options=chrome_options)  
        wait = WebDriverWait(driver, 30, 0.2)                                   # 返回驱动等待的变量
        driver.implicitly_wait(30)                                              # 隐性等待，最长等30秒
        driver.set_page_load_timeout(60)                                        #页面载入超时
        driver.set_script_timeout(60)                                           #脚本执行超时
        return wait,driver

    def title_proc(self,title,num):
        title_1 = re.sub(r"\(.*?\)|\{.*?\}|\[.*?\]", "", title)           #将小括号，中括号，大括号及其中内容置空
        titles = re.findall(r"\w(?:[-'\w]*\w)?",title_1)                           #将标题分割为字母以及\'和连字符\-组成的单词
        i = 1
        return_title = ''
        for item in titles:
            if i <= num:
                return_title = return_title + ' ' + item
                i += 1
            else:
                break
        return return_title

    def author_proc(self,author,num):
        try:
            author_1 = re.findall(r"\[(.*?)\]", author)                     #从中括号中提取内容
            first_author = re.sub(r"\d+\-?\d*", "", author_1[0])            #把提取的第一个列表内容中的数字及-去掉
            first_author = re.sub(r"\(.*?\)|\{.*?\}|\[.*?\]", "", first_author)     #清洗字符串中括号及其中内容
            authors = re.findall(r"\w(?:[-'\w]*\w)?",first_author)          
            i = 1
            return_author = ''
            for item in authors:
                if i <= num:
                    return_author = return_author + ' ' + item
                    i += 1
                else:
                    break
            author = return_author
        except:
            pass
        finally:
            return author



    def amazon_get_intro(self,wait,driver,url,title,author,delay,intro_min_length):
        web = r'''https://www.amazon.com'''
        intro = ''
        intro_length = 0
        driver.get(url)                                         #载入首页
        QThread.sleep(delay)
        try:
            wait.until(lambda x:x.find_element_by_id("asMain"))      #css选择器，返回结果存在跳出，异常报错   ec.presence_of_element_located((By.ID,"pageContent"))
            self.printstr('载入链接，开始输入数据:\t作者[%s]\t题名[%s]'%(author,title))
        
            #opt = driver.find_element_by_name("sort")
            #Select(opt).select_by_value("salesrank")
            driver.find_element_by_name("field-title").send_keys(title)
            driver.find_element_by_name("field-author").send_keys(author)
            self.printstr('开始检索书名[%s]'%title)
            driver.find_element_by_name("Adv-Srch-Books-Submit").click()          # driver自动点击搜索按钮，开始搜索

            QThread.sleep(delay)
            try:
                wait.until(lambda x:x.find_element_by_id("search"))      #css选择器，返回结果存在跳出，异常报错ec.presence_of_element_located((By.CLASS_NAME, "s-main-slot.s-result-list.s-search-results.sg-row"))
                list_driver = driver
                self.printstr('载入链接，开始处理检索结果')
                list_soup = BeautifulSoup(driver.page_source,'lxml')
                result = list_soup.find_all('div',class_='a-section a-spacing-small a-spacing-top-small')
                if result:
                    self.printstr(result[0].text.replace('\n',''))
                    search_list = list_soup.find_all('h2',class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
                    if search_list:
                        i = 0
                        for item in search_list:
                            i += 1
                            list_title = item.select('a')[0].text
                            list_url = item.select('a')[0]['href']
                            self.printstr('开始载入第[%d]/[%d]个检索结果[%s]'%(i, len(search_list), list_title))
                            one_url = web + list_url       
                            self.printstr('载入数据,链接为:[%s]'%one_url)
                            driver.get(one_url)                                         #转到内容页
                            QThread.sleep(delay)
                            try:
                                wait.until(lambda x:x.find_element_by_id("dp"))      #css选择器，返回结果存在跳出，异常报错ec.presence_of_element_located((By.ID, "dp"))
                                self.printstr('detail页载入完成')
                                try:
                                    self.printstr('定位简介容器[book_description_expander]...')
                                    intro = driver.find_element_by_css_selector("div[data-a-expander-name=\"book_description_expander\"]>div").get_attribute("textContent").strip()
                                    intro_length = len(re.findall(r"\w(?:[-'\w]*\w)?",intro))
                                    if intro_length < intro_min_length or self.have_stopword(intro):
                                        self.printstr('获取简介过短[%d]或者包含禁止词，继续尝试下一条检索结果...\r简介内容为:[%s]'%(intro_length,intro))
                                        intro = ''
                                    else:
                                        self.printstr("简介长度为[%d],内容为:[%s]"%(intro_length,intro))
                                        break
                                except Exception as e:
                                    self.printstr('无法找到简介容器[book_description_expander],转入iframe处理...')
                                    try:
                                        iframe = driver.find_element_by_id("bookDesc_iframe")
                                        driver.switch_to.frame(iframe)                              #转到iframe
                                        self.printstr('载入iframe...')
                                        QThread.sleep(delay)
                                        try:
                                            intro = wait.until(lambda x:x.find_element_by_id("iframeContent")).text      #css选择器，返回结果存在跳出，异常报错ec.presence_of_element_located((By.ID, "iframeContent"))
                                            intro_length = len(re.findall(r"\w(?:[-'\w]*\w)?",intro))
                                            if intro_length < intro_min_length or self.have_stopword(intro):
                                                self.printstr('获取简介过短[%d]或者包含禁止词，继续尝试下一条检索结果...\r简介内容为:[%s]'%(intro_length,intro))
                                                intro = ''
                                            else:
                                                self.printstr("简介长度为[%d],内容为:[%s]"%(intro_length,intro))
                                                break
                                        except Exception as e:
                                            self.printstr('iframe没有加载完成/t[%s]'%repr(e))
                                    except Exception as e:
                                        self.printstr('无法找到iframe元素...')
                            except  Exception as e:
                                self.printstr('detail页没有加载完成/t[%s]'%repr(e))
                    else:
                        self.printstr('没有发现题名为[%s]的检索结果列表'%title)
                else:
                    self.printstr('[%s]没有检索到结果'%title)
            except Exception as e:
                self.printstr('检索列表页没有加载完成/t[%s]'%repr(e))
        except Exception as e:
            self.printstr('高级检索页页没有加载完成/t[%s]'%repr(e))
        return intro,len(intro)

    def main(self):
        threadname = str(QThread.currentThread().objectName())
        start_time = time.time()
        url = globalvar.url
        language = 'en-us.UTF-8'
        wait, driver = self.driver_init(language)
        circle_init = False
        while not globalvar.record_queue.empty():
            try:
                rec_info = globalvar.record_queue.get()
                self.printstr('当前位于线程[%s],程序启动时间[%d],本次循环开始时间[%d],时间差为[%d]'%(threadname, start_time, time.time(), time.time()-start_time))
                if time.time() - start_time > 600:
                    if driver : driver.quit()
                    self.clear_cache()
                    start_time = time.time()
                    circle_init = True
                if circle_init:
                    language = 'en-us.UTF-8'
                    wait, driver = self.driver_init(language)
                    circle_init = False

                self.printstr('当前处理记录:[%s]'%rec_info[1])
                if rec_info[3]:
                    book_name = rec_info[3].replace('\n', ' ').replace('\r', ' ')
                else:
                    book_name = rec_info[3]
                if rec_info[2]:
                    author_name = rec_info[2].replace('\n', ' ').replace('\r', ' ')
                else:
                    author_name = rec_info[2]

                self.printdownlist( ['[%s][%s]'%(rec_info[1],rec_info[3]) ] )
                self.printCurRow(['begin','[%s][%s]'%(rec_info[1],rec_info[3])])

                intro, i, author, need_author, j, intro_length = '', 10, '', True, 0, 0
                min_key = 3
                while intro_length == 0 and (i >= min_key):
                    try:
                        j += 1
                        self.printstr('当前标题单词数量为[%d]'% i )
                        title = self.title_proc(book_name, i)
                        i = i - 1
                        if author_name and need_author:
                            author = self.author_proc(author_name, 3)
                        self.printlist(['第[%d]次策略循环'%j, '标题:[%s],作者:[%s]'%(title, author)])
                        self.printstr('第[%d]次策略循环,标题:[%s],作者:[%s]'%(j, title, author))
                        intro, intro_length = self.amazon_get_intro(wait, driver, url, title, author, 15, 10)
                        self.printstr('第[%d]次策略循环,标题单词数量[%d],获取简介长度:[%d],简介内容:[%s]'%(j, i, intro_length, intro))
                        if i == 2 and len(intro)==0 and need_author:        #如果指定作者检索一直检索不到内容，那么去掉作者检索
                            i = 10
                            need_author = False
                            author = ''
                            min_key = 4
                    except Exception as e:
                        self.printstr('出现错误，继续循环策略..[%s]'%repr(e))
                if intro:
                    self.printlist(['第[%d]次策略循环已经获取成功'%j, '标题:[%s],作者:[%s]'%(title, author)])
                    self.printCurRow(['success','[%s][%s]'%(rec_info[1],rec_info[3])])
                    globalvar.success_queue.put(rec_info[1])
                    self.tasks[threadname][0] += 1 
                    self.printRecId(['success',rec_info[1],self.proc_content(intro)])
                    self.tasks[threadname][2] += 1
                else:
                    self.printstr('已进行[%d]次策略循环，仍未获取数据，策略失败，停止获取..'%j)
                    self.printlist(['已进行[%d]次策略循环，仍未获取数据，策略失败..'%j, '标题:[%s],作者:[%s]'%(title, author)])
                    self.printCurRow(['fault','[%s][%s]'%(rec_info[1],rec_info[3])])
                    globalvar.fault_queue.put(rec_info[1])
                    self.tasks[threadname][1] += 1 
                    self.printRecId(['fault',rec_info[1],'None'])
                    self.tasks[threadname][2] += 1
            except Exception as e:
                self.printstr('出现错误,本条记录重新进入队列,错误信息:[%s]'%repr(e))
                globalvar.record_queue.put(rec_info)
                self.printRecId(['rein',rec_info[1],'None'])
                if driver: driver.quit()
                circle_init = True
            QThread.sleep(random.randint(15,30)) 
        if driver: driver.quit()

    def clear_cache(self):
        language = 'zh_CN.UTF-8'
        wait, driver = self.driver_init(language)
        url = 'chrome://settings/clearBrowserData'
        driver.get(url)
        QThread.sleep(5)
        clearButton = driver.execute_script("return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
        clearButton.click()
        QThread.sleep(10)
        driver.quit()

    def have_stopword(self,intro):
        is_have = False
        for item in self.stop_word:
            have_text = re.findall(item,intro)
            if have_text:
                is_have = True
                break
        return is_have

    def proc_content(self, content):             #清理字符串中的表情字符，表情字符会导致selenium出错
        if content:
            etext = emoji.demojize(content.replace('_x000D_',' ').replace('\n', ' ').replace('\r', ' '))
        else:
            etext = emoji.demojize(content)
        result = re.sub(':\S+?:', ' ', etext)
        result = re.sub('<[^>]*?>','',result)       #清除尖括号标签
        return result

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


#if __name__ == "__main__":
#    amazon = AmazonGet()
#    os.system('')
#    path = r'D:\GitHub\pyside\pdf_spider\france.xlsx'
#    url = r'''https://www.amazon.com/advanced-search/books'''
#    amazon.main(path,url)
#    clear_cache()

    
    




