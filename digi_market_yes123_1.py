from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import requests


urls='https://www.yes123.com.tw/admin/index.asp'
options = webdriver.ChromeOptions()
options.add_argument("Connection=close")
#options.add_argument('--headless')
driver=webdriver.Chrome(executable_path="/Users/liuyukun/python/chromedriver",chrome_options=options)
driver.get(urls)
time.sleep(10)

soup = bs(driver.page_source, 'html.parser')

inputElement = driver.find_element_by_id("find_key1")
inputElement.send_keys("數位社群行銷")
inputElement.submit()
time.sleep(10)

#爬職缺網址存成txt
with open ('digi_market.txt','w') as li:
    soup = bs(driver.page_source, 'html.parser')
    links=soup.find_all('a',class_='jobname')
    job_home="https://www.yes123.com.tw/admin/"
    jobUrl=[]
    x=1
    while x == 1 :
        for i in links:
            lin=i.get("href")
            lin=str(lin)
            if "job_refer_comp" in lin:
                 job=job_home+lin
                 jobUrl.append(str(job))
            li.writelines(job)
            li.writelines('\n')
        try:
            driver.find_element_by_class_name('next').send_keys(Keys.ENTER)
            time.sleep(5)

        except NoSuchElementException:
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            driver.quit()
            break
