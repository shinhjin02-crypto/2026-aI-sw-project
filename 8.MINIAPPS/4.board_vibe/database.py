import sqlite3
import random
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'board.db')

EMOJIS = [
    "🚀", "✨", "🌈", "🎨", "🔮", "⚡", "🍀", "🧁", "🎸", "🎭", 
    "🪐", "🧸", "🐱", "🍕", "🎈", "💡", "💎", "💌", "🎉", "🔥", 
    "🦄", "👾", "🌟", "🌸", "🐳", "🍟", "🥨", "🧩", "🎤", "🕶️"
]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """데이터베이스 테이블이 존재하지 않는 경우 테이블을 생성합니다."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                color_hue INTEGER NOT NULL,
                emoji TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def get_all_posts():
    """모든 게시글을 작성일 기준 최신순(내림차순)으로 가져옵니다."""
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM posts ORDER BY created_at DESC')
        posts = cursor.fetchall()
        # Row 객체를 dict 리스트로 변환하여 JSON 직렬화가 가능하게 합니다.
        return [dict(post) for post in posts]

def create_post(title, message):
    """새로운 게시글을 생성하고 고유한 색상 Hue와 이모지를 자동으로 할당합니다."""
    # 0부터 360 사이의 무작위 색조(Hue) 생성
    color_hue = random.randint(0, 360)
    # 목록에서 임의의 이모지 선택
    emoji = random.choice(EMOJIS)
    
    with get_db_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO posts (title, message, color_hue, emoji) VALUES (?, ?, ?, ?)',
            (title, message, color_hue, emoji)
        )
        conn.commit()
        # 새로 생성된 게시글을 조회하여 반환합니다.
        new_id = cursor.lastrowid
        new_post = conn.execute('SELECT * FROM posts WHERE id = ?', (new_id,)).fetchone()
        return dict(new_post)
