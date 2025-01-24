import requests
import csv
import time

# 스컬 게임의 AppID
APP_ID = "1147560"  # Skul: The Hero Slayer

# API 엔드포인트
BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"

# API 요청 파라미터
params = {
    "json": 1,
    "language": "korean",  # 한국어 리뷰만 가져옴
    "filter": "recent",    # 최신 리뷰 순
    "num_per_page": 100,   # 요청당 최대 100개
    "cursor": "*",         # 페이지네이션 시작점
}

# 리뷰 데이터를 저장할 리스트
all_reviews = []

# 리뷰 데이터 수집
print("리뷰 데이터를 수집 중입니다...")
while True:
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code}")
        break

    data = response.json()

    # 현재 요청의 리뷰 데이터
    reviews = data.get("reviews", [])
    if not reviews:  # 더 이상 가져올 리뷰가 없으면 종료
        print("모든 리뷰를 가져왔습니다.")
        break

    # 리뷰 데이터를 리스트에 추가
    all_reviews.extend(reviews)

    # 다음 페이지로 이동
    params["cursor"] = data["cursor"]

    print(f"{len(reviews)}개의 리뷰를 가져왔습니다. 총 리뷰 수: {len(all_reviews)}")

    # API 서버에 과부하를 주지 않도록 약간의 대기 시간 추가
    time.sleep(1)

# 리뷰 데이터를 CSV 파일로 저장
with open("skul_reviews_korean.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)

    # 헤더 작성
    writer.writerow(["review", "recommendationid", "playtime_forever", "timestamp_created", "votes_up", "votes_funny", "steam_purchase", "received_for_free"])

    # 리뷰 데이터 작성
    for review in all_reviews:
        writer.writerow([
            review.get("review", ""),                  # 리뷰 내용
            review.get("recommendationid", ""),       # 추천 ID
            review["author"].get("playtime_forever", 0),  # 플레이 시간 (전체)
            review.get("timestamp_created", ""),      # 리뷰 작성 시간 (유닉스 타임스탬프)
            review.get("votes_up", 0),                # 도움이 된 투표 수
            review.get("votes_funny", 0),             # 재미있음 투표 수
            review.get("steam_purchase", False),      # 스팀 구매 여부
            review.get("received_for_free", False)    # 무료로 받았는지 여부
        ])

print(f"총 {len(all_reviews)}개의 리뷰 데이터를 skul_reviews_korean.csv 파일에 저장했습니다.")
