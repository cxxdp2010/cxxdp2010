#coding:utf-8
from splinter import Browser
import time, threading,sys,random

def cnooc_login(url=None, username=None, password=None):
    with Browser(driver_name="chrome") as browser:
        browser.visit(url)
        browser.find_by_name("strBianMa_xm").first.fill(username)  
        browser.find_by_name("strPwd_xm").first.fill(password)  
        browser.find_by_text("刷卡").first.click()
        log=browser.find_by_id("info").first.text
        print(log)
        filelog=open("log.txt","a+")
        filelog.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+log+"\n")
        filelog.close()
	    #print(text)
        #for k, v in browser.cookies.all().items():
         #   print (k, ":", v)         
            
        #quit_browser(browser)
def quit_browser(browser=None):
    flag = input("Input q when you want to quit: ")
    if 'q' == str(flag):
        quit(browser)
    
if __name__=='__main__':
    #url="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%C9%CF%B0%E0"
    #urlxb="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%CF%C2%B0%E0"
	#替换为本人手机号
    username=sys.argv[3]
    password=sys.argv[4]
    if "s"==sys.argv[1]:
        url="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%C9%CF%B0%E0"
    if "e"==sys.argv[1]:
        url="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%CF%C2%B0%E0"
    rantime=random.randint(1, int(sys.argv[2]))
    print(u"打卡随机延迟时间/分钟："+str(rantime))
    time.sleep(rantime*61)
    cnooc_login(url,username,password)
