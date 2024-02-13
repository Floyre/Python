import requests
import os
import time
from selenium import webdriver as webdriver #Selenium
from selenium.webdriver.chrome.options import Options #Selenium Options / Headless, Disable Logs
from selenium.webdriver.common.keys import Keys #Selenium Key Input
from urllib.request import urlretrieve

# Selenium WebDriver 관련 설정값
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument('--hide-scrollbars')
options.add_argument("--log-level=3")  # Log Only FATAL info = 3
options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Suppress Console Logs
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)  # WebDriver Location

def createFolder(directory): #폴더 생성 함수
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('디렉터리 생성에 오류가 발생했습니다. 해당 디렉터리 : ' +  directory)

emojiurl_list = []
emoji_path = input('긁어올 카카오톡 이모티콘 판매 사이트 링크를 입력해주세요 : ')
driver.get(emoji_path) #입력받은 이모티콘 판매 사이트에 접속

body = driver.find_element_by_tag_name("body") #PageDown을 통해 페이지 전체 이모티콘 로딩
for num in range(0,5):
    body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)

title =([e.text for e in driver.find_elements_by_xpath('//*[@id="kakaoContent"]/div[1]/div[2]/h3/span')])
print('이모티콘의 이름 :',title[0])
createFolder(title[0]) #이모티콘 판매 페이지에 있는 제목 / 리스트에 들어가버려서 리스트의 첫번쨰 값이라 지정해줘야 str로 나옴
count = -3 #이모티콘 판매 페이지에 있는 4개의 광고, 이모티콘 썸네일을 제외시키기 위한 변수
img = driver.find_elements_by_tag_name("img")
advertisement = "17ea012db208c" #유저가 크롤링을 원하는 이모티콘이 아닌, 다른 추천 이모티콘의 썸네일 주소 중 일부
for item in img:
    if(count <=  0):
        count = count+1
        continue
    if(count >= 1 and count < 100): #이모티콘의 원본 주소'만'(img src) 포함 된 클래스나 Xpath의 개수(size())를 파악하여 단순 무작위 반복이 아닌 정해진 개수만큼 루프를 돌릴 수 있지만 귀찮아서 거기까지는 구현하지 않음
        emoji_url = item.get_attribute('src')
        if advertisement in emoji_url: #만약 페이지에서 크롤링된 이미지 주소에 '추천 이모티콘'의 주소가 포함되있다면 리스트에 추가하지 않고 스킵한다
            continue
        else:
            emojiurl_list.append(emoji_url) 

for index, value in enumerate(emojiurl_list):
    print(index+1,'번째 이모티콘 주소 : ', value)
    urlretrieve(value, './{}/{}{}'.format(title[0],index+1, '.png')) 
print('작업이 완료되었습니다.')