import requests
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def get_youtube_trending_page_selenium(country_code='KR'):
    # ChromeDriver 경로 설정
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 백그라운드 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 브라우저 열기
    driver = webdriver.Chrome( options=options)
    
    # YouTube 인기 동영상 페이지 열기
    url = f"https://www.youtube.com/feed/trending?gl={country_code}"
    driver.get(url)
    time.sleep(1.5)
    # 페이지 로딩 대기
    
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(last_height)
    new_height = 0
    while new_height < last_height :
        new_height += 1000
        driver.execute_script(f"window.scrollTo(0, {new_height})")
        time.sleep(0.5)
        print(new_height)

    time.sleep(1.5)

    return driver

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

            # 썸네일 URL 추출
            thumbnail_element = video.find_element(By.XPATH, './/*[@id="thumbnail"]/yt-image/img')
            thumbnail_url = thumbnail_element.get_attribute('src')
            print(thumbnail_element.get_attribute('src'))
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


# Function to download and save thumbnail images, then embed them into Excel
def save_to_excel_with_images(video_data, file_name='youtube_trending_with_images.xlsx'):
    wb = Workbook()
    ws = wb.active

    # 헤더 추가
    headers = ['Rank', 'Title', 'Channel', 'Views', 'URL', 'Thumbnail']
    ws.append(headers)
    
    # 엑셀 셀 크기 설정 (썸네일 크기에 맞게)
    
    ws.column_dimensions['F'].width = 16  # 열 너비 설정
    ws.column_dimensions['F'].width = 16  # 열 너비 설정

    for index, video in enumerate(video_data, start=2):
        # 썸네일 이미지를 다운로드
        try:
            response = requests.get(video['Thumbnail'])
            img_data = BytesIO(response.content)
            img = PILImage.open(img_data)

            # 이미지 임시 저장 후 엑셀 삽입
            img_filename = f"thumbnail_{index}.png"
            img.save(img_filename)
            excel_img = Image(img_filename)
            excel_img.width, excel_img.height = (128, 72)
            ws.row_dimensions[index].height = 54  # 행 높이 설정
            
            # 썸네일을 셀에 삽입
            ws.add_image(excel_img, f'F{index}')
        except Exception as e:
            print(f"Failed to download image for video {video['Rank']}: {e}")

        # 텍스트 데이터 추가
        ws.append([video['Rank'], video['Title'], video['Channel'], video['Views'], video['URL']])

    # 엑셀 파일 저장
    wb.save(file_name)
    print(f'Data saved to {file_name}')

# Main script
def main():
    country_code = 'KR'
    driver = get_youtube_trending_page_selenium(country_code)
    
    try:
        video_data = parse_trending_videos_selenium(driver)
        save_to_excel_with_images(video_data)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
