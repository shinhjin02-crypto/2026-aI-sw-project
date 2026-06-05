import requests

OLLAMA_HOST = "http://192.168.0.64"
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"

payload = {
    "model": "exaone3.5",
    "prompt": "파이썬으로 구현하는 헬로우 월드 코드를 보여줘.",
    "stream": False
}

response = requests.post(OLLAMA_ENDPOINT, json=payload)
data = response.json()

print("모델 응답: ", data.get("response"))