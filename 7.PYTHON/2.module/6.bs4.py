#pip install bs4

from bs4 import BeautifulSoup

html = "<html><head><title>HEllo</title></head><body><h1>Title</h1></body></html>"

soup = BeautifulSoup(html, "html.parser")

print(soup)

heading = soup.find_all('h1')
paragraph = soup.find_all('p')

print(heading)