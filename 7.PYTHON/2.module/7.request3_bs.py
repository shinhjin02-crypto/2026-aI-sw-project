import requests
from bs4 import BeautifulSoup

url = "https://www.example.com"
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "html.parser")
#print(soup)

title = soup.find_all("title")
print(title)

headings = soup.find_all("h1")
print(headings)

divs = soup.find_all("div")
print(divs)

for elem in divs:
    link = elem.a
    if link:
        href = link.get("href")
        print("링크주소: ", href)