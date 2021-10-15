from bs4 import BeautifulSoup
from urllib.request import urlopen 
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
import openpyxl
import time 
import datetime
from tqdm import tqdm

# 시작 시간
start = time.time()

# (403 error) header 추가후 접근
h = {'User-Agent':'Mozilla/5.0'}
req = "https://www.investing.com/news/stock-market-news"
url = urllib.request.Request(req, headers=h)

# 페이지 전체 html 가져오기
html = urlopen(url)
bsObj = BeautifulSoup(html, "html.parser")
total = bsObj.find_all("a",{'href' and 'title'})

 
# 기사 스크랩!
title = []
link = []
for i, element in enumerate(total):
        
    tit = element.text
    lin = "https://www.investing.com/" + element.attrs['href']
    title.append(tit)
    link.append(lin)
print("기사 스크랩 완료") 
print("기사 스크랩 수: ", len(total))



# 제목 번역
# driver setting & open webChrome with url
driver = webdriver.Chrome()
# driver.maximize_window()
url ='https://www.google.com/'
driver.get(url)
# Adding the sentences into the search box 
driver.find_element_by_css_selector('.gLFyf.gsfi').send_keys("번역")
driver.find_element_by_css_selector('.gLFyf.gsfi').send_keys(Keys.ENTER)
search_xpath = "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/g-expandable-container/div/div/div[2]/div[1]/div[1]"
driver.find_element_by_xpath(search_xpath).click()
time.sleep(0.5)


filename = 'investing_articles_'+datetime.datetime.now().strftime('%Y-%m-%d %H %M')+'.txt'
f = open(filename, 'w', encoding='utf-8')
invest = [] 
for i in tqdm(range(0,len(total))):
    temp=[]
    temp.append(i+1)
    temp.append(title[i])
        
    # temp is clear at 2nd time  
    try:
          
        textbox_xpath = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/g-expandable-container/div/div/div[2]/div[1]/div[1]/div[1]/textarea'
        driver.find_element_by_xpath(textbox_xpath).send_keys(title[i])
                
        xpath_kor = '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/g-expandable-container/div/div/div[2]/div[3]/div/div[2]/div[1]/pre/span'
        kor = driver.find_element_by_xpath(xpath_kor)
        kor_text = kor.text
        
        temp.append(kor_text)
        temp.append(link[i])  
        invest.append(temp)    
           
        time.sleep(1)
        driver.refresh()
        time.sleep(0.5)
        print(str(i+1) +'. '+ title[i] +'   ' + link[i], file=f)
        print('  ' + kor_text, file=f)    
        
    except:
        pass
        print(str(i+1) + "번째 번역 실패")  
f.close()
print('총 번역문 수 = ' + str(len(title)))
df = pd.DataFrame(invest,index=None, columns=['Num','Title',' Translated','Link'])
filename2 = 'investing_articles_'+datetime.datetime.now().strftime('%Y-%m-%d %H %M')+'.xlsx'
df.to_excel(filename2)

# # for i in range(0,len(title)): 
# preq  = link[0]
# url = urllib.request.Request(preq,headers=h)

# driver = webdriver.Chrome()
# driver.get(url)


# xpath ='//*[@id="leftColumn"]/div[3]'
# text = driver.find_element_by_xpath(xpath).get_text 
# print(text)