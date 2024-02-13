import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#셀레니움 크롬 웹드라이버 옵션 설정
options = webdriver.ChromeOptions()
#options.add_argument('headless') #프로그램 실행 시 크롬 창 안나오게 하기(백그라운드)
options.add_argument("disable-gpu")
options.add_argument('--hide-scrollbars')
options.add_argument("--log-level=3")  #Level 3문제만 로그에 기록하기
options.add_experimental_option("excludeSwitches", ["enable-logging"]) #콘솔 로그 막기

#Main.ui location
form_class = uic.loadUiType("dr_ui\main.ui")[0]
#Checkbox Checker Variables
google_doeschecked = 0
naver_doeschecked = 0
daum_doeschecked = 0
zum_doeschecked = 0
nate_doeschecked = 0
bing_doeschecked = 0
dcinside_doeschecked = 0
yahoo_doeschecked = 0
duck_doeschecked = 0
twitter_doeschecked = 0
facebook_doeschecked = 0
instagram_doeschecked = 0
tistory_doeschecked = 0
howmanytabs = 0
class main_window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchbtn.clicked.connect(self.chkbox_state)
        self.searchbtn.clicked.connect(self.Result_Func)
        self.searchbox.returnPressed.connect(self.chkbox_state) #QLineEdit에서 편집 후 엔터를 눌러도 SEARCH 버튼과 똑같이 동작하게 함
        self.searchbox.returnPressed.connect(self.Result_Func)
        howmanytabs = 0

    def chkbox_state(self): #Checkbox Status Checker
        #체크박스 확인용 함수들을 전역변수 처리하여 다른 창(클래스)에서도 접근 가능하게 함
        global google_doeschecked
        global naver_doeschecked
        global daum_doeschecked
        global zum_doeschecked
        global nate_doeschecked
        global bing_doeschecked
        global dcinside_doeschecked
        global yahoo_doeschecked
        global duck_doeschecked
        global twitter_doeschecked
        global facebook_doeschecked
        global instagram_doeschecked
        global tistory_doeschecked
        global search_keyword
        global howmanytabs

        search_keyword = self.searchbox.text() #searchbox(QLineEdit)에 있는 내용을 search_keyword 변수에 할당
        print('KEYWORD :', search_keyword) 

        if (self.google.isChecked()): #Google
            google_doeschecked = 1
            howmanytabs += 1
        else:
            google_doeschecked = 0
        if (self.naver.isChecked()): #Naver
            naver_doeschecked = 1
            howmanytabs += 1
        else:
            naver_doeschecked = 0
        if(self.daum.isChecked()): #Daum
            daum_doeschecked = 1
            howmanytabs += 1
        else:
            daum_doeschecked = 0
        if(self.zum.isChecked()): #Zum
            zum_doeschecked = 1
            howmanytabs += 1
        else:
            zum_doeschecked = 0
        if(self.nate.isChecked()): #Nate
            nate_doeschecked = 1
            howmanytabs += 1
        else:
            nate_doeschecked = 0
        if(self.bing.isChecked()): #Bing
            bing_doeschecked = 1
            howmanytabs += 1
        else:
            bing_doeschecked = 0
        if(self.dcinside.isChecked()): #DCinside
            dcinside_doeschecked = 1
            howmanytabs += 1
        else:
            dcinside_doeschecked = 0
        if(self.yahoo.isChecked()): #Yahoo
            yahoo_doeschecked = 1
            howmanytabs += 1
        else:
            yahoo_doeschecked = 0
        if(self.duckduckgo.isChecked()): #DuckDuckGO
            duck_doeschecked = 1
            howmanytabs += 1
        else:
            duck_doeschecked = 0
        if(self.twitter.isChecked()): #Twitter
            twitter_doeschecked = 1
            howmanytabs += 1
        else:
            twitter_doeschecked = 0
        if(self.facebook.isChecked()): #Facebook
            facebook_doeschecked = 1
            howmanytabs += 1
        else:
            facebook_doeschecked = 0
        if(self.instagram.isChecked()): #Instagram
            instagram_doeschecked = 1
            howmanytabs += 1
        else:
            instagram_doeschecked = 0
        if(self.tistory.isChecked()): #Tistory
            tistory_doeschecked = 1
            howmanytabs += 1
        else:
            tistory_doeschecked = 0

    def Result_Func(self):
        result_window(self)
