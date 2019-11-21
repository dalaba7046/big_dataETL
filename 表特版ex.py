import requests,os,urllib
from bs4 import BeautifulSoup
def pic(url):
    headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
    html=requests.get(url ,headers=headers , cookies={'over18': '1'})
    html.encoding="utf-8"
    bs=BeautifulSoup(html.text,'html.parser')
    all_links=bs.find_all('a') #用串列取得所有<img>標籤的內容
    for i in all_links:
        #print(i.get('href'))
        attr=str(i.get('href'))
        if attr!=None and('jpg'in attr or'gif'in attr or'png'in attr):
            full_path = attr #設定圖檔完整路徑    1、網址        
            file_n=full_path.split('/')[-1] #list依照‘/’切割，抓最後一個，從網址的最右側取得圖檔的名稱
            print(attr)
            print('================')
            print('圖檔完整路徑：',full_path)            
            try:  #儲存圖片程式區塊，try不會讓程式中斷
                image = urllib.request.urlopen(full_path)#請求打開圖檔   2
                f = open(os.path.join('/Users/liuyukun/python/pics_dir',file_n),'wb')#將檔案放入pics_dir資料夾（位置，圖片名稱），wb寫入圖檔
                f.write(image.read())#寫入（image），若是用requests就把 read改成text  3
                print('下載成功：%s' %(file_n))
                f.close()
            except: #無法儲存圖片程式區塊
                print("無法下載：%s" %(file_n))
url='https://www.ptt.cc/bbs/Beauty/index3055.html'
headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
data=requests.get(url ,headers=headers , cookies={'over18': '1'})
data.encoding='utf-8'
data1=data.text
data2=BeautifulSoup(data1,'html.parser')
data3=data2.find_all('div', class_='r-ent')
data4=[str(i.find('a')).split('"') for i in data3]

for i in range(0,len(data4)):
    if  'None' not in data4[i]:
         l=data4[i][1]
         url='https://www.ptt.cc'+l
         pic(url)
         
