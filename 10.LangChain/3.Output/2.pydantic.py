from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """ 영화 리뷰 분석 결과 """
    title: str = Field(description="영화 제목")
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    score: int = Field(description="1~10 점수")
    summary: str = Field(description="리뷰 요약(1~2 문장)")
    keywords: list[str] = Field(description="핵심 키워드 3개")

llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=MovieReview)
# print("포멧 명령문: ")
# print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """ 다음 영화 리뷰를 분석해 주세요.
리뷰: {review}

{format_instructions}
"""
)

chain = prompt | llm | parser

reviews = [
    """
    미션 임파서블: 파이널 레코닝은 톰 크루즈의 액션이 여전히 압도적이었다.
    특히 실제 스턴트 장면들의 몰입감이 뛰어났고 긴장감이 끝까지 유지됐다.
    다만 스토리가 다소 복잡해서 이해하기 어려운 부분도 있었다.
    """,

    """
    인사이드 아웃 2는 감정 표현이 더욱 다양해져 공감이 잘 되는 영화였다.
    불안이라는 감정을 섬세하게 다뤄서 많은 사람들이 자신의 이야기처럼 느낄 수 있었다.
    가족과 함께 보기 좋은 따뜻한 애니메이션이었다.
    """,

    """
    듄: 파트2는 영상미와 음악이 엄청난 스케일을 보여줬다.
    전투 장면과 세계관 표현이 인상적이었으며 몰입감이 매우 강했다.
    하지만 러닝타임이 길어서 조금 지루하게 느껴지는 구간도 있었다.
    """
]

for review in reviews:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })

    print(f"제목: {result.title}")
    print(f"감성: {result.sentiment}")
    print(f"점수: {result.score}/10")
    print(f"요약: {result.summary}")
    print(f"키워드: {result.keywords}")
    print("-" * 30)