import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get YouTube trending page HTML
def get_youtube_trending_page(country_code='KR'):
    url = f"https://www.youtube.com/feed/trending?gl={country_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to parse the trending page and extract video information
def parse_trending_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    video_data = []
    
    # Each video is within a "ytd-video-renderer" tag
    videos = soup.find_all('ytd-video-renderer', limit=20)  # limiting to top 20 for this example
    
    for index, video in enumerate(videos, start=1):
        title = video.find('a', id='video-title').text.strip()
        url = 'https://www.youtube.com' + video.find('a', id='video-title')['href']
        views = video.find('span', class_='view-count').text.strip() if video.find('span', class_='view-count') else 'N/A'
        channel = video.find('a', class_='yt-simple-endpoint style-scope yt-formatted-string').text.strip()
        
        video_data.append({
            'Rank': index,
            'Title': title,
            'Channel': channel,
            'Views': views,
            'URL': url
        })
        
    return video_data

# Function to save the extracted data into an Excel file
def save_to_excel(video_data, file_name='youtube_trending.xlsx'):
    df = pd.DataFrame(video_data)
    df.to_excel(file_name, index=False)
    print(f'Data saved to {file_name}')

# Main script to fetch, parse, and save data
def main():
    country_code = 'KR'  # Change the country code for different YouTube trends
    html = get_youtube_trending_page(country_code)
    
    if html:
        video_data = parse_trending_page(html)
        save_to_excel(video_data)
    else:
        print("Failed to retrieve the page.")

if __name__ == '__main__':
    main()
