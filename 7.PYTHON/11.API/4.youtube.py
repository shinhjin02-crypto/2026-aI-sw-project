import requests
import os
from dotenv import load_dotenv

load_dotenv() #

API_KEY = os.getenv("YOUTUBE_API_KEY")

url = 'https://www.googleapis.com/youtube/v3/search'

search_query = "파이썬 튜토리얼"

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(url, params)
data = response.json()

for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    description = item['snippet']['description']

    print(f'제목: {title}, id: {video_id}, 설명: {description}')
    print('-'*40)