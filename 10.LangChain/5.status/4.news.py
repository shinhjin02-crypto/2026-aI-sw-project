# 목적 - 뉴스를 분석한다.
# 뉴스 입력 -> 요약 
#          -> 감정분석 
#          -> 카테고리 분석
# RunnableParallel

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt1 = ChatPromptTemplate.from_template("다음 뉴스를 2~3문장으로 요약해줘.\n\n{news}")

summary_chain = prompt1 | llm | StrOutputParser()

sentiment_chain = (
    ChatPromptTemplate.from_template("다음 뉴스의 전반적 감성을 한 단어로 분석해줘 (긍정/부정/중립)\n\n{news}")
    | llm
    | StrOutputParser()
)

category_chain = (
    ChatPromptTemplate.from_template("다음 뉴스의 카테고리를 한 단어로 분석해줘(정치/경제/사회/IT/Sports/기타...\n\n{news}")
    | llm
    | StrOutputParser()
)

final_chain = RunnableParallel({
    "summary": summary_chain,
    "sentiment": sentiment_chain,
    "category": category_chain
})

news = """대만 출신인 젠슨 황 엔비디아 최고경영자(CEO)가 대만에 연 1500억달러(약 225조원)를 투자하겠다고 27일(현지 시각) 밝혔다. TSMC를 중심으로 한 대만의 인공지능(AI) 생태계를 핵심 거점으로 삼겠다는 것이다.

황 CEO는 이날 타이베이에서 열린 대만 본사 착공 행사에서 “대만은 AI 혁명의 진원지”라며 “4~5년 전만 해도 엔비디아는 대만에서 연간 100억~150억달러를 썼지만, 지금은 1000억달러, 앞으로는 연간 1500억달러를 쓰게 될 것”이라고 했다. 그는 “칩과 첨단 패키징, AI 시스템, AI 수퍼컴퓨터가 모두 이곳에서 만들어진다”며 대만 본사 완공 후 약 4000명을 고용할 계획이라고 밝혔다. 엔비디아의 새 대만 본사는 2030년 완공을 목표로 한다.

황 CEO의 발언은 엔비디아 생태계의 핵심 역할을 하고 있는 대만과의 협력을 더욱 공고히 하겠다는 의미로 풀이된다. 엔비디아는 그래픽 처리 장치(GPU) 설계와 소프트웨어 플랫폼을 장악하고 있지만, 실제 칩 생산은 TSMC의 첨단 공정에 의존하고 있다. 엔비디아의 차세대 AI 장악력이 커질수록 대만 업체들의 역할도 커지는 구조다. 앞서 AMD도 지난 22일 대만 AI 분야에 100억달러 이상을 투자한다고 밝혔다.

한편 업계에 따르면 황 CEO는 다음 주 타이베이에서 열리는 엔비디아 연례 AI 콘퍼런스 ‘GTC 타이베이 2026’ 일정을 마친 뒤 한국을 방문할 예정인 것으로 전해졌다. 이번 방한을 계기로 삼성전자, SK하이닉스 등 국내 반도체 기업과의 고대역폭 메모리(HBM), 차세대 AI 가속기, 파운드리 협력 논의가 이뤄질 것으로 보인다."""

result = final_chain.invoke({"news": news})
print(f"원문: {news}")
print(f"요약: {result["summary"]}")
print(f"감정: {result["sentiment"]}")
print(f"카테고리: {result["category"]}")