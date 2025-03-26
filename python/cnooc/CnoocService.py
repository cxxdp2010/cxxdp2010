# -*- coding: utf-8 -*-
import sys
import win32event
import win32service
import win32serviceutil
import servicemanager
import logging
import inspect
import os
from selenium import webdriver
import os,sys,time,random
from apscheduler.schedulers.blocking import BlockingScheduler

class CnoocService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CnoocService"
    _svc_display_name_ = "CnoocService"
    _svc_description_ = "考勤脚本海油"
    _svc_data_dir = None
    # 
    # _ffmpeg_proc = None

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.scheduler=None
        self.dirpath=None
        

    def _getLogger(self):

        logger = logging.getLogger('[CnoocService]')

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, self._svc_name_ + ".log"))
        self._svc_data_dir=dirpath
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.logger.info('CnoocService Service is Starting ...')
            self.start()
            self.logger.info('CnoocService Service Started Success')
            import time
            time.sleep(3)
            # from apscheduler.schedulers.blocking import BlockingScheduler
            
            self.scheduler=BlockingScheduler()
            #self.scheduler.add_job(self.tick,'interval',seconds=300)
            self.scheduler.add_job(func=self.cnooc_login, args=('work',), trigger='cron',day_of_week='0-4',hour=8,minute=29)
            self.scheduler.add_job(func=self.cnooc_login, args=('end',), trigger='cron',day_of_week='0-4',hour=16,minute=50)
            self.logger.info('CnoocService cnooc_login Service is runing')
    
            try:
                self.scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                pass

            # ffmpeg = r'C:\Windows\System32\ffmpeg.exe'
            # cmd = r'%s -f gdigrab -framerate 10 -i desktop D:\\output.mkv -y' % ffmpeg
            # self.logger.info(cmd)
            # self._ffmpeg_proc = subprocess.Popen(cmd, shell=True)
            # try:
            #     sys.exit(self._ffmpeg_proc.wait())
            # except SystemExit as e:
            #     self.logger.warn('Exception : %s' % e)
            # self.logger.info('Screen Recorder Service ffmpeg stop')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            # self._ffmpeg_proc.kill()
            self.logger.info('CnoocService Service Done!')
        except BaseException as e:
            self.logger.warn('Exception : %s' % e)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.logger.info('CnoocService Servicee is Stopping ...')
        self.stop()
        self.logger.info('CnoocService Service Stopped Success')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        if not os.path.exists(self._svc_data_dir):
            os.mkdir(self._svc_data_dir)
        else:
            pass

    def stop(self):
        pass

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))
    def tick(self):
        self.logger.info("自动考勤服务正在运行中。。。。。。。。")
        #打开脚本
    def cnooc_login(self,option=None):
        #手机号
        phone='18301258719'
        #获取打卡参数
        #print(option)
        #option=sys.argv[1]
        #如果输入参数为work，则上班卡
        try:
            #加载谷歌浏览器
            # browser = webdriver.Chrome(executable_path=self._svc_data_dir+'\chromedriver.exe')
            browser = webdriver.Ie(executable_path=self._svc_data_dir+r'\IEDriverServer.exe')

            #打开网址
            browser.get('http://web01.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/agtExtAction_xm?open')
            #如果输入参数为work=上班，end=下班
            if option in ['work','WORK']:
                self.logger.info("开始上班考勤")
                work=browser.find_element_by_xpath("//img[contains(@alt,'上班刷卡')]")
            elif option in ['end','END']:
                self.logger.info("开始下班考勤")
                work=browser.find_element_by_xpath("//img[contains(@alt,'下班刷卡')]")
            else:
                print("输入有误,上班参数work，下班参数end")
                self.logger.info("输入有误,上班参数work，下班参数end，程序退出")
                sys.exit()
            work.click()
            #获取所有句柄
            chandles = browser.window_handles
            self.logger.info(chandles)
            #切换句柄
            browser.switch_to_window(chandles[1])

            
            #查找并输入人员编码
            self.logger.info(browser)
            browser.find_element_by_name("strBianMa_xm").send_keys(phone)
            #查找并输入用户密码
            browser.find_element_by_name("strPwd_xm").send_keys(phone)
            #browser.find_element_by_text("刷卡").first.click()
            #点击刷卡按钮
            browser.find_element_by_id("smartdot_form_Button_1_label").click()
            #获取打卡结果，并在屏幕打印
            info=browser.find_element_by_id("info").text
            self.logger.info(info)
            self.logger.info('考勤正常结束')
            with open("log.txt","a+") as log:
                print(info)
                log.write(info+"\n")
        except Exception  as wdmsg:
           self.logger.warn(wdmsg)
           self.logger.warn('考勤异常结束')

        finally:
            #退出webdriver
            browser.close()
            browser.quit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CnoocService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CnoocService)
