from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time
import os


# 초기화 함수
def init_chrome(URL):
	chrome_options = webdriver.ChromeOptions()
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
	driver.get(url=URL)
	# 로딩될 때 까지 최대 10초동안 대기
	driver.implicitly_wait(time_to_wait=10)
	return driver

# 로그인
def log_in_seq(driver):
	# 로그인 버튼 클릭
	log_in_button = driver.find_element(By.XPATH, '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div')
	log_in_button.click()
	driver.implicitly_wait(time_to_wait=2)
	# 아이디 입력
	keyElement = driver.find_element(By.XPATH, '//*[@id="email"]')
	keyElement.send_keys('gkstjswo12@naver.com')
	# 비밀번호 입력
	keyElement = driver.find_element(By.XPATH, '//*[@id="password"]')
	keyElement.send_keys('ishuer12')
	# 엔터
	keyElement.send_keys(Keys.RETURN)
	driver.implicitly_wait(time_to_wait=5)

# 페이지 스크롤
def search_target(bodyElement):
	for i in range(5):
	# 0.2초마다 스크롤 다운
		bodyElement.send_keys(Keys.PAGE_DOWN)
		time.sleep(0.4)

# 검색
def search_seq(target, driver):
	keyElement = driver.find_element(By.XPATH, '//*[@id="searchBoxContainer"]/div/div/div[2]/input') # 검색창 선택
	keyElement.send_keys(target) # 입력
	keyElement.send_keys(Keys.RETURN) # 엔터

def crawling(driver):
	bodyElement = driver.find_element(By.TAG_NAME, 'body')
	search_target(bodyElement)
	driver.implicitly_wait(time_to_wait=3)
	
	# 검색 결과의 이미지들의 selector 저장
	images = driver.find_elements(By.CSS_SELECTOR, '#__PWS_ROOT__ > div:nth-child(1) > div.appContent > div > div > div:nth-child(4) > div.zI7.iyn.Hsu > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div:nth-child(1) > a > div > div.zI7.iyn.Hsu > div > div > div > div > div > img')

	imageURL = []
	for image in images:
		if image.get_attribute('src') is not None:
			# 이미지의 src태그의 주소 저장
			imageURL.append(image.get_attribute('src'))
	return imageURL

def makedirs(path):
	try:
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise