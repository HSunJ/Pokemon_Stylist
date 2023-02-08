#image selector = #islrg > div.islrc > div:nth-child(2) > a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img
#search XPATH = /html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input

# 엔터키 사용 모듈
from selenium.webdriver.common.keys import Keys

import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import urllib.request


search = input("대상 입력 : ")

def makedirs(path):
	try:
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

URL = 'https://www.google.co.kr/imghp'
driver.get(url=URL)
# 로딩될 때 까지 최대 10초동안 대기
driver.implicitly_wait(time_to_wait=10)

keyElement = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input') # 검색창 선택
keyElement.send_keys(search) # 입력
keyElement.send_keys(Keys.RETURN) # 엔터

bodyElement = driver.find_element(By.TAG_NAME, 'body')
for i in range(20):
	# 0.2초마다 스크롤 다운
	bodyElement.send_keys(Keys.PAGE_DOWN)
	time.sleep(0.2)

# 검색 결과의 이미지들의 selector 저장
images = driver.find_elements(By.CSS_SELECTOR, '#islrg > div.islrc > div > a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img')

imageURL = []
for image in images:
	if image.get_attribute('src') is not None:
		# 이미지의 src태그의 주소 저장
		imageURL.append(image.get_attribute('src'))

# 이미지 저장
f_path = 'WebImage/'+search
makedirs(f_path)
for seq, img_url in enumerate(imageURL):
	# WebImage/이름/web_이름_0.jpg
	save_path = 'WebImage/'+search+'/web_'+search+'_'+str(seq)+'.jpg'
	urllib.request.urlretrieve(img_url, save_path)






