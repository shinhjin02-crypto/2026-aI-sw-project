import requests

url = "http://www.example.com"

response = requests.get(url)

html = response.text

print(html) #이 안에 문자열(string)이 있는 것

print("-"*30)

#원하는 태그 찾아오기
while "<h1>" in html:
    start = html.find("<h1>")
    end = html.find("</h1>")

    text = html[start+4:end]
    print(text)

