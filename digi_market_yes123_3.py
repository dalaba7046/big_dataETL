import pandas as pd
import re

csv=pd.read_csv('digi_market.csv')
 #=============================================================================
csv = csv.rename(index=str, columns={"標題： ": "title", "公司名稱： ": "cName", "工作內容： ": "jobCont","工作地點 ： ": "jobLoc", "管理人數 ： ": "manage", "職缺更新 ： ": "job_update", 
                               "上班時段 ： ": "workT", "休假制度 ： ": "vacation", "薪資待遇 ： ": "salary", "工作性質 ： ": "empType", "職務類別 ： ": "category", "需求人數 ： ": "hireNum", "身份類別 ： ": "accept",
                               "學歷要求 ： ": "edu", "科系要求 ： ": "department", "工作經驗 ： ": "workExp", "聯絡方式： ": "contact", "語言能力 ： ": "lan", "電腦專長": "skills", "出差說明 ： ": "busTrip",
                               "擅長工作 ： ": "tools","附加條件 ： ":"otherReq",'工作條件':'work_detail','url':'href'
                               })
#csv['lan','tools','skills','otherReq','sabisu','email','brand_Adv']=''
csv=csv.drop(columns=['Unnamed: 0','工作經歷 ： '],axis=1)
Title_Len=len(csv['title'])
csv["newJobLoc"] = "NA"
for i in range(Title_Len):
    csv["newJobLoc"][i] = csv['jobLoc'][i][0] + csv['jobLoc'][i][
        1] + csv['jobLoc'][i][2]

# #重新排列
#csv = csv[['title','cName','jobCont','jobLoc','category','vacation','workT','hireNum','empType','manage','busTrip','salary',
#            'job_update','accept','workExp','edu','department','lan','tools','skills','otherReq','sabisu','insurance','entertain','bonus',
#            'contact','email','similar','workD','jobRegion',
#            'newJobLoc','furlough','newHireNum','newEmpType','newManage',
#            'newBusTrip','monthSalary','hourSalary','otherSalary','workUpdate',
#            'newWorkExp','newEdu','jobKey','humanBank','href','work_detail','brand_Adv']]
csv['jobKey'] = '網路小編'
csv['humanBank'] = 'yes123'
csv['insurance'] = 'NA'
csv['entertain'] = 'NA'
csv['bonus'] = 'NA'
csv['similar'] = 'NA'



csv["newJobLoc"]='NA'
for l in range(Title_Len):
     csv["newJobLoc"][l] = csv['jobLoc'][l][0] + csv['jobLoc'][l][1] +csv['jobLoc'][l][2]
 
csv["jobRegion"] = "NA"
locc = ["新北市","台北市","桃園市","新竹市","新竹縣","基隆市","苗栗縣","台中市","彰化縣","南投縣",
       "雲林縣","嘉義縣","嘉義市","台南市","高雄市","屏東縣","屏東市","宜蘭縣","花蓮縣","台東縣","澎湖縣","金門縣","馬祖縣"]
for i in range (Title_Len):
    if csv["newJobLoc"][i] in locc[0:7]:
        csv["jobRegion"][i]="北部"
    elif csv["newJobLoc"][i] in locc[7:13]:
        csv["jobRegion"][i]="中部"
    elif csv["newJobLoc"][i] in locc[13:17]:
        csv["jobRegion"][i]="南部"
    elif csv["newJobLoc"][i] in locc[17:20]:
        csv["jobRegion"][i]="東部"
    elif csv["newJobLoc"][i] in locc[20:23]:
        csv["jobRegion"][i]="外島"
    else:
        csv["jobRegion"][i]="其他"
 
csv["furlough"] = csv["vacation"]
for i in range(Title_Len): 
    if "依公司規定" in csv["vacation"][i]:
        csv["furlough"][i] = csv["vacation"][i].replace(csv["vacation"][i][6:],'')
    elif "排班制" in csv ["vacation"][i]:
                csv["furlough"][i] = csv["vacation"][i].replace(csv["vacation"][i][3:],'')

csv["workTime"] = "NA"
for m in range(Title_Len):
     if "，" in csv['workT'][m]:
         key = csv['workT'][m]
         p1 = "^.*?，"
         pattern1 = re.compile(p1)
         reNet = str(pattern1.findall(key)).replace("，", "").replace(r"/", r"、").replace("'", "").replace(r"[",
                                                                                                          "").replace(
             r"]", "")
         csv['workTime'][m] = reNet
     else:
         csv['workTime'][m] = csv['workT'][m].replace(r"/", r"、")
 
csv["newHireNum"] = "0"
for n in range(Title_Len):
     csv['hireNum'][n]=str(csv['hireNum'][n])
     if "不拘" in csv['hireNum'][n]:
         csv['newHireNum'][n]='0'
     else:
         csv["newHireNum"][n]=csv['hireNum'][n].replace(csv['hireNum'][n][1:],'')
 
csv["newEmpType"] = "NA"
for o in range(Title_Len):
     if "全職" in csv['empType'][o]:
         csv['newEmpType'][o] = "全職"
     elif "兼職" in csv['empType'][o]:
         csv['newEmpType'][o] = "兼職"
     else:
         csv['newEmpType'][o] = "其他"
 
csv["newManage"] = "NA"
for p in range(Title_Len):
     if csv['manage'][p] == "NA":
         csv["newManage"][p] = "NA"
     elif "不需" in csv['manage'][p]:
         csv["newManage"][p] = "N"
     else:
         csv["newManage"][p] = "Y"
 

csv["newBusTrip"] = "NA"
for q in range(Title_Len):
     if csv['busTrip'][q] == "NA":
         csv["newBusTrip"][q] = "NA"
     elif "不需" in str(csv['busTrip'][q]):
         csv["newBusTrip"][q] = "N"
     else:
         csv["newBusTrip"][q] = "Y"
 
