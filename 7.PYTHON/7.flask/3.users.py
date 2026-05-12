from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '123-444-7890'},
    {'name': 'Charlie', 'age': 27, 'phone': '123-555-7890'}
]

@app.route('/')
def main():
    # list/dict -> JSON 형태로 변환
    return jsonify(users)

# user 오타 수정
@app.route('/user/<name>')
def get_user_by_name(name):

    print("사용자 입력값:", name)

    user = None

    for u in users:
        if u['name'] == name:
            user = u

    if user:
        # uesr -> user 오타 수정
        return jsonify(user)
    else:
        # 문자열은 따옴표 필요
        return jsonify({"message": "사용자를 찾지 못했습니다."})

if __name__ == '__main__':
    app.run(debug=True)