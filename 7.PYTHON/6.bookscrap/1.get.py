# 1. books.toscrape.com에 접속해서 페이지를 받아온다
# 2. DOM을 bs4로 구성한다.
# 3. 첫 페이지의 도서명, 평점, 가격을 받아온다
# 4. CSV 파일로 저장한다.

#import requests
#from bs4 import BeautifulSoup
#import csv
#
#url = "https://books.toscrape.com/"
#resp = requests.get(url)
#
## DOM 생성
#soup = BeautifulSoup(resp.text, "html.parser")
#
## 책 정보들 가져오기
#books = soup.find_all("article", class_="product_pod")
#
## CSV 파일 저장
#with open("books.csv", "w", newline="", encoding="utf-8-sig") as file:
#    writer = csv.writer(file)
#
#    # 헤더 작성
#    writer.writerow(["도서명", "평점", "가격"])
#
#    # 책 정보 반복
#    for book in books:
#
#        # 도서명
#        title = book.h3.a["title"]
#
#        # 가격
#        price = book.find("p", class_="price_color").text
#
#        # 평점
#        rating = book.find("p", class_="star-rating")["class"][1]
#
#        print(title, rating, price)
#
#        # CSV 저장
#        writer.writerow([title, rating, price])
#
#print("CSV 저장 완료!")

import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"

resp = requests.get(url)
resp.encoding = "utf-8" # 유니코드 글자로 인식시켜서 꺠진 글자를 제거
soup = BeautifulSoup(resp.text, "html.parser")

#print(soup)

books = soup.find_all("article")
#print(len(books))

rating_map = {
    "One":1,
    "Two":2,
    "Three":3,
    "Four":4,
    "Five":5
}

with open("books.csv", "w", encoding = "utf-8") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow({"도시명", "평점", "가격"})

    for book in books:
        #print(book)
        title = book.h3.a["title"]
        #print(title)

        #평점
        rating = book.p["class"][1]
        rating_num = rating_map[rating]
        #print(rating)

        #가격
        price = book.select_one(".price_color").text
        price = price.replace("£", " ") # 파운드 부호 제거
        #print(price)

        #print(f"도서명: {title}, 평점: {rating_num}, 가격: {price}")
        csv_writer.writerow({title, rating, price})

print("파일 작성 완료")

    