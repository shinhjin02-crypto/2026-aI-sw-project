import requests
import os
from dotenv import load_dotenv

load_dotenv() #

API_KEY = os.getenv("YOUTUBE_API_KEY")

search_url = 'https://www.googleapis.com/youtube/v3/search'
main_video_url = 'https://www.googleapis.com/youtube/v3/videos'

search_query = "파이썬 튜토리얼"

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(search_url, params=params)
data = response.json()

search_results = []

for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    description = item['snippet']['description']

    search_results.append(item)

    print(f'제목: {title}, id: {video_id}, 설명: {description}')
    print('-' * 40)

#최종 결과 담을 곳
table = []

#가져오고 싶은 추가정보
table_header = ['index', 'title', 'view count', 'video url']

for index, result in enumerate(search_results, start=1):
    title = result['snippet']['title']
    video_id = result['id']['videoId']
    youtube_url = f'https://www.youtube.com/watch?v={video_id}'

    video_params = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }

    video_response = requests.get(main_video_url, params=video_params)
    video_data = video_response.json()

    if 'items' in video_data and video_data['items']:
        view_count = video_data['items'][0]['statistics']['viewCount']
    else:
        view_count = 'N/A'

    table.append([index, title, view_count, youtube_url])

print(table)