from google_play_scraper import reviews_all, Sort
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 리버스1999 앱 패키지 이름
app_package_name = 'kr.haoplay.game.and.reverse'


# 2. 모든 리뷰 가져오기
reviews = reviews_all(
    app_package_name,
    lang='ko',  # 한국어 리뷰
    country='kr',  # 한국 스토어
    sort=Sort.NEWEST  # 최신순으로 정렬
)

# 3. 데이터프레임으로 변환
df = pd.DataFrame(reviews)

# 4. 필요한 컬럼만 선택
df = df[['userName', 'score', 'at', 'content']]

# 5. CSV 파일로 저장
df.to_csv(
    'reverse1999_reviews.csv',
    index=False,
    encoding='utf-8-sig',
    quoting=1,
    escapechar='\\'
)

# 6. 긍정 리뷰 필터링 (4점, 5점)
filtered_df = df[df['score'].isin([4, 5])]

# 7. 리뷰 텍스트 통합
if 'content' in filtered_df.columns and not filtered_df.empty:
    context_45 = ' '.join(filtered_df['content'].dropna())
else:
    context_45 = ''
    print("content 컬럼이 없거나 데이터가 비어 있습니다.")

# 8. 형태소 분석 및 단어 빈도 계산
okt = Okt()
nouns = okt.nouns(context_45)
word_counts = Counter(nouns)

# 9. 워드클라우드 생성 함수
def create_korean_wordcloud(word_counts):
    font_path = 'C:\Windows\Fonts\malgun.ttf'
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color='white',
        max_words=200,
        max_font_size=100,
        min_font_size=10,
        random_state=42,
    )
    wc.generate_from_frequencies(dict(word_counts))
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    wc.to_file('wordcloud_result.png')
    print("워드클라우드가 'wordcloud_result.png'로 저장되었습니다.")

# 10. 워드클라우드 생성 실행
create_korean_wordcloud(word_counts)
