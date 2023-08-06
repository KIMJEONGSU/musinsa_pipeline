# naver데이터 DB에 적재
# https://cloud.mongodb.com/v2/643ccaad61e6283573beb739#/clusters
# 해당 파일은 모델용 학습 데이터를 몽고디비에 적재하기 위한 코드입니다.

import csv
from pymongo import MongoClient
from tqdm import tqdm
import json
import urllib.parse


class MongoDBClient:
    def __init__(self):
        self.host = 'cluster0.w3ampdj.mongodb.net'
        self.user = 'text_sentiment'
        self.password = self._load_password()
        self.database_name = 'data'
        self.client = MongoClient(self._mongo_uri())
        

    def _mongo_uri(self):
        return f"mongodb+srv://{self.user}:{self.password}@{self.host}/{self.database_name}?retryWrites=true&w=majority"

    def get_database(self, collection_name):
        return self.client[self.database_name][collection_name]
    
    def _load_password(self):
        with open('version2/password.json') as f:
            data = json.load(f)
            print(data.get('password'))
            return data.get('password')

class NaverDataLoader:
    def __init__(self, collection_name,db_filepath=None):
        self.collection_name = collection_name
        self.client = MongoDBClient()
        self.database = self.client.get_database(collection_name)
        if db_filepath is not None:
            self.db_filepath = db_filepath

    def insert_many(self, documents):
        collection = self.database[self.collection_name]
        collection.insert_many(documents)
        
    def load_data(self):
        self.database.drop()

        # 예측 모델을 만들기 위한 데이터셋 적재.
        # with open('naver_shopping.txt', 'r', encoding='utf-8') as f:
        #     naver = csv.reader(f)

        #     documents = []
        #     for row in tqdm(naver):
        #         raw = {
        #             'rating': int(row[0][0]),
        #             'review': row[0][1:].strip(),
        #         }
        #         documents.append(raw)
        #     #bulk insert를 사용하여 대량 데이터 빠르게 삽입.
        #     self.database.insert_many(documents)

        
        with open('version2/data/musinsa_model_predict.csv', 'r', encoding='utf-8') as f:
            musinsa = csv.reader(f)
            documents = []
            for row in tqdm(musinsa):
                raw = {
                    'user_name': row[0],
                    'starss': row[1],
                    'review' : row[2],
                    'predict_result':row[3],
                    'predict_result_persent':row[4],
                    'predict_result_review':row[5]
                }
                documents.append(raw)
            #bulk insert를 사용하여 대량 데이터 빠르게 삽입.
            self.database.insert_many(documents)


if __name__ == '__main__':

    # 예측 모델을 만들기 위한 데이터셋 적재.
    # loader = NaverDataLoader('naver_data','naver_shopping.txt')
    # loader.load_data()
    loader = NaverDataLoader('musinsa_predict','version2/data/musinsa_model_predict.csv')
    loader.load_data()
