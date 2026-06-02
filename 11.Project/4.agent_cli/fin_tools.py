import os
import re
import requests
from langchain_core.tools import tool


@tool
def get_news(keyword: str) -> str:
    """키워드와 관련된 뉴스를 네이버에서 조회한다."""
    naver_cid = os.getenv("NAVER_CLIENT_ID")
    naver_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not (naver_cid and naver_secret):
        return "네이버 뉴스 API 키가 등록되지 않아 뉴스 검색을 할 수 없습니다."

    resp = requests.get(
        "https://openapi.naver.com/v1/search/news.json",
        params={"query": keyword, "display": 5, "sort": "date"},
        headers={
            "X-Naver-Client-Id": naver_cid,
            "X-Naver-Client-Secret": naver_secret
        }
    )

    items = resp.json().get("items", [])

    if not items:
        return f"'{keyword}' 관련 뉴스 없음"

    return "\n".join(
        f"- {re.sub(r'<[^>]+>', '', it['title'])} ({it['link']})"
        for it in items
    )


@tool
def get_company_info(company: str) -> str:
    """기업 이름으로 회사 개요나 최근 정보를 조회한다."""
    key = os.getenv("SUPER_API_KEY")

    if not key:
        return "SUPER_API_KEY가 설정되지 않아 기업 정보 검색이 불가능합니다."

    return f"{company} 기업 정보 조회 결과입니다."


@tool
def get_exchange_rate(base: str = "USD", target: str = "KRW") -> str:
    """환율을 조회한다. 예: base=USD, target=KRW"""
    resp = requests.get(f"https://open.er-api.com/v6/latest/{base.upper()}")
    data = resp.json()

    rate = data["rates"].get(target.upper())

    if rate is None:
        return f"{base} => {target} 환율 조회에 실패하였습니다."

    return f"1 {base.upper()} = {rate} {target.upper()}"


@tool
def get_stock_price(ticker: str) -> str:
    """yfinance로 다양한 기업의 주가를 가져온다. 예: 애플 AAPL, 삼성전자 005930.KS"""
    import yfinance as yf

    data = yf.Ticker(ticker).history(period="1d")

    if data.empty:
        return f"{ticker} 주가 정보를 찾을 수 없습니다."

    price = data["Close"].iloc[-1]

    return f"{ticker} 현재가: {price:.2f}"


TOOLS = [get_news, get_company_info, get_exchange_rate, get_stock_price]