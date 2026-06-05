import anthropic

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

messages = []

def ask(question):
    print("[질문]", question)

    messages.append({'role': 'user', 'content': question})

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens = 300,
        temperature=1.0,
        messages=messages
    )    

    answer = message.content[0].text
    messages.append({'role': 'assistant', 'content': answer})
    return message

print("[챗봇]", ask("내 이름은 홍길동이야."))