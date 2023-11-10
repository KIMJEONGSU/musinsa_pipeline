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
