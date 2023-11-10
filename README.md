# 별점 5점인 부정 리뷰 감정 분석

<br>

### 프로젝트 기간
2023.03.09 ~ 2023.03.13

### 기술 스택
- Python
    - BeautifulSoup을 활용한 웹 스크래핑
    - sklearn, tensorflow, konlpy, pandas, wordcloud을 활용한 분석 및 시각화
- Docker: Metabase 사용을 위한 환경 구축
- MongoDB / Metabase


### 데이터 소개
<details>
<summary>무신사 데이터</summary>
<div markdown="1">

1. Data shape : 44383rows × 11 columns
2. 컬럼 소개
    
    
    | 컬럼 | 소개 | 컬럼 | 소개 |
    | --- | --- | --- | --- |
    | user_level | 사용자 레벨 | brand | 브랜드 |
    | user_name | 닉네임 | product | 제품 |
    | user_sex | 성별 | date | 날짜 |
    | user_height | 키 | starss | 별점 |
    | user_weight | 몸무게 | Review | 리뷰 |

</div>
</details>

<details>
<summary>네이버 쇼핑 데이터</summary>
<div markdown="1">

1. Data shape : 200000 rows × 2 columns
2. 컬럼 소개
    
    
    | 컬럼 | 소개 |
    | --- | --- |
    | rating | 별점 |
    | Review | 리뷰 |

</div>
</details>


### 파이프라인

![Untitled (5)](https://github.com/KIMJEONGSU/musinsa_pipeline/assets/23291338/03d9b0c7-641b-43ac-8b67-01b5c3e2d9de)

- `Docker` : MongoDB Atlas와 Metabase 간에 독립적인 환경이 생성되기 때문에 의존성이 줄어들고 서로의 환경에 영향을 미치지 않아 더 안정적이고 신뢰성있는 서비스 구축 가능.
- `MongoDB`
    - 리뷰 텍스트는 비정형 데이터이므로 다양한 유형의 데이터 저장이 가능한 MongoDB 선택.
    - 수평 확장이 쉽고, 빠른 읽기/ 쓰기 처리를 지원하기 때문에 대용량 데이터를 처리하는데 유리함.
