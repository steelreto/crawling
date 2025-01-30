from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Steam 커뮤니티 리뷰 페이지
BASE_URL = "https://steamcommunity.com/app/1623730/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=koreana&p={}"

def fetch_reviews_selenium(page):
    """Steam 웹페이지에서 Selenium을 사용하여 리뷰를 가져오는 함수"""
    url = BASE_URL.format(page)

    # Selenium 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    service = Service("/path/to/chromedriver")  # 크롬드라이버 경로 수정 필요
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)  # 페이지가 완전히 로딩될 때까지 대기

    reviews = driver.find_elements(By.CLASS_NAME, "apphub_CardTextContent")
    extracted_reviews = [review.text.strip() for review in reviews]
    
    driver.quit()
    print(f"✅ 페이지 {page}: {len(extracted_reviews)}개 리뷰 수집 완료")
    return extracted_reviews

if __name__ == '__main__':
    start_time = time.time()
    
    all_reviews = []
    num_pages = 5  # 크롤링할 페이지 수 설정

    for page in range(1, num_pages + 1):
        reviews = fetch_reviews_selenium(page)
        all_reviews.extend(reviews)

    # DataFrame으로 변환 후 CSV 저장
    df = pd.DataFrame(all_reviews, columns=["review"])
    df.to_csv("palworld_reviews_selenium.csv", index=False, encoding="utf-8-sig")

    print(f"\n총 {len(all_reviews)}개의 리뷰를 가져와 'palworld_reviews_selenium.csv'로 저장했습니다.")
    print(f"⏳ 실행 시간: {time.time() - start_time:.2f}초")
