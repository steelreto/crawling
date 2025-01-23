from google_play_scraper import reviews_all, Sort
import pandas as pd

# '트릭컬 리바이브' 앱의 패키지 이름
app_package_name = 'com.epidgames.trickcalrevive'

# 모든 리뷰 가져오기
reviews = reviews_all(
    app_package_name,
    lang='ko',  # 한국어 리뷰
    country='kr',  # 한국 스토어
    sort=Sort.NEWEST  # 최신순으로 정렬
)

# 데이터프레임으로 변환
df = pd.DataFrame(reviews)
df.shape

df.head()

# 필요한 컬럼만 선택
df = df[['userName', 'score', 'at', 'content']]

df.head(20)

# CSV 파일로 저장 (escapechar와 quoting 추가)
df.to_csv(
    'trickcal_revive_reviews.csv',
    index=False,
    encoding='utf-8-sig',
    quoting=1,  # 항상 큰따옴표로 감싸기
    escapechar='\\'  # 특수 문자 이스케이프
)

import pandas as pd

# 'trickcal_revive_reviews.csv' 파일 읽기
df = pd.read_csv('trickcal_revive_reviews.csv', encoding='utf-8-sig')




# score가 4 또는 5인 행 필터링
filtered_df = df[df['score'].isin([4, 5])]

# content 컬럼 체크 및 context_45 생성
if 'content' in filtered_df.columns and not filtered_df.empty:
    context_45 = ' '.join(filtered_df['content'].dropna())
else:
    context_45 = ''
    print("content 컬럼이 없거나 데이터가 비어 있습니다.")

# context_45 확인
if context_45:
    print("context_45 내용:", context_45[:100])  # 처음 100자 출력
else:
    print("context_45가 비어 있습니다.")

from collections import Counter
from konlpy.tag import Okt

# 형태소 분석기 초기화
okt = Okt()

# 텍스트에서 명사 추출
nouns = okt.nouns(context_45)

# 단어 빈도 계산
word_counts = Counter(nouns)

print(word_counts)
print("단어 개수:", len(word_counts))

from collections import Counter
from konlpy.tag import Okt

# 형태소 분석기 초기화
okt = Okt()

# 테스트를 위한 출력
print("분석할 텍스트:", context_45[:100])  # 텍스트의 처음 100자만 출력

# 텍스트에서 명사 추출
nouns = okt.nouns(context_45)
print("추출된 명사 수:", len(nouns))
print("추출된 명사 예시:", nouns[:10])  # 처음 10개의 명사만 출력

# 단어 빈도 계산
word_counts = Counter(nouns)
print("단어 빈도 상위 10개:", word_counts.most_common(10))

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def create_korean_wordcloud(word_counts):
    """
    window의 기본 한글 폰트를 사용하여 워드클라우드를 생성하는 함수
    
    Parameters:
    word_counts (Counter): 단어 빈도수 Counter 객체
    """
    
    # window의 기본 한글 폰트 경로
    font_path = 'C:\Windows\Fonts\malgun.ttf'
    
    # WordCloud 생성
    wc = WordCloud(
        font_path=font_path,  # 폰트 경로
        width=800,  # 가로 크기
        height=400,  # 세로 크기
        background_color='white',  # 배경색
        max_words=200,  # 최대 단어 수
        max_font_size=100,  # 최대 글자 크기
        min_font_size=10,  # 최소 글자 크기
        random_state=42,  # 랜덤 시드 고정
    )
    
    # Counter 객체를 딕셔너리로 변환하여 워드클라우드 생성
    wc.generate_from_frequencies(dict(word_counts))
    
    # 그래프 크기 설정
    plt.figure(figsize=(10, 8))
    
    # 워드클라우드 출력
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 축 제거
    
    # 그래프 출력
    plt.show()
    
    # 워드클라우드 이미지 저장
    wc.to_file('wordcloud_result.png')
    print("워드클라우드가 'wordcloud_result.png'로 저장되었습니다.")

# 워드클라우드 생성 실행
create_korean_wordcloud(word_counts)