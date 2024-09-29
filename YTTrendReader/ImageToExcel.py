from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 백그라운드 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

    # 브라우저 열기
driver = webdriver.Chrome( options=options)

# 유튜브 영상 링크
video_url = "https://www.youtube.com/watch?v=3n4oPLWi44k"  # 여기에 원하는 유튜브 링크를 넣으세요.

# 해당 URL로 이동
driver.get(video_url)

# 페이지 로드 대기 (네트워크 상황에 따라 조정 가능)
time.sleep(3)

# 해시태그가 위치하는 영역 찾기 (제목 위쪽에 표시된 해시태그들)
try:
    hashtags = driver.find_elements(By.CSS_SELECTOR, "yt-formatted-string.style-scope.ytd-video-primary-info-renderer a")

    if hashtags:
        print("해시태그 정보:")
        for hashtag in hashtags:
            print(hashtag.text)
    else:
        print("해시태그를 찾을 수 없습니다.")
finally:
    # 드라이버 종료
    driver.quit()
