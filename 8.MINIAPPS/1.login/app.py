from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session, flash

from datetime import timedelta

import sqlite3

app = Flask(__name__)
app.secret_key = 'hello1234' #실무적으로는 커밋하지 않음
app.permanent_session_lifetime = timedelta(minutes = 5)

DATABASE = 'users.sqlite3' #나의 파일명

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row #나의 결과를 다 Dict 포멧으로 관리
                                   #row[0] => row['id'] 이런식으로 접근 가능
    return conn

def init_db():
    with app.app_context(): #flask app 초기화 완료된 후
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
            )''')
        
        #기본게정 추가
        cur.execute("SELECT COUNT(*) AS count FROM users")
        count = cur.fetchone()['count']

        if count == 0:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("user1", "password1") # 실무적으로는 암호화 된 비번이 들어간다
            )

            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("user2", "password2")
            )

        #부팅시 계정 정보 출력
        cur.execute('SELECT * FROM users')
        rows = cur.fetchall()

        print('-' * 30)
        for row in rows:
            print(row['id'], row['username'], row['password'])
        print('-' * 30)

        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # 사용자가 입력한 username/password 받아오기
        username = request.form.get("username")
        password = request.form.get("password")

        # DB 연결
        conn = get_db_connection()
        cur = conn.cursor()

        # username/password 둘 다 일치하는 계정 찾기
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        # 결과 하나 가져오기
        user_data = cur.fetchone()

        # DB 연결 종료
        conn.close()

        # 로그인 성공
        if user_data:
            session['user'] = username

            # 세션 유지시간 갱신
            session.permanent = True

            flash("로그인에 성공하였습니다.")
            return redirect(url_for("home"))

        # 로그인 실패
        else:
            flash("로그인에 실패하였습니다.")
            return redirect(url_for("login"))

    return render_template('login.html')

@app.route('/logout')
def logout():

    # 세션 삭제
    session.pop("user", None)

    flash("성공적으로 로그아웃이 되었습니다.")

    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True) #실무적으로는 꼭 ~~~~~ 끌 것