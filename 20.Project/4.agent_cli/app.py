# 금융 도우미 에이전트 챗봇 만들기

# 랭체인들을 불러온다
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from fin_tools import TOOLS

load_dotenv()

SYSTEM="""
당신은 금융 정보 비서입니다. 뉴스검색, 기업정보조회, 환율, 주가 도구를 사용해서 한국어로 간결하게 답변을 주는 금융 비서입니다.
- 환율/주가 같은 수치 데이터는 반드시 도구를 통해서 확인하시오 (추측 또는 과거데이터 이용 금지)
- 출처 링크가 있으면 함께 제시하시오.
"""

agent = create_agent(ChatOpenAI(model="gpt-4o-mini"), TOOLS, system_prompt=SYSTEM)


def ask(q):
    # agent를 통해서 해당 질문을 호출한다.
    print('[질문]', q)
    result = agent.invoke({"messages": [("user", q)]})
    tool_used = [c["name"] for m in result["messages"]
                 if getattr(m, "tool_calls", None) for c in m.tool_calls]
    print(f"[사용 도구] {tool_used or '(없음)'}")
    print(f"[답변] {result['messages'][-1].content}")

if __name__ == "__main__":
    print('=== 데모 명령어 실행 ===')
    for q in ["삼성전자 주가 알려줘", "달러 환율 얼마야?", "엔비디아 관련 최근 뉴스는 뭐가 있어?"]:
        ask(q)

    print('=== 수동 질의 응답 시작 ===')
    while True:
        # 사용자로부터 질문을 받아서 'q', 'quit', 'exit', 가 올때까지 반복한다.
        q = input('질문> ').strip()
        if not q or q.lower() in ("q", "quit", "exit"):
            break
        ask(q)