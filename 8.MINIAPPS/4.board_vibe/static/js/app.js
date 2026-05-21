document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 캐싱
    const vibeForm = document.getElementById('vibeForm');
    const titleInput = document.getElementById('title');
    const messageInput = document.getElementById('message');
    const titleCounter = document.getElementById('titleCounter');
    const messageCounter = document.getElementById('messageCounter');
    const vibeGrid = document.getElementById('vibeGrid');
    const emptyState = document.getElementById('emptyState');
    const totalCountEl = document.getElementById('totalCount');
    const toastContainer = document.getElementById('toastContainer');

    // 실시간 글자수 계산 및 제한 연동
    titleInput.addEventListener('input', () => {
        titleCounter.textContent = `${titleInput.value.length} / 50`;
    });

    messageInput.addEventListener('input', () => {
        messageCounter.textContent = `${messageInput.value.length} / 500`;
    });

    // ==========================================================================
    // 상대 시간 변환기 (SQLite UTC -> 한국인 친화적인 상대 시간)
    // ==========================================================================
    function formatRelativeTime(utcTimeString) {
        try {
            // "YYYY-MM-DD HH:MM:SS" 형식을 ISO 8601 표준 포맷 "YYYY-MM-DDTHH:MM:SSZ"로 변환
            const isoString = utcTimeString.replace(' ', 'T') + 'Z';
            const postDate = new Date(isoString);
            const now = new Date();
            
            const diffMs = now - postDate;
            const diffSec = Math.floor(diffMs / 1000);
            const diffMin = Math.floor(diffSec / 60);
            const diffHour = Math.floor(diffMin / 60);
            const diffDay = Math.floor(diffHour / 24);

            if (diffSec < 5) return '방금 전';
            if (diffSec < 60) return `${diffSec}초 전`;
            if (diffMin < 60) return `${diffMin}분 전`;
            if (diffHour < 24) return `${diffHour}시간 전`;
            if (diffDay < 7) return `${diffDay}일 전`;
            
            // 그 이상은 날짜 및 시각 표시
            return postDate.toLocaleDateString('ko-KR', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            });
        } catch (e) {
            return '방금 전';
        }
    }

    // ==========================================================================
    // 토스트 알림창 출력 시스템
    // ==========================================================================
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const iconName = type === 'success' ? 'check-circle' : 'alert-circle';
        
        toast.innerHTML = `
            <i data-lucide="${iconName}" class="toast-icon-${type}"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        lucide.createIcons(); // 새 아이콘 활성화

        // 4.5초 뒤 제거 (애니메이션 포함)
        setTimeout(() => {
            toast.classList.add('removing');
            toast.addEventListener('transitionend', () => {
                toast.remove();
            });
        }, 4000);
    }

    // ==========================================================================
    // 개별 카드 엘리먼트 생성
    // ==========================================================================
    function createCardElement(post) {
        const card = document.createElement('article');
        card.className = 'glass-card vibe-card fade-in-up';
        
        // 커스텀 CSS 변수를 전달해 고유 그라데이션 및 네온 효과 부여
        card.style.setProperty('--card-hue', post.color_hue);
        card.dataset.id = post.id;
        
        const timeFormatted = formatRelativeTime(post.created_at);
        
        card.innerHTML = `
            <div class="card-header">
                <div class="card-emoji-title">
                    <span class="card-emoji">${post.emoji}</span>
                    <h4 class="card-title" title="${escapeHtml(post.title)}">${escapeHtml(post.title)}</h4>
                </div>
                <time class="card-date" datetime="${post.created_at}">
                    <i data-lucide="clock" style="width:12px; height:12px;"></i>
                    ${timeFormatted}
                </time>
            </div>
            <div class="card-body">
                <p class="card-message">${escapeHtml(post.message)}</p>
            </div>
            <div class="card-glow-bar"></div>
        `;
        
        return card;
    }

    // HTML 특수 문자 이스케이프 (XSS 방지)
    function escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // ==========================================================================
    // 카드 피드 조회 및 렌더링
    // ==========================================================================
    async function loadPosts() {
        try {
            const response = await fetch('/api/posts');
            const data = await response.json();
            
            if (data.success) {
                const posts = data.posts;
                
                // 총 Vibe 개수 업데이트
                totalCountEl.textContent = posts.length;
                
                if (posts.length > 0) {
                    // 비어있음 컴포넌트 은닉
                    if (emptyState) emptyState.style.display = 'none';
                    
                    // 기존 Grid 초기화 (empty state가 들어있었을 수 있으므로 빈 그리드로 변환)
                    vibeGrid.innerHTML = '';
                    
                    posts.forEach(post => {
                        const card = createCardElement(post);
                        vibeGrid.appendChild(card);
                    });
                    
                    // 신규 렌더링 카드들에 대해 Lucide 아이콘 적용
                    lucide.createIcons();
                } else {
                    // 글이 없는 경우
                    vibeGrid.innerHTML = '';
                    vibeGrid.appendChild(emptyState);
                    emptyState.style.display = 'flex';
                }
            } else {
                showToast(data.error || '글을 불러오는 도중 오류가 발생했습니다.', 'error');
            }
        } catch (error) {
            console.error('Error fetching posts:', error);
            showToast('서버와의 연결이 원활하지 않습니다.', 'error');
        }
    }

    // ==========================================================================
    // 폼 제출 (비동기 POST 글 작성)
    // ==========================================================================
    vibeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = titleInput.value.trim();
        const message = messageInput.value.trim();
        
        // 전면 유효성 검사
        if (!title) {
            showToast('제목을 입력해주세요!', 'error');
            titleInput.focus();
            return;
        }
        if (!message) {
            showToast('내용을 입력해주세요!', 'error');
            messageInput.focus();
            return;
        }
        
        const submitBtn = vibeForm.querySelector('.submit-btn');
        const originalBtnHtml = submitBtn.innerHTML;
        
        try {
            // 버튼 로딩 상태 전환
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span>전송 중...</span><i data-lucide="loader" class="btn-icon animate-spin"></i>`;
            lucide.createIcons();
            
            const response = await fetch('/api/posts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // 성공 알림
                showToast(data.message || '소중한 글이 등록되었습니다!', 'success');
                
                // 폼 리셋 및 카운터 초기화
                vibeForm.reset();
                titleCounter.textContent = '0 / 50';
                messageCounter.textContent = '0 / 500';
                
                // 신규 생성된 카드 가져오기
                const newPost = data.post;
                const newCard = createCardElement(newPost);
                
                // 그리드가 비어있었을 때 emptyState 제거
                if (vibeGrid.contains(emptyState)) {
                    emptyState.style.display = 'none';
                    vibeGrid.innerHTML = '';
                }
                
                // 그리드 맨 위에 새 카드 추가 (prepend)
                vibeGrid.insertBefore(newCard, vibeGrid.firstChild);
                lucide.createIcons();
                
                // 총 개수 증가
                const currentCount = parseInt(totalCountEl.textContent, 10);
                totalCountEl.textContent = currentCount + 1;
                
            } else {
                showToast(data.error || '글 등록에 실패했습니다.', 'error');
            }
        } catch (error) {
            console.error('Error adding post:', error);
            showToast('네트워크 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.', 'error');
        } finally {
            // 버튼 원래 상태 복구
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHtml;
            lucide.createIcons();
        }
    });

    // 페이지 초기화 로딩
    loadPosts();
});
