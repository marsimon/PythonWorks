from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Function to set up the webdriver and get YouTube trending page
def get_youtube_trending_page_selenium(country_code='KR'):
    # 브라우저 열기
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 백그라운드 실행 옵션
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    # YouTube 인기 동영상 페이지 열기
    url = f"https://www.youtube.com/feed/trending?gl={country_code}"
    driver.get(url)
    
    # 페이지 로딩 대기
    time.sleep(2)  # YouTube 페이지가 완전히 로드될 때까지 대기
    
    return driver

# Function to parse trending videos
def parse_trending_videos_selenium(driver):
    videos = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
    
    video_data = []
    for index, video in enumerate(videos, start=1):
        try:
            # 제목, 채널, 조회수, URL 추출
            title_element = video.find_element(By.ID, 'video-title')
            title = title_element.text
            url = title_element.get_attribute('href')
            
            channel = video.find_element(By.XPATH, './/*[@id="text"]/a').text
            views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
            
            thumbnail_element = video.find_element(By.XPATH, './/*[@id="img"]')
            thumbnail_url = thumbnail_element.get_attribute('src')
            
            video_data.append({
                'Rank': index,
                'Title': title,
                'Channel': channel,
                'Views': views,
                'URL': url,
                'Thumbnail': thumbnail_url
            })
        except Exception as e:
            print(f"Error processing video {index}: {e}")
    
    return video_data

# Function to save data to an Excel file
def save_to_excel(video_data, file_name='youtube_trending_selenium.xlsx'):
    df = pd.DataFrame(video_data)
    df.to_excel(file_name, index=False)
    print(f'Data saved to {file_name}')

# Main script
def main():
    country_code = 'KR'  # 국가 코드를 변경하여 다른 나라의 인기 동영상을 가져올 수 있음
    driver = get_youtube_trending_page_selenium(country_code)
    
    try:
        video_data = parse_trending_videos_selenium(driver)
        save_to_excel(video_data)
    finally:
        driver.quit()  # 브라우저 닫기

if __name__ == '__main__':
    main()
