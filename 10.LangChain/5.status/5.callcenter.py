
# 목적 - 고객 문의를 분류해서 상담 답변한다.
# RunnableBranch

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def make_chain(role):
    return (
        ChatPromptTemplate.from_messages([
            ("system", role),
            ("user", "{question}")
        ])
        | llm
        | StrOutputParser()
    )


payment_chain = make_chain("당신은 결제 상담원 입니다. 결제/환불/청구 문제에 대해서 친절하게 답변하세요.")

delivery_chain = make_chain("당신은 배송 상담원 입니다. 배송조회/지연/반품에 대해서 친절하게 설명하세요.")

techsupport_chain = make_chain("당신은 기술지원 담당자 입니다. 웹/서비스/제품설정 등 사용법과 오류를 해결하는 단계를 친절하게 설명하세요.")

general_chain = make_chain("당신은 일반 고객 상담원 입니다. 친절하고 간략하게 답변하세요.")


branch = RunnableBranch(
    (lambda x: any(k in x["question"] for k in ["결제", "환불", "청구"]), payment_chain),
    (lambda x: any(k in x["question"] for k in ["배송", "택배", "반품"]), delivery_chain),
    (lambda x: any(k in x["question"] for k in ["오류", "에러", "안돼요"]), techsupport_chain),
    general_chain,
)


questions = [
    "배송이 아직 안왔어요. 언제쯤 도착할까요?",
    "결제가 두번 됐어요. 환불 가능 할까요?",
    "웹 로그인이 안돼요. 오류 메시지가 떠요.",
    "이용 시간은 어떻게 되나요?"
]


for q in questions:
    print("-" * 40)
    print(f"고객: {q}")
    result = branch.invoke({"question": q})
    print(f"상담원: {result}")