# 해당파일은 mongoDB에서 직접 가져와서 전처리를 하면 과부하때문에 파일로 저장하기 위한 파일.
import re
from tqdm import tqdm
from db_info_load import MongoDBClient
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
import pandas as pd

class comeon_data:
    def __init__(self):
        self.client = MongoDBClient()
        self.database = self.client.get_database('musinsa_data')
    
class clear_data:  
    def __init__(self,df):
        self.df = df 

    # 리뷰전처리
    def processing_data(self,columns1,columns2,new_name):
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        self.df[new_name] = self.df[columns1].apply(lambda x : 1 if x>3 else 0)
        self.df[columns2] = self.df[columns2].apply(lambda x : re.sub(r'\d+[가-힣]+|[^가-힣 ]','', x))

        return self.df

    def split_data(self,columns1,columns2):
        X = self.df[columns1]
        y = self.df[columns2] 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y,random_state=42)
        return X_train, X_test, y_train, y_test


    def change(self):
        X_train, X_test, _, _ = self.split_data('review','index')
        okt = Okt()
        X_train_change = []
        X_test_change=[]

        for sentence in tqdm(X_train):
            temp_X = []
            temp_X = okt.morphs(sentence, stem=True)
            X_train_change.append(temp_X)

        for sentence in tqdm(X_test):
            temp_X = []
            temp_X = okt.morphs(sentence, stem=True)
            X_test_change.append(temp_X)

        return X_train_change,X_test_change,okt

# 아래코드는 mongoDB에서 데이터를 직접 가져와서 데이터프레임으로 만드는 코드
d=comeon_data()
temp_list = []
for i in d.database.find():
    temp_list.append(i)

musinsa_mongo_data = pd.DataFrame(temp_list)
musinsa_mongo_data.to_csv("version2/data/musinsa.csv", index = False)
