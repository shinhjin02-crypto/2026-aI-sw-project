import requests

url = 'https://api.github.com/users/lovehyun/repos'

resp = requests.get(url)
repos = resp.json()

data = []

for repo in repos:
    name = repo['name']
    html_url = repo['html_url']
    description = repo['description']

    data.append({
        'name': name,
        'html_url': html_url,
        'desc': description
    })

print(f"{'리포이름':<30} {'리포URL':<50} {'설명':<20}")

for d in data:
    print(f"리포이름: {d['name']:<30}, 리포URL{d['html_url']:<50}") 

    #print(reop['name'])
    #print(repo['html_url'])
    #print(repo['description'])
    
     #변수명, 함수명, 클래스명, 파일명, 디렉토리명 다 meaningful하게 짓기.