import math

from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By

xpath = {'login_button':'//*[@id="loginLi"]/a',
         'name':'//*[@id="root"]/div/form/div/div[1]/div/div/div/input',
         'password':'//*[@id="root"]/div/form/div/div[2]/div/div/div/input',
         'login_button_2':'//*[@id="root"]/div/form/div/div[3]/span',
         'advanced_search':'//*[@id="_view_1540966814000"]/div/div[1]/div[1]',
         'start_time':'//*[@id="cprqStart"]',
         'end_time':'//*[@id="cprqEnd"]',
         'search_button':'//*[@id="searchBtn"]',
         'sellect_all':'//*[@id="AllSelect"]',
         'download_all':'//*[@id="_view_1545184311000"]/div[2]/div[4]/a[3]',
         'next_page':'//*[@id="_view_1545184311000"]/div[8]/a['
         }
def run(start_time, end_time ,count):
    count = math.ceil(count / 5)
    #打开网页
    option = webdriver.ChromeOptions()
    if not os.path.isdir('zips'):
        os.mkdir('zips')
    path = os.path.abspath('zips')
    prefs = {"download.default_directory":path}
    option.add_experimental_option("prefs", prefs)
    # option.add_argument('--headless')
    url = 'https://wenshu.court.gov.cn/'
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe',chrome_options = option)
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    time.sleep(3)

    #登录
    print('login')
    driver.find_element(By.XPATH,xpath['login_button']).click()
    time.sleep(1)
    driver.refresh()
    time.sleep(4)
    driver.switch_to.frame('contentIframe')
    time.sleep(1)
    name = driver.find_element(By.XPATH,xpath['name'])
    name.send_keys('17796226836')
    time.sleep(1)
    password = driver.find_element(By.XPATH,xpath['password'])
    password.send_keys('.3024753855ws')
    time.sleep(1)
    driver.find_element(By.XPATH, xpath['login_button_2']).click()
    time.sleep(5)


    #搜索
    print('search')
    driver.find_element(By.XPATH,xpath['advanced_search']).click()
    time.sleep(5)
    driver.find_element(By.XPATH,xpath['start_time']).send_keys(start_time)
    time.sleep(2)
    driver.find_element(By.XPATH,xpath['end_time']).send_keys(end_time)
    time.sleep(2)
    driver.find_element(By.XPATH,xpath['search_button']).click()
    time.sleep(5)
    #下载
    print('download')
    index = 8
    for i in range(count):
        if i != 0:
            next_page = xpath['next_page']+str(index)+']'
            # print(next_page)
            driver.find_element(By.XPATH, next_page).click()
            time.sleep(5)
            if index < 14: index += 1
        else:
            driver.refresh()
        time.sleep(5)
        driver.find_element(By.XPATH, xpath['sellect_all']).click()
        time.sleep(3)
        driver.find_element(By.XPATH, xpath['download_all']).click()
        time.sleep(3)
        print(i+1)

if __name__ == '__main__':
    run('2020-05-05','2021-09-09',20)
