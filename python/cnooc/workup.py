from selenium import webdriver
import time,threading,sys,random,datetime,configparser

#海油上下班打卡
def cnooc_login(url=None, username=None, password=None, webName=None):

    #3分钟内随机打卡
    #rantime=random.randint(1,3)
    #print(u"打卡随机延迟时间/分钟："+str(rantime))
    browser = getWebDriver(webName)
    #打卡地址
    browser.get(url)
    
    now=datetime.datetime.now()

    #操作浏览器
    browser.find_element_by_name("strBianMa_xm").send_keys(username)  
    browser.find_element_by_name("strPwd_xm").send_keys(password)  
    browser.find_element_by_id("smartdot_form_Button_1_label").click()
    info=browser.find_element_by_id("info").text
    print(info)
    with open("log.txt","a+") as log:
        log.write("打卡时间:"+str(now.hour)+":"+str(now.minute)+"====>")
        log.write(info+"\n")
    #browser.quit()
    print("刷卡结束")

def getWebDriver(name):
    #加载Edge浏览器驱动
    if name=="Ie":
        browser = webdriver.Ie()
    #加载firefox浏览器驱动
    if name=="Firefox":
        browser = webdriver.Firefox()
    #加载Chrome浏览器驱动
    if name=="Chrome":
        browser = webdriver.Chrome()
    return browser

if __name__=='__main__':
    #打开文件操作
    log=open("log.txt","a+")
    #配置文件
    config = configparser.ConfigParser()
    config.read("config.ini")
    cfg=dict(config.items("setting"))  
    while True:
        now=datetime.datetime.now()
        url=0
        #判断上班打卡时间
        if  now.hour<=int(cfg['workstart_h']) and now.hour>=7 and now.minute<=int(cfg['workstart_m']):
            url="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%C9%CF%B0%E0"
            print("当前时间"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"上班卡")
            #log.write("==========上班卡开始==========="+str(now.hour)+":"+str(now.minute)+"\n")
        #判断下班班打卡时间
        if  now.hour>=int(cfg['workend_h']) and now.hour<=22 and now.minute>=int(cfg['workend_m']):
            url="http://web01as1.oa.cnooc/zgsjg/itc/EX_ZGS_wlrykq.nsf/frmShuaKaNew_xm?openform&SkType=%CF%C2%B0%E0"
            print("当前时间"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"下班卡")
            #log.write("==========下班卡开始==========="+str(now.hour)+":"+str(now.minute)+"\n")
        time.sleep(5)
        if url!=0:
            #print("开始打卡")
            cnooc_login(url,cfg['name'],cfg['name'],cfg['webname'])
            with open("log.txt","a+") as log:
                log.write("打卡成功程序停止5小时"+"\n") 
            time.sleep(18000)
            
        with open("log.txt","a+") as log:
            print("不到打卡时间")
            log.write("不到打卡时间"+"\n")