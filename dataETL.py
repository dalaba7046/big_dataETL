import pandas as pd

df_a=pd.read_csv('./a_lvr_land_a.csv')
df_b=pd.read_csv('./b_lvr_land_a.csv')
df_e=pd.read_csv('./e_lvr_land_a.csv')
df_f=pd.read_csv('./f_lvr_land_a.csv')
df_h=pd.read_csv('./h_lvr_land_a.csv')

#將讀取完的dataframe變成一個list之後方便合併
df_lists=[df_a,df_b,df_e,df_f,df_h]
#為之後需要分析的目標設定一個空的dataframe
df_all=pd.DataFrame()
#合併5個dataframe為1個
df_all=pd.concat(df_lists,ignore_index=True)
#計算資料長度
total=len(df_all['鄉鎮市區'])
#整理資料 將樓層總數準備轉為阿拉伯數字
for i in range(total):
    df_all['總樓層數'][i]=str(df_all['總樓層數'][i])
    if 'total floor number' in df_all['總樓層數'][i]:
        df_all['總樓層數'][i]='零'
    elif '層' in df_all['總樓層數'][i]:
        df_all['總樓層數'][i]=df_all['總樓層數'][i].replace('層','')
    elif 'nan' in df_all['總樓層數'][i]:
        df_all['總樓層數'][i]='零'

#下面將中文大寫轉為阿拉伯數字設定
CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
}

CN_UNIT = {
    '十' : 10,
    '拾' : 10,
    '百' : 100,
    '佰' : 100,
    '千' : 1000,
    '仟' : 1000,
    '万' : 10000,
    '萬' : 10000,
    '亿' : 100000000,
    '億' : 100000000,
    '兆' : 1000000000000,
}

def chinese_to_arabic(cn:str) -> int:
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

#將樓層整數欄位轉為阿拉伯數字
x=[]

for cn in df_all['總樓層數']:
    x.append(chinese_to_arabic(cn))
#x=pd.DataFrame(x)
for j in range(total):
    df_all['總樓層數'][j]=x[j]
#將住宅大樓欄位內容綁定
for k in range(total):
    if '住宅大樓' in df_all['建物型態'][k]:
        df_all['建物型態'][k]='住宅大樓'
#下達篩選條件輸出csv
filter_a=df_all[(df_all['主要用途']=='住家用')&(df_all['建物型態']=='住宅大樓')&(df_all['總樓層數']>=13)]
filter_a.to_csv('filter_a.csv')

'''
filter_b.csv資料集建立
'''
#進行資料二次整理
df_a=df_a.drop(index=0)
df_b=df_b.drop(index=0)
df_e=df_e.drop(index=0)
df_f=df_f.drop(index=0)
df_h=df_h.drop(index=0)

df_lists=[df_a,df_b,df_e,df_f,df_h]
#為之後需要分析的目標設定一個空的dataframe
df_all=pd.DataFrame()
#合併5個dataframe為1個
df_all=pd.concat(df_lists,ignore_index=True)
#計算總件數
total=len(df_all)
#將車位資料提取
df_all['車位']=''
for l in range(total):
    df_all['車位'][l]=int(df_all['交易筆棟數'][l][-1])
#計算車位數量
car_sum=df_all['車位'].sum()

#計算平總價元
for m in range(total):
    df_all['總價元'][m]=int(df_all['總價元'][m])
avg_total=df_all['總價元'].mean()
#計算平均車位總價元
for n in range(total):
    df_all['車位總價元'][n]=int(df_all['車位總價元'][n])
avg_cartotal=df_all['車位總價元'].mean()

Dict={
      '總件數':[total],
      '總車位數':[car_sum],
      '平均總價元':[avg_total],
      '平均車位總價元':[avg_cartotal]
      }
filter_b=pd.DataFrame(Dict).round(2)
filter_b.to_csv('filter_b.csv')