class result_window(QMainWindow):
    def __init__(self, parent):
        super(result_window, self).__init__(parent)
        uic.loadUi("dr_ui\search_result.ui", self)
        #self.show()
        #구현해야되는거 프로그램 2번째 런 했을때 기존에 열려있는 탭 전부 닫고 다시 열어주는거
        global howmanytabs
        driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)  #웹드라이버 파일 위치
        print('열어야 되는 탭 개수 : ',howmanytabs)
        for i in range(howmanytabs-1):
            driver.execute_script('window.open("about:blank", "_blank");')
        tabs = driver.window_handles
        taskedtabs = 0 #활성화 & 처리 완료된 탭 개수
        if(google_doeschecked == 1): #Google 검색 체크박스 활성화 되있을 시
            driver.get('https://www.google.com/')
            google_search = driver.find_element_by_name('q')
            google_search.send_keys(search_keyword)
            google_search.submit()
            taskedtabs +=1
        if(naver_doeschecked == 1): #Naver 검색 체크박스 활성화 되어있을 시
            if(howmanytabs>1):
                driver.switch_to_window(tabs[taskedtabs])
                driver.get('https://www.naver.com/')
                naver_search = driver.find_element_by_name('query')
                naver_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="search_btn"]').click() #검색버튼 클릭
                taskedtabs +=1
            else:
                driver.get('https://www.naver.com/')
                naver_search = driver.find_element_by_name('query')
                naver_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="search_btn"]').click() #검색버튼 클릭
        if(daum_doeschecked == 1):
            if(howmanytabs>1):
                driver.switch_to_window(tabs[taskedtabs])
                driver.get('https://www.daum.net/')
                daum_search =  driver.find_element_by_name('q')
                daum_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="daumSearch"]/fieldset/div/div/button[2]').click() #검색버튼 클릭
                taskedtabs +=1
            else:
                driver.get('https://www.daum.net/')
                daum_search =  driver.find_element_by_name('q')
                daum_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="daumSearch"]/fieldset/div/div/button[2]').click() #검색버튼 클릭
        if(zum_doeschecked == 1):
            if(howmanytabs>1):
                driver.switch_to_window(tabs[taskedtabs])
                driver.get('https://zum.com/')
                zum_search =  driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div/fieldset/div/input')
                zum_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div/fieldset/div/button[2]').click() #검색버튼 클릭
                taskedtabs +=1
            else:
                driver.get('https://zum.com/')
                zum_search =  driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div/fieldset/div/input')
                zum_search.send_keys(search_keyword)
                driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div/fieldset/div/button[2]').click() #검색버튼 클릭
            if(nate_doeschecked == 1):
                if(howmanytabs >1):
                    driver.switch_to_window(tabs[taskedtabs])
                    driver.get('https://www.nate.com/')
                    nate_search = driver.find_element_by_name('q')
                    nate_search.send_keys(search_keyword)
                    driver.find_element_by_xpath('//*[@id="acBtn"]').click()
                    taskedtabs +=1
                else:
                    print('not workding') #Nate 버그 있음 작동이 안됨
                    driver.get('https://www.nate.com/')
                    nate_search = driver.find_element_by_name('q')
                    nate_search.send_keys(search_keyword)
                    driver.find_element_by_xpath('//*[@id="acBtn"]').click()
        print('jobs done')
        howmanytabs = 0
app = QApplication(sys.argv)
mainWindow = main_window()
mainWindow.show()
app.exec()