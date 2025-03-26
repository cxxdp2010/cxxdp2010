#encoding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    with open('./ITSm/new.html',encoding='utf-8') as wb_data:
        soup=BeautifulSoup(wb_data,'lxml')
        #print(soup)
        docs=soup.select('body>tr>td>a')
        flag=8
        for doc in docs:
            ITSM_GAS_STA_NEE=doc.get('onclick').split("','")[1]
            name=doc.get_text()
            if flag % 8 ==0:
                print('编号:{}的 ITSM工单的内部编号为:{}'.format(name,ITSM_GAS_STA_NEE))
                with open("log.txt","a+") as log:
                    log.write('编号:{}的 ITSM工单的内部编号为:{}'.format(name,ITSM_GAS_STA_NEE))

                get_docs(ITSM_GAS_STA_NEE)

            flag=flag+1
            #print(flag %7)
        #print(docs)

def get_docs(str1):
    itsm_url='http://itsm.cnooc:8070/ultrabpp/ultrabpp/view.action?baseSchema=ITSM_GAS_STA_NEE&baseID={}&taskID=&mode=MODIFY'.format(str1)
    browser=webdriver.Ie()
    browser.get(itsm_url)
    print(browser.page_source)

main()
