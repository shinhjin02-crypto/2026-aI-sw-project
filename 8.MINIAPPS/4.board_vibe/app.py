from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# 데이터베이스 초기화
database.init_db()

@app.route('/')
def index():
    """메인 페이지를 렌더링합니다."""
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """모든 게시글을 조회하는 API 엔드포인트입니다."""
    try:
        posts = database.get_all_posts()
        return jsonify({
            'success': True,
            'posts': posts
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/posts', methods=['POST'])
def add_post():
    """새로운 게시글을 등록하는 API 엔드포인트입니다."""
    try:
        data = request.get_json()
        
        # 클라이언트 제공 데이터 검증
        if not data:
            return jsonify({
                'success': False,
                'error': '요청 바디가 비어있습니다.'
            }), 400
            
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'error': '제목을 입력해주세요.'
            }), 400
            
        if not message:
            return jsonify({
                'success': False,
                'error': '내용을 입력해주세요.'
            }), 400
            
        # 글자 수 제한 (서버측 검증)
        if len(title) > 50:
            return jsonify({
                'success': False,
                'error': '제목은 최대 50자까지 입력 가능합니다.'
            }), 400
            
        if len(message) > 500:
            return jsonify({
                'success': False,
                'error': '본문은 최대 500자까지 입력 가능합니다.'
            }), 400
            
        # 게시글 생성
        new_post = database.create_post(title, message)
        
        return jsonify({
            'success': True,
            'post': new_post,
            'message': '글이 성공적으로 등록되었습니다!'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 0.0.0.0으로 바인딩하여 외부 접근도 용이하게 함
    app.run(host='0.0.0.0', port=5000, debug=True)
