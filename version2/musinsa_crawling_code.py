# 해당파일은 무신사 리뷰홈페이지에서 크롤링한 후 몽고디비에 바로 적재하도록하는 코드
import requests
from bs4 import BeautifulSoup
from db_info_load import MongoDBClient
import re
import time
import schedule
import datetime


class MusinsaDataLoader():
    def __init__(self, month, day, collection_name):
        self.month = month
        self.day = day
        self.client = MongoDBClient()
        self.database = self.client.get_database(collection_name)
        print(f'현재 스크래핑 진행중인 날짜:{self.month}/{self.day}')

    def load_data(self, start, end):
        t_list = self.crawling(start, end)
        time.sleep(2)
        self.database.insert_many(t_list)

    def crawling(self,start, end):
        title_list=[]
        try:
            for num in range(start,end):
                start0 = time.time()
                time.sleep(2)
                url = f'https://www.musinsa.com/goods/reviews/lists?type=style&searchYear=2022&searchMonth={self.month}&searchDay={self.day}&maxRt=2023&minRt=2009&brand=&page={num}&sort=new&hashId=&bestType=&s_type=all&searchKeyword='
                req = requests.get(url)
                #get : request로 url의  html문서의 내용 요청
                html = requests.get(url,headers={"User-Agent" : "Mozilla/5.0"})
                #html을 받아온 문서를 .content로 지정 후 soup객체로 변환
                soup = BeautifulSoup(html.content,'html.parser')
                review_page = soup.find_all('div',class_='review-list')
                try:
                    for f in review_page:
                        user_level = f.select_one('p').text[3]
                        user_name = f.select_one('p').text[4:].strip()

                        user_i = f.select_one('div.review-profile__information').text
                        user_info = re.sub("[A-Za-z]|신고|·","",user_i).strip().split()

                        if user_info==[]:
                            user_info.extend(['모름',0,0])

                        user_sex = user_info[0]
                        user_height = user_info[1]
                        user_weight = user_info[-1]

                        brand = f.select_one('a.review-goods-information__brand').text
                        product = f.select_one('a.review-goods-information__name').text
                        time.sleep(2)
                        date = f.select_one('p.review-profile__date').text

                        stars_i = f.select_one('span.review-list__rating__active').get('style')
                        stars = re.sub("[^0-9]","",stars_i)
                        starss =  stars.replace('100','5').replace('80','4').replace('60','3').replace('40','2').replace('20','1')
                        review_i = f.select_one('div.review-contents__text').text
                        review = re.sub("[^가-힣 ]","",review_i)

                        musinsa1={'user_level': user_level, 'user_name': user_name,'user_sex': user_sex,
                                'user_height': user_height,'user_weight': user_weight,'brand': brand,
                                'product': product,'date': date,'starss': starss,
                                'review': review}
                        title_list.append(musinsa1)
                except :
                    musinsa1={'user_level': None, 'user_name': None,'user_sex': user_sex,
                                'user_height': user_height,'user_weight': user_weight,'brand': brand,
                                'product': product,'date': date,'starss': starss,
                                'review': review}
                    title_list.append(musinsa1)
                end0 = time.time()
                print(f"페이지수:{num} / 실행시간 : {end0 - start0:.5f} sec") # 실행 시간 출력

        except Exception as e:
            print(f"Error occurred: {e}")
            pass
        return title_list
    
def load_data_and_schedule(start, end):
    for i in range(1, 13): # 1월부터 12월 크롤링
        Musinsa = MusinsaDataLoader(i, 2, 'musinsa_data') # 2번째 인자값은 day
        time.sleep(10)
        Musinsa.load_data(start, end)  # 크롤링할 페이지 입력
        
if __name__ == '__main__':
    now = datetime.datetime.now()
    print("현재시간 :",now)
    schedule.every(5).minutes.do(load_data_and_schedule(151, 153)) #월, 일, 데이터베이스이름 입력

    # 스캐쥴 시작
    while True:
        schedule.run_pending()
        time.sleep(10)
        
        

# 2023.04.29 
# 1/1/1~101,150
# 2/1/1~101,150
# 3/1/1~101,150
# 4/1/1~101,150
# 5/1/1~101,150
# 6/1/1~101,150
# 7/1/1~101,150
# 8/1/1~101,150
# 9/1/1~101,150
# 10/1/1~101,150
# 11/1/1-101,150
# 12/1/1-101,150