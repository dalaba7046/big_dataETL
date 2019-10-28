dataETL.py是處理時價登陸平台資料
程式會匯出2個檔案filter_a.csv和filter_b.csv

filter_a.csv內容包含篩選條件為以下標準的資料:
-【主要用途】為【住家用】
-【建物型態】為【住宅大樓】
-【總樓層數】需【大於等於十三層】

filter_b.csv內容包含以下計算條件的資料:
- 計算【總件數】
- 計算【總車位數】(透過交易筆棟數)
- 計算【平均總價元】
- 計算【平均車位總價元】

591tai_pei.py和591tai_pei.py為租屋網爬蟲並將資料匯入mongoDB
DB內部資料表具有下列欄位:
- 出租者 (陳先生)
- 出租者身份 (屋主)
- 聯絡電話 (02-25569419)
- 型態 (電梯大樓)
- 現況 (獨立套房)
- 性別要求 (男女生皆可)