csv["monthSalary"] = "0"
csv["hourSalary"] = "0"
csv["otherSalary"] = "NA"
for s in range(Title_Len):
     if "月薪" in csv['salary'][s]:
         csv['monthSalary'][s] = str(
             csv['salary'][s].replace("月薪", "").replace(" ", "").replace("元", "").replace(",",
                                                                                                            "").replace("'", ""))
         if "至" in csv['monthSalary'][s]:
             csv['monthSalary'][s] = csv['monthSalary'][s].replace("月薪", "").replace(
                 " ", "").replace("元", "").replace(",", "").replace("'", "").replace(csv['monthSalary'][s][11:],'').split("至")
             csv['monthSalary'][s] = (int((int(csv['monthSalary'][s][0]) + int(
                 csv['monthSalary'][s][1])) / 2))
 
     if "時薪" in csv['salary'][s]:
         csv['hourSalary'][s] = str(
             csv['salary'][s].replace(r"/小時", "").replace(" ", "").replace("元", "").replace("時薪",
                                                                                                              "").replace(
                 "'", ""))
 
         if "至" in csv['hourSalary'][s]:
             csv['hourSalary'][s] = csv['hourSalary'][s].split("至")
             csv['hourSalary'][s] = (int(
                 (int(csv['hourSalary'][s][0]) + int(csv['hourSalary'][s][1])) / 2))
 
     if "面議" in csv['salary'][s]:
         csv['otherSalary'][s] = "面議"
 
csv["workUpdate"] = "NA"
for z in range (Title_Len):
    csv['job_update'][z]=csv['job_update'][z].replace('年','/').replace('月','/').replace('日','')
for i in range (Title_Len):
    g = str(csv['job_update'][i].replace(r"更新日期：", ""))
    if "工作內容" in g:
        g =0
        csv["workUpdate"][i]=g
    else:
        s =g.split('/')#分割成list
        q = list(map(int, s)) #這裡要將裡面的list轉成int
        if q[1] < 10 :
            h ="%02d" % q[1] #  %02d"補0
            q[1] =h
        if q[2] < 10 :
            h ="%02d" % q[2]  #  %02d"補0
            q[2] =h
        k = list(map(str, q)) #這裡要將裡面的list轉成str
        u =''
        l =u.join(k) #這裡要將裡面的list合併為str
        csv["workUpdate"][i]=l 
csv["newAccept"] = csv['accept']
 
csv["newWorkExp"] = "0"
for u in range(Title_Len):
     csv['newWorkExp'][u] = csv['workExp'][u].replace("年以上", "")
     if csv['workExp'][u] == "不拘":
         csv['newWorkExp'][u] = "0"
 
csv["newEdu"] = "NA"
for i in range(Title_Len):
    csv["edu"][i]=str(csv["edu"][i])
for v in range(Title_Len):
     if '國小' in csv["edu"][v]:
         csv["newEdu"][v] = '國小'
     elif '國中' in csv["edu"][v]:
         csv["newEdu"][v] = '國中'
     elif '高職' in csv["edu"][v]:
         csv["newEdu"][v] = '高職'
     elif '高中' in csv["edu"][v]:
         csv["newEdu"][v] = '高中'
     elif '專科' in csv["edu"][v]:
         csv["newEdu"][v] = '專科'
     elif '大學' in csv["edu"][v]:
         csv["newEdu"][v] = '大學'
     elif '碩士' in csv["edu"][v]:
         csv["newEdu"][v] = '碩士'
     elif '博士' in csv["edu"][v]:
         csv["newEdu"][v] = '博士'
     elif '不拘' in csv["edu"][v]:
         csv["newEdu"][v] = '不拘'
 
csv["dep"] = csv['department']
 
csv["newLan"] = "NA"
#for i in range(Title_Len):
#    csv["lan"][i]=str(csv["lan"][i])

#for w in range(Title_Len):
#     if "不拘" not in csv['lan'][w]:
#         key = csv['lan'][w]
#         p1 = "...--"
#         pattern1 = re.compile(p1)
#         reNet = str(pattern1.findall(key)).replace("，", "").replace(r"/", r"、").replace("'", "").replace(r"[",
#                                                                                                          "").replace(
#             r"]", "")
#         csv['newLan'][w] = reNet
#         csv['newLan'][w] = csv['newLan'][w].replace("--", '').replace(' ', '')
#     elif "不拘" in csv['lan'][w]:
#         csv['newLan'][w] = "不拘"
#     else:
#         csv['newLan'][w]=''
#csv["newSabisu"] = csv["sabisu"]
csv['brandAdv']=''
for i in range (Title_Len):
    if '行銷'  in csv['cName'][i]:
        csv['brandAdv'][i]='廣告商'
    elif '廣告' in csv['cName'][i]:
        csv['brandAdv'][i]='廣告商'
    elif '媒體' in csv['cName'][i]:
        csv['brandAdv'][i]='廣告商'
    elif '電視資訊有線公司' in csv['cName'][i]:
        csv['brandAdv'][i]='廣告商'
    else:
        csv['brandAdv'][i]='品牌商'

csv = csv[['title','cName','jobCont','jobLoc','category','vacation','workT','hireNum','empType','manage','busTrip','salary',
            'job_update','accept','workExp','edu','department','insurance','entertain','bonus',
            'contact','similar','jobRegion',
            'newJobLoc','furlough','newHireNum','newEmpType','newManage',
            'newBusTrip','monthSalary','hourSalary','otherSalary','workUpdate',
            'newWorkExp','newEdu','jobKey','humanBank','href','brandAdv']]

csv.to_csv('editor_yes123.csv')