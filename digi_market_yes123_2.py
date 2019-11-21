from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def job_page(url):
    head={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding":"gzip, deflate, br",   
            "Host":"www.yes123.com.tw",
            "Referer":"https://www.yes123.com.tw/admin/job_refer_list.asp",
            "Cookie":"_sh_c_2=search_type%3Ajob%7Csearch_item%3A1; _sh_c_1=search_type%3Ajob%7Csearch_item%3A1%7Csearch_key_word%3A%E7%B6%B2%E8%B7%AF%E5%B0%8F%E7%B7%A8%7Cfind_key2%3A%E7%B6%B2%E8%B7%AF%E5%B0%8F%E7%B7%A8; _gcl_au=1.1.1397802470.1560331499; __auc=718fcebb16b4b0134565d7361bf; _ga=GA1.3.1956786803.1560331499; yes123_make_cookie=3ac316d6e4e6f15a64b70d258db939ae; ASPSESSIONIDSARSTDTT=MEJOBKEBFDHCDENIFEBJDBAM; NSC_xxx=ffffffffaf19007945525d5f4f58455e445a4a423660; citrix_ns_id=CycCkoniJRbmrNUHmXSzAaAs0H80000; ApplicationGatewayAffinity=802db5cd0d15c582172e07ad49208c95e43d15e73850ec3fdce991eca23ded3c; ASP.NET_SessionId=346158876; StepCookie_id=346158876; ClientIP=203.67.127.86; __asc=d0158e5a16bd4fd9be92e055e14; _gid=GA1.3.784869396.1562646519; step=6"
            }
    html=requests.get(url,headers=head)
    html.encoding='utf-8' 
    soup = bs(html.text, 'html.parser')
    #職缺名稱
    title=soup.find('h1').text
    
    #公司名稱
    com_tag=soup.find('div',class_='jobname_title').find('p').text

    #com_tag=soup.find('p').text
    Company=com_tag.replace('回公司介紹','')
    
    #標題(span.tt),排除工作內容
    Title=[]
    for Title1 in soup.find_all('span',class_='tt'):
            Title.append(Title1.get_text())
    Title=Title[1:12]
    
    #內容(span.rr),排除工作內容
    Content=[]
    for Content1 in soup.find_all('span',class_='rr'):
        Content.append(Content1.get_text())
    Content=Content[1:12]
    Content[0]=Content[0].replace('\r','').replace('\n','').replace('\t','').replace(' ','').replace('地圖','').replace('\xa0','')
    Content[1]=Content[1].replace('\xa0','').replace('職涯發展地圖','')
    Content[3]=Content[3].replace('\xa0','')
    Content[4]=Content[4].replace('\xa0','')
    Content[6]=Content[6].replace('\xa0','').replace('每月薪資行情表我要申訴','')
    Content[7]=Content[7].replace('每月薪資行情表我要申訴','')
    #工作內容
    job_tag=soup.find_all('span',class_='rr')
    Job=job_tag[0].text.replace('\u3000','').replace('\r','').replace(',','').replace('\br','').replace('\t','')
    #工作條件
    
    #Work_detail=soup.select('div.comp_detail')[1].text.replace('\n','').replace('\t','').replace('\xa0','').replace('\u3000','').replace('\r','').replace('科系就業導航','').replace('工作條件','')
    Work_detail=soup.select('div.comp_detail')[1]
    work_tag=[]
    for tags in Work_detail.find_all('span',class_='tt'):
        work_tag.append(tags.get_text())
    work_content=[]
    for tags1 in Work_detail.find_all('span',class_='rr'):
        work_content.append(tags1.get_text())
    try:
        work_content[0]=work_content[0].replace('\r','').replace('\n','').replace('\xa0','').replace('\t','').replace('科系就業導航','')
        work_content[1] =work_content[1].replace('\r','').replace('\n','').replace('\xa0','').replace('科系就業導航','')
        work_content[2]=work_content[2].replace('\r','').replace('\n','').replace('\xa0','').replace('科系就業導航','')
        work_content[3]=work_content[3].replace('\r','').replace('\n','').replace('\xa0','').replace('科系就業導航','')
        work_content[4]=work_content[4].replace('\r','').replace('\n','').replace('\xa0','').replace('科系就業導航','')
        work_content[5]=work_content[5].replace('\r','').replace('\n','').replace('\xa0','').replace('科系就業導航','')
    except IndexError:
        pass
    #需求技能
    #Work_skill=soup.select('div.comp_detail')[2].text.replace('\n','').replace('\xa0','').replace('\u2028','')
    Work_skill=soup.select('div.comp_detail')[2]
    skill_Tag=[]
    for skill in Work_skill.find_all('span',class_='tt'):
        skill_Tag.append(skill.get_text())
    skill_Content=[]
    for content in Work_skill.find_all('span',class_='rr'):
        skill_Content.append(content.get_text())
    #skill_Content[0]=skill_Content[0].replace('\n','').replace('\xa0','').replace('\u2028','')
    #skill_Content[1]=skill_Content[1].replace('\n','').replace('\xa0','').replace('\u2028','')
    #skill_Content[2]=skill_Content[2].replace('\n','').replace('\xa0','').replace('\u2028','')

    #聯絡方式
    Contact=[]
    for contact1 in soup.find_all('span',class_='rr'):
        Contact.append(contact1.get_text())
    Contact=Contact[-4:-2]
    Contact[0]=Contact[0].replace(',','').replace('\xa0','').replace('\r','').replace('\n','')
    Contact[1]=Contact[1].replace(',','').replace('\xa0','').replace('\r','').replace('\n','')
    #Contact[2]=Contact[2].replace(',','').replace('\xa0','').replace('\r','').replace('\n','')

    
    Dic={}
    
    Dic["公司名稱： "]=Company
    Dic["標題： "]=title
    Dic["工作內容： "]=Job
    title_num=(len(Content))
    for i in range(0,title_num):
        Dic[Title[i]]=Content[i]
    
    title_num2=(len(work_content))
    for j in range(0,title_num2):
        Dic[work_tag[j]]=work_content[j]
    try:
        title_num3=(len(skill_Content))
    except:    
        for k in range(0,title_num3):
            Dic[skill_Tag[k]]=skill_Content[k]
            continue
    Dic["聯絡方式： "]=Contact
    Dic['url']=url
    if '職位等級 ： ' in Dic:
        del Dic['職位等級 ： ']
    if '方言能力 ： ' in Dic:
       del Dic['方言能力 ： ']
    if '外語能力 ： ' in Dic:
       del Dic['外語能力 ： ']
    if '工作日期 ： ' in Dic:
       del Dic['工作日期 ： ']
    return Dic

x=0
li=open('digi_market.txt','r')
lines=li.readlines()
Output=pd.DataFrame()
##將url去掉最後的\n
job_num=len(lines)
for i in range(job_num):
   lines[i]=lines[i].replace('\n','')
for j in lines:
    x=x+1
    print("主人,我現在爬到第",x,"個")
    Output=pd.DataFrame(job_page(j)).append(Output, ignore_index=True)
    time.sleep(2)
    Output=Output.drop_duplicates(['url'])
#輸出ｃｓｖ
Output.to_csv('digi_market.csv')
li.close()