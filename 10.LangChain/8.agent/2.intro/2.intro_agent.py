from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

# 우리의 도구를 정의할 때 @tool 테코레이터를 정의하고, 함수 내에 주석을 쓰면, 
# 그 내용을 읽어가서 본인이 해야할 일을 파악한다.
@tool
def calculator(expression):
    """ 수학 식을 계싼한다. 예: 53 * 7 + 2 """
    return str(eval(expression))

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [calculator]) #나의 에이전트

result = agent.invoke({
    "messages": [("user", "(50 * 5 + 5) / 5는 얼마야?")]
})

print('=== 전체 메시지 흐름 ===')
for m in result["messages"]:
    if hasattr(m, "tool_calls") and m.tool_calls:
        for c in m.tool_calls:
            print(f"[도구 호출] {c['name']}({c['args']})")
    if m.content:
        prefix = {"human": "[사용자]", "ai": "[AI]", "tool": "[도구 결과]"}.get(m.type, m.type)
        print(f"{prefix} {m.content}")