from google_play_scraper import reviews_all, Sort
import pandas as pd

# 1. '트릭컬 리바이브' 앱 패키지 이름
app_package_name = 'com.epidgames.trickcalrevive'

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
output_file = 'trickcal_revive_reviews.csv'
df.to_csv(
    output_file,
    index=False,
    encoding='utf-8-sig',
    quoting=1,
    escapechar='\\'
)

print(f"리뷰 데이터가 '{output_file}'에 저장되었습니다.")
