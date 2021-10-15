from bs4 import BeautifulSoup
from urllib.request import urlopen 
import urllib.parse
import datetime
import time 
from tqdm import tqdm


filename = 'KR_investing_articles_'+datetime.datetime.now().strftime('%Y-%m-%d %H %M')+'.txt'
f = open(filename, 'w', encoding='utf-8')
section = {1:"news/", 2:"news/economy", 3:"news/stock-market-news", 4:"economic-indicators", 5:"commodities-news", 6:"forex-news", 7:"news/cryptocurrency-news"}
h={ 
    1: {'User-Agent':'Mozilla/5.0'}, 
    2: {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'},
    3: {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
    4: {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'},
    5: {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.1985.67 Safari/537.36'},
    6: {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.67 Safari/537.36'},
    7: {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.1985.67 Safari/537.36'}
}

def req_url(x):
    req = 'https://kr.investing.com/{}'.format(section[x])
    url = urllib.request.Request(req, headers=h[x])
    if bool(url) == True:
        return url
# class Parent(self):
#     def __init__(self):
#         print("뉴스 기사 총길이")
#         self.length = len(self)

# class Child_1(Parent):
#     def __init__(self):
#         print("1번 기사입니다")

# class Child_2(Parent):
#     def __init__(self):
        # print("2번 기사입니다")


soup = []
for x in tqdm(range(0,7)): 
    try:
        tempurl = req_url(x+1)
        html = urlopen(tempurl)        
        bsObj = BeautifulSoup(html, "html.parser")
        soup.append(bsObj)
        total = soup[x].find_all("a",{'href' and 'title'})  
    except:
        print('404오류 when article num =', x+1)
        pass      
    tempdic={0:"가장 인기 있는뉴스", 1:"경제 뉴스", 2:"주식 뉴스", 3:"경제 지표 뉴스", 4:"원자재 뉴스", 5:"외환 뉴스", 6:"암호화폐 뉴스"}
    print("***************************************"+ str(x+1) + '.', tempdic[x] +"***************************************", file=f)
    print('\n', file=f)
    for i, element in enumerate(total):
        try:        
            tit = element.text
            lin = "https://kr.investing.com/" + element.attrs['href']                      
            print(str(i+1)+'.', tit, file =f)
            print(lin, file=f, end='')
        except:
            print("또 오류 when catagory num = ", i+1)
        print('\n', file=f)
        print('\n', file=f)
f.close()



