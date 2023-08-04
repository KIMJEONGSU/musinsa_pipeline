# 해당 파일의 코드는 네이버리뷰데이터를 csv파일로 불러와 모델학습진행.
# mongoDB에서 직접 불러오면 데이터베이스 부하를 줄 수 있기 때문에 위처럼 진행하였습니다.
import pickle
import pandas as pd
import re
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from about_DB.naver_data import NaverDataLoader
import pickle
from scikeras.wrappers import KerasClassifier 


def sentiment_predict(new_sentence, model):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣\s]','', new_sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = 25, padding='post') # 패딩
    score = float(model.predict(pad_new)) # 예측
    if(score > 0.5):
        return("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
    return("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))

okt = Okt()
tokenizer = Tokenizer()

musinsa = pd.read_csv('processing/about_DB/musinsa.csv')
musinsa_nlp = musinsa[['user_name','starss','review']][:10]

with open('processing/model/LSTM_model.pkl', 'rb') as f:
    model = pickle.load(f)
    musinsa_nlp['predict_result'] = musinsa_nlp['review'].apply(lambda x: sentiment_predict(str(x), model))
    musinsa_nlp['predict_result_persent'] = musinsa_nlp['predict_result'].apply(lambda x : float(re.sub(r'^([\d.]+).*\n*', r'\1', x)))
    musinsa_nlp['predict_result_review'] = musinsa_nlp['predict_result'].apply(lambda x : re.search(r'부정|긍정', x).group())
    musinsa_nlp.to_csv('musinsa_model_predict.csv', index=False)
    # mongo_store = NaverDataLoader('musinsa_predict')
    # documents = []
    # for row in tqdm(range(len(musinsa_nlp))):
    #     raw = {
    #         'user_name': musinsa_nlp['user_name'][row],
    #         'starss': int(musinsa_nlp['starss'][row]),
    #         'review' : musinsa_nlp['review'][row],
    #         'predict_result':musinsa_nlp['predict_result'][row],
    #         'predict_result_persent':musinsa_nlp['predict_result_persent'][row],
    #         'predict_result_review':musinsa_nlp['predict_result_review'][row]
    #     }
    #     documents.append(raw)
    # mongo_store.insert_many(documents)



