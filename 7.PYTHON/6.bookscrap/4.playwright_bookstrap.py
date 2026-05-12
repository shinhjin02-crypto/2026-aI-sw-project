from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")

    #책 목록 가져오기
    books = page.locator("acticle.product_pod")
    #print(books.count())

    for i in range(books.count()):
        book = books.nth(i)

        title = book.locator("h3 a").get_attribute('title')
        print(title)

        price = book.locator(".price_color").inner_text()
        price = price.replace("", " ")
        print(price)