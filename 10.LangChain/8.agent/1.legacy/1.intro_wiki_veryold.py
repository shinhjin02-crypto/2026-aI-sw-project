import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

tools = load_tools(["wikipedia"])

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPT,
    verbose=True
)

result = agent.invoke({"input": "대한민국의 수도는?"})
print(result)

# Langchain이 업뎃돼서 initialize_agent 를 쓸 수 없음