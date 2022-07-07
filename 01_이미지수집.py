from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import  pyautogui , time , os , re
import urllib.parse as rep
import urllib.request as req
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests as rq
from bs4 import BeautifulSoup as bs
from typing import Union

class ChromeDriver:
    def set_driver(self):
        # options 객체 생성
        chrome_options = Options()

        # headless chrome
        # chrome_options.add_argument('--headless')

        # 브라우저 꺼짐 방지
        chrome_options.add_experimental_option('detach', True)

        # 불필요한 에러메시지 제거
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Service 객체
        service = Service(executable_path=ChromeDriverManager().install())

        # driver 객체
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.maximize_window()

        return browser

class Application:
    def __init__(self):
        # ChromeDriver 객체 생성
        self.chromedriver = ChromeDriver()

        # set_driver 메서드 실행 후 , 리턴 값 멤버변수로 정의
        self.browser  = self.chromedriver.set_driver()

        # header 정보
        self.headers : dict = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36'
                        }

        # input_keword 메소드의 return 데이터 인스턴스 변수로 정의
        self.keword : str =  self.input_keword()

        # quote 처리
        self.quote_keword : str = rep.quote_plus(self.keword)

        # url 지정
        self.url : list = [
            f'https://www.google.com/search?q={self.quote_keword}&sxsrf=ALiCzsbpRs1qtKCvEy4evEWVZlI-BbJy7A:1655885757552&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiH-PeSz8D4AhUUx2EKHdd4AdEQ_AUoAXoECAIQAw&biw=1874&bih=978&dpr=1'
        ]

    def run(self):
        # 브라우저 이동
        self.browser.get(url=self.url[-1])
        self.browser.implicitly_wait(15)

        # 스크롤 이동
        self.scroll()

        # 데이터 파싱
        self.parsing()


    def parsing(self) -> None:
        # 이미지 증가 카운트 인스턴스 변수로 정의
        count : int = 1

        # 게시글 리스트 추출
        content_list = self.browser.find_elements(By.CSS_SELECTOR,'.rg_i.Q4LuWd')

        for content in content_list :
            # 첫 번째 게시글 부터 차례대로 클릭
            self.browser.execute_script('arguments[0].click()',content)
            time.sleep(0.5)

            try :
                imgUrl : Union[list,str] = self.browser.find_elements(By.CSS_SELECTOR,'img.n3VNCb')
                if len(imgUrl) == 2 :
                    imgUrl : str = imgUrl[0].get_attribute('src')
                    if 'data:' in str(imgUrl) :
                        continue
                elif len(imgUrl) == 3:
                    imgUrl : str = imgUrl[1].get_attribute('src')
                    if 'data:' in str(imgUrl):
                        continue
                else :
                    continue

                # 이미지 다운로드
                self.download_iamge(imgUrl=imgUrl , count=count)

                # 이미지 카운트번호 증감
                count += 1
            except :
                continue

    def download_iamge(self,imgUrl : str , count : int) -> None:
        # 이미지 파일 저장 위치 지정
        img_save_path : str = os.path.abspath(f"{self.keword}")
        if not os.path.exists(img_save_path) :
            os.mkdir(img_save_path)

        # 이미지 파일명 지정
        img_filename = os.path.join(img_save_path,f'{count}.jpg')
        print(f"{img_filename}\n")

        # 이미지 다운로드
        download_file = rq.get(imgUrl,headers=self.headers,verify=False)

        with open(img_filename,'wb') as photo :
            photo.write(download_file.content)

    # 스크롤 내림 메서드 정의
    def scroll(self) -> None:
        prev_height : int = self.browser.execute_script("return document.documentElement.scrollHeight")

        while True :
            # 더 보기 버튼 클릭
            more_btn = self.browser.find_element(By.CSS_SELECTOR, 'input.mye4qd')
            self.browser.execute_script('arguments[0].click()',more_btn)
            time.sleep(1.5)

            # 스크롤 내리기
            self.browser.execute_script("window.scrollTo(0 , document.documentElement.scrollHeight)")

            # 대기시간 할당하기
            time.sleep(2)

            # 새로운 높이 값 받기
            curr_height : int = self.browser.execute_script("return document.documentElement.scrollHeight")

            # 이전 높이가 현재 높이와 같은경우 더보기 버튼 클릭
            if curr_height == prev_height :
                break

            prev_height : int = curr_height


    # 키워드 입력 메소드 정의
    def input_keword(self) -> str:
        os.system('cls')
        while True :
            keword : str = input('원하시는 키워드명을 입력해주세요\n\n:')
            if not keword :
                pyautogui.alert('키워드가 입력되지 않았습니다!')
                os.system('cls')
                continue
            else :
                return keword



if __name__ == '__main__':
    app = Application()

    app.run()

