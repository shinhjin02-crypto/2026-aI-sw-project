import csv
import requests
import os
from dotenv import load_dotenv

#강사님거 붙여ㅕ넣기,,,

load_dotenv() #

API_KEY = os.getenv("YOUTUBE_API_KEY")

video_api_url = 'https://www.googleapis.com/youtube/v3/videos'

video_ids = []

with open("search_result.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        video_ids.append(row["video_id"])

params = {
    "part": "snippet,statistics",
    "id": ",".join(video_ids),
    "key": API_KEY
}

response = requests.get(video_api_url, params=params)
data = response.json()

search_results = []

for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    description = item['snippet']['description']

    search_results.append(item)

    print(f'제목: {title}, id: {video_id}, 설명: {description}')
    print('-' * 40)

#최종 결과 담을 곳
table = []

#가져오고 싶은 추가정보
table_header = ['video_id', 'title', 'view_count', 'like_count', 'comment_count']

with open("video_status.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow(table_header)

    for item in data['items']:

        video_id = item['id']
        title = item["snippet"]["title"]

        stats = item["statistics"]

        view_count = stats.get("viewCount", 0)
        like_count = stats.get("likeCount", 0)
        comment_count = stats.get("commentCount", 0)

        writer.writerow([video_id, title, view_count, like_count, comment_count])