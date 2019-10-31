import json
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pymongo import MongoClient



def  MongoBase(host,port,database,table,data):
    #設定mongoDB連線
    client = MongoClient(host, port)
    #連線後設定要放入資料的database
    db=client[database]#database名稱為591spider
    #選擇要放入的資料表
    spider = db[table]#資料表名稱為spider
    #操作mongoDB放入資料
    spider.insert(json.loads(data.T.to_json()).values())
    
    
#建立所需資料集合
linkman =[]#出租者
nick_name = []#身分
house_attr =[]#型態
house_phone = []#電話
kind_name = []#現況
house_gender =[]#性別要求
#header的tokene跟coockie每次都要換
api_two='https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow='
try:
    for m in range(365):
        print("第{}筆".format(m))
        m=m*30
        apiurl=api_two+str(m)
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=k0gingasp4ndf66qnkqpaokon1; urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; new_rent_list_kind_test=0; 591_new_session=eyJpdiI6IjF6cDlldGI4c0t0Q29tSVJ4UHJ6UEE9PSIsInZhbHVlIjoia2IwUzBRQnRwZFZLSW1TeVJMY1hDUXdTdHRxZjFHU0t6VXFOZHVDaXhPQ3JnaE8rVFJMcHVvK3JjZjFtVVVpbzVTeVE3SHViVmFQd0ZpVXpzR3VpMFE9PSIsIm1hYyI6IjQ5YWJhMzU3MDY2YWEyMWQ3M2NkMzM1ZGUxNDJlNWFiYzZiMGMwMzIwOWMyYzcyOWI5MWU4NWM5NjA0OWZiYTkifQ%3D%3D; T591_TOKEN=k0gingasp4ndf66qnkqpaokon1; c10f3143a018a0513ebe1e8d27b5391c=1; _ga=GA1.3.1587201468.1572241758; _gid=GA1.3.1335629771.1572241758; _ga=GA1.4.1587201468.1572241758; _gid=GA1.4.1335629771.1572241758; XSRF-TOKEN=eyJpdiI6ImZ2NmY1dEhQT0FRMk9BT0l1WksycEE9PSIsInZhbHVlIjoiVnFLM25WbmU3MWw2bkd0VzdCT2l4cGhhSFNBdk9LNjhTbDNyMXRaUnZKVkIrUE96ZFRVcmVUMUx5bWRSY2JTdjZ0U2xXeGNjNEFac1BtTnVIYlRsaGc9PSIsIm1hYyI6IjBkYTM2MTFhMzU5NDkyYWU5ODYzZWQ0ZmRlZTc0YTVmNTMzODJhMzJiMDEzMTFkMTZmODg1MGI1MTM3MjZjOGUifQ%3D%3D; _fbp=fb.2.1572241759237.1405095899; DETAIL[1][8334570]=1; user_index_role=1; user_browse_recent=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228334570%22%3B%7D%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%2280d9a8e15314a3fb67dc8fbceb75e1d4%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-8334570.html%22%3Bs%3A7%3A%22time_ex%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22time%22%3Bi%3A1572241969%3B%7D; __asc=0e60daee16e10ec8e498c3846ec; __auc=0e60daee16e10ec8e498c3846ec; localTime=1; _gat_UA-97423186-1=1',
            'Host': 'rent.591.com.tw',
            'Referer': 'https://rent.591.com.tw/v2/rent?regionid=3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' ,
            'X-CSRF-TOKEN': 'RNGEni8wMneYEXj7JeaB3GNnN8N8B8ufCaz9jiJ0',
            'X-Requested-With':'XMLHttpRequest'
            }
        req = requests.get(api_two, headers=headers)
        html = bs(req.text,'html.parser')
        goods_url = json.loads(html.text)
        #根據API爬取出租者,身分,現況
        for i in range(30):
            linkman.append(goods_url['data']['data'][i]['linkman'])
            nick_name.append(goods_url['data']['data'][i]['nick_name'][0:2])
            kind_name.append(goods_url['data']['data'][i]['kind_name'])
            
        #建立物件url,方便等等爬取電話,型態,性別要求
        urls_id=[]
        for j in range(30):
            try:
                good_url = goods_url['data']['data'][j]['id']
                urls_id.append(good_url)   
            except:
                pass
        urls=[]
        for k in range(len(urls_id)):
            under_url = 'https://rent.591.com.tw/rent-detail-'+ str(urls_id[k]) +'.html'
            urls.append(under_url)
            under_req = requests.get(under_url, headers=headers)
            u_task = bs(under_req.text,'html.parser')
        #    print(under_url)
        
        #爬取物件中的型態+性別要求
        
        for url in urls:
            res = requests.get(url, headers=headers)
            soup = bs(res.text,'html.parser')
            task=soup.select('ul[class="attr"]')[0].find_all('li')
            task_len=len(task)
            for l in range(task_len):
                task[l]=task[l].get_text()
                if  "型態" in task[l]:
            #型態取出
                    house_attr.append(task[l].replace('\xa0','').replace('型態:',''))
                else:
                    pass 
            #性別要求取出
            task2=soup.select('ul[class="clearfix labelList labelList-1"]')[0].find_all('li')[1].get_text()
            gender = task2.find('性別要求')
            try:
                if gender != -1:
                    house_gender.append(task2[gender:gender+10].replace("性別要求：","").replace('朝向：','').replace('隔間材','').replace('可遷入',''))
                else:
                    house_gender.append("None")
            except:
                    pass
            #電話取出
            try:
                phone=soup.select('span[class="dialPhoneNum"]')[0].get('data-value')
                house_phone.append(phone)
            except:
                pass
    df= pd.concat([pd.DataFrame({'linkman': linkman}), pd.DataFrame({'nick_name':nick_name}), pd.DataFrame({'house_attr':house_attr}), 
         pd.DataFrame({'kind_name':kind_name}), pd.DataFrame({'house_phone':house_phone}), pd.DataFrame({'house_gender':house_gender})], axis=1)
except:
    pass
if __name__ =='__main__':
    #mongoDB設定
    host='localhost'
    port=27017
    database='591spider'
    table='xin_bei'
    data=df
    MongoBase(host,port,database,table,data)
