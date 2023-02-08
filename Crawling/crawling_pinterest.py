from functions import *

import argparse
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--name', required=True, help='Select Crawling Target')
args = vars(ap.parse_args())

search = args['name']

URL = 'https://www.pinterest.co.kr/'
seq = 1

driver = init_chrome(URL)

# 로그인
log_in_seq(driver)
# 검색
target = search+' drawing'
search_seq(target, driver)

for i in range(5):
	# 검색한 이미지들의 주소를 저장
	imageURL = crawling(driver)

	# 이미지 저장
	f_path = 'WebImage/'+search
	makedirs(f_path)
	for img_url in imageURL:
		# WebImage/이름/web_이름_1.jpg
		save_path = 'WebImage/'+search+'/web_'+search+'_'+str(seq)+'.jpg'
		urllib.request.urlretrieve(img_url, save_path)
		seq += 1



