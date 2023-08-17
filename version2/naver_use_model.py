# 해당 파일의 코드는 네이버리뷰데이터를 csv파일로 불러와 모델학습진행.
# mongoDB에서 직접 불러오면 데이터베이스 부하를 줄 수 있기 때문에 위처럼 진행하였습니다.
import numpy as np
import pandas as pd
import re
import csv
import pickle
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.metrics import AUC


# 네이버데이터파일 불러오기
with open('version2/data/naver_shopping.txt', 'r', encoding='utf-8') as f:
    naver = csv.reader(f)
    df = pd.DataFrame([sentence[0].split('\t') for sentence in naver], columns=['rating', 'review'])

    # 전처리
    df['rating'] = df['rating'].apply(lambda x : 1 if int(x)>3 else 0)
    df['review'] = df['review'].apply(lambda x : re.sub(r'\d+[가-힣]+|[^가-힣 ]','', x))
    df['review'] = df['review'].apply(lambda x : re.sub(r'[^가-힣 ]','', x))
    X_train, X_test, y_train, y_test = train_test_split(df['review'], df['rating'], test_size=0.2, random_state=42)
    
    # 형태소분석
    okt = Okt()
    X_train_okt = []
    X_test_okt=[]

    for sentence in tqdm(X_train):
        temp_X = okt.morphs(sentence, stem=True)
        X_train_okt.append(temp_X)
    for sentence in tqdm(X_test):
        temp_X = okt.morphs(sentence, stem=True)
        X_test_okt.append(temp_X)

    # 불용어 제거
    stopwords = ['가', '이', '을', '를', '에', '에서', '이나', '나', '의', '과', '와', 
                 '도', '만', '까지', '부터', '저', '나', '너', '우리', '그들', '그녀', 
                 '이들', '저희', '내', '제', '모두', '이', '그', '저', '모든', '모두', 
                 '어떤', '어느', '한', '또한', '다른', '같은', '비슷한', '입니다', '입니다.', 
                 '있습니다', '있습니다.', '합니다', '합니다.', '드립니다', '드립니다.', '입니다!', 
                 '있습니다!', '합니다!', '드립니다!','것']

    X_train_clean = []
    for sentence in X_train_okt:
        temp_X = [word for word in sentence if not word in stopwords]     
        X_train_clean.append(temp_X)
        
    X_test_clean = []
    for sentence in X_test_okt:
        temp_X = [word for word in sentence if not word in stopwords]     
        X_test_clean.append(temp_X)

    # 토큰화, 패딩
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train_clean)
    X_encoded = tokenizer.texts_to_sequences(X_train_clean)
    X_encoded_test = tokenizer.texts_to_sequences(X_test_clean)

    X_data=pad_sequences(X_encoded, maxlen=25, padding='post')
    X_data_test=pad_sequences(X_encoded_test, maxlen=25, padding='post')

    y_train=np.array(y_train)
    y_test=np.array(y_test)

# 모델 구현
def model_LSTM(X_train, y_train, tokenizer):
    embedding_dim = 100
    hidden_units = 128
    vocab_size = len(tokenizer.word_index)+1


    model_lstm = Sequential()
    model_lstm.add(Embedding(vocab_size, embedding_dim))
    model_lstm.add(LSTM(hidden_units))
    model_lstm.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', 
                    mode='min', 
                    verbose=1, 
                    patience=4)
    # recall_m, precision_m, f1_m
    model_lstm.compile(loss='binary_crossentropy', 
                optimizer='adam', 
                metrics=['acc', AUC()])

    # history_lstm = model_lstm.fit(X_train, 
    #                 y_train, 
    #                 epochs=10, 
    #                 callbacks=[es], 
    #                 batch_size=64, 
    #                 validation_split=0.2)
    return model_lstm

# 모델학습 및 피클링
model = model_LSTM(X_data, y_train, tokenizer)
with open('version2/model/LSTM.pkl','wb') as pickle_file:
    pickle.dump(model,pickle_file)


