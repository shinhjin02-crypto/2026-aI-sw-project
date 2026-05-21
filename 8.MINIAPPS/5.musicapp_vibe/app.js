/**
 * Music Vibe - Main SPA Application Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- App State ---
  let currentView = "home";
  let activeHashtagFilter = null;
  let activeAdminTab = "users-panel";
  let activeSongIdForComments = null;

  // --- Toast System ---
  function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    
    // Custom Toast styling injection directly for maximum robustness
    toast.style.padding = "12px 24px";
    toast.style.borderRadius = "12px";
    toast.style.boxShadow = "0 8px 20px rgba(255, 77, 109, 0.15)";
    toast.style.fontWeight = "600";
    toast.style.fontSize = "0.9rem";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "10px";
    toast.style.transition = "all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    toast.style.transform = "translateX(100px)";
    toast.style.opacity = "0";
    toast.style.color = "white";
    toast.style.pointerEvents = "auto";
    
    let icon = "🌸";
    if (type === "success") {
      toast.style.backgroundColor = "var(--accent-pink-hover)";
      icon = '<i class="fa-solid fa-circle-check"></i>';
    } else if (type === "error") {
      toast.style.backgroundColor = "var(--heart-red)";
      icon = '<i class="fa-solid fa-circle-exclamation"></i>';
    } else if (type === "warning") {
      toast.style.backgroundColor = "var(--accent-pink-dark)";
      icon = '<i class="fa-solid fa-triangle-exclamation"></i>';
    } else {
      toast.style.backgroundColor = "var(--text-primary)";
      icon = '<i class="fa-solid fa-circle-info"></i>';
    }
    
    toast.innerHTML = `${icon} <span>${message}</span>`;
    container.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
      toast.style.transform = "translateX(0)";
      toast.style.opacity = "1";
    }, 10);
    
    // Auto remove
    setTimeout(() => {
      toast.style.transform = "translateX(100px)";
      toast.style.opacity = "0";
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3000);
  }

  // --- Helper: Format Relative Time ---
  function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHr = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHr / 24);

    if (diffSec < 60) return "방금 전";
    if (diffMin < 60) return `${diffMin}분 전`;
    if (diffHr < 24) return `${diffHr}시간 전`;
    if (diffDay < 30) return `${diffDay}일 전`;
    
    // Default standard format
    return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
  }

  // --- Routing & Navigation Controller ---
  function initRouter() {
    window.addEventListener("hashchange", handleRouting);
    handleRouting(); // First load trigger
  }

  function navigateTo(hash) {
    window.location.hash = hash;
  }

  function handleRouting() {
    const hash = window.location.hash || "#/home";
    const session = DB.getSession();

    // Close notifications dropdown on nav
    document.getElementById("notification-dropdown").classList.remove("show");

    // Close YouTube Import Bar if present
    document.getElementById("fast-import-bar").style.display = "none";

    // Standard views show/hide helper
    const views = ["home", "top-likes", "hashtags", "song-detail", "profile", "admin"];
    views.forEach(v => {
      const section = document.getElementById(`${v}-view`);
      if (section) section.classList.remove("active");
      
      const navItem = document.getElementById(`nav-${v}`);
      if (navItem) navItem.classList.remove("active");
    });

    // Sub-route parsing
    if (hash.startsWith("#/song")) {
      // Song detail subpage
      currentView = "song-detail";
      document.getElementById("song-detail-view").classList.add("active");
      
      const params = new URLSearchParams(hash.split("?")[1] || "");
      const songId = params.get("id");
      
      if (songId) {
        renderSongDetailPage(songId);
      } else {
        navigateTo("#/home");
        showToast("존재하지 않는 음악 주소입니다.", "error");
      }
    } else if (hash.startsWith("#/home")) {
      currentView = "home";
      document.getElementById("home-view").classList.add("active");
      document.getElementById("nav-home").classList.add("active");
      
      const params = new URLSearchParams(hash.split("?")[1] || "");
      const tagFilter = params.get("tag");
      
      if (tagFilter) {
        activeHashtagFilter = decodeURIComponent(tagFilter);
        document.getElementById("active-hashtag-filter").style.display = "flex";
        document.getElementById("active-hashtag-name").innerText = `#${activeHashtagFilter}`;
      } else {
        activeHashtagFilter = null;
        document.getElementById("active-hashtag-filter").style.display = "none";
      }
      
      renderHomeMusicGrid();
    } else if (hash === "#/top-likes") {
      currentView = "top-likes";
      document.getElementById("top-likes-view").classList.add("active");
      document.getElementById("nav-top-likes").classList.add("active");
      renderTopLikesGrid();
    } else if (hash === "#/hashtags") {
      currentView = "hashtags";
      document.getElementById("hashtags-view").classList.add("active");
      document.getElementById("nav-hashtags").classList.add("active");
      renderHashtagRanking();
    } else if (hash === "#/profile") {
      if (!session) {
        navigateTo("#/home");
        showToast("로그인이 필요한 화면입니다.", "warning");
        return;
      }
      currentView = "profile";
      document.getElementById("profile-view").classList.add("active");
      document.getElementById("nav-profile").classList.add("active");
      renderUserProfile();
    } else if (hash === "#/admin") {
      if (!session || session.role !== "admin") {
        navigateTo("#/home");
        showToast("관리자 전용 권한이 필요합니다.", "error");
        return;
      }
      currentView = "admin";
      document.getElementById("admin-view").classList.add("active");
      document.getElementById("nav-admin").classList.add("active");
      renderAdminDashboard();
    } else {
      // Fallback
      navigateTo("#/home");
    }

    // Update navigation items and layout values
    updateAuthLayout();
  }

  // --- Session Layout Management ---
  function updateAuthLayout() {
    const session = DB.getSession();
    const loginBtn = document.getElementById("header-login-btn");
    const logoutBtn = document.getElementById("header-logout-btn");
    const profileNav = document.getElementById("nav-profile");
    const adminNav = document.getElementById("nav-admin");
    const userDisplay = document.getElementById("user-display-tag");
    const notifBtn = document.getElementById("notif-btn-icon");

    if (session) {
      // Logged in
      loginBtn.style.display = "none";
      logoutBtn.style.display = "inline-flex";
      userDisplay.style.display = "inline-flex";
      userDisplay.innerHTML = `<i class="fa-solid fa-circle-user"></i> ${session.nickname}`;
      profileNav.style.display = "inline-flex";
      notifBtn.style.display = "flex";

      if (session.role === "admin") {
        adminNav.style.display = "inline-flex";
      } else {
        adminNav.style.display = "none";
      }
      
      // Update notifications counter
      updateNotificationsCounter();
    } else {
      // Guest
      loginBtn.style.display = "inline-flex";
      logoutBtn.style.display = "none";
      userDisplay.style.display = "none";
      profileNav.style.display = "none";
      adminNav.style.display = "none";
      notifBtn.style.display = "none";
      document.getElementById("notification-dropdown").classList.remove("show");
    }
  }

  // --- Dynamic Grid Rendering (Cards creation) ---
  function createMusicCardHTML(song, rank = null) {
    const commentsCount = DB.getComments().filter(c => c.songId === song.id).length;
    
    let tagHTML = "";
    if (song.hashtags && song.hashtags.length > 0) {
      tagHTML = song.hashtags.map(t => `<span class="tag" onclick="event.stopPropagation(); window.location.hash='#/home?tag=${encodeURIComponent(t)}'">#${t}</span>`).join("");
    }

    // Custom Rank Badge
    let rankBadgeHTML = "";
    if (rank !== null) {
      rankBadgeHTML = `<div class="rank-badge">${rank}</div>`;
    }

    // Likes toggled status indicator (small heart)
    const session = DB.getSession();
    const isLikedByMe = session && song.likes.includes(session.id);
    const heartIcon = isLikedByMe ? "fa-solid" : "fa-regular";
    const heartStyle = isLikedByMe ? "color: var(--heart-red);" : "";

    return `
      <div class="music-card" onclick="window.location.hash='#/song?id=${song.id}'">
        ${rankBadgeHTML}
        <div class="card-thumbnail-container">
          <img class="card-thumbnail" src="https://img.youtube.com/vi/${song.youtubeId}/hqdefault.jpg" alt="${song.title} 커버" loading="lazy">
          <div class="card-play-overlay">
            <div class="play-icon-circle">
              <i class="fa-solid fa-play fa-lg"></i>
            </div>
          </div>
        </div>
        <div class="card-content">
          <div class="card-artist">${song.artist}</div>
          <div class="card-title">${song.title}</div>
          <div class="card-tags">
            ${tagHTML}
          </div>
          <div class="card-footer">
            <div class="card-likes" onclick="event.stopPropagation(); toggleLike('${song.id}')">
              <i class="${heartIcon} fa-heart" style="${heartStyle}"></i>
              <span>${song.likes.length}</span>
            </div>
            <div class="card-comments-count">
              <i class="fa-regular fa-comment-dots"></i>
              <span>${commentsCount} 댓글</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // Render main home music grid with search filter & sorting
  function renderHomeMusicGrid() {
    const searchVal = document.getElementById("music-search-input").value.toLowerCase().trim();
    const sortVal = document.getElementById("music-sort-select").value;
    const songs = DB.getSongs();
    const comments = DB.getComments();

    // 1. Filtering
    let filteredSongs = songs.filter(song => {
      // A. Active hashtag filter from hashtags view click
      if (activeHashtagFilter) {
        if (!song.hashtags || !song.hashtags.some(t => t.toLowerCase() === activeHashtagFilter.toLowerCase())) {
          return false;
        }
      }

      // B. Main search value (Title, Artist, Description, Tags)
      if (searchVal) {
        const matchesTitle = song.title.toLowerCase().includes(searchVal);
        const matchesArtist = song.artist.toLowerCase().includes(searchVal);
        const matchesDesc = song.description.toLowerCase().includes(searchVal);
        const matchesTags = song.hashtags && song.hashtags.some(t => t.toLowerCase().includes(searchVal));

        if (!matchesTitle && !matchesArtist && !matchesDesc && !matchesTags) {
          return false;
        }
      }

      return true;
    });

    // 2. Sorting
    filteredSongs.sort((a, b) => {
      if (sortVal === "likes") {
        return b.likes.length - a.likes.length;
      } else if (sortVal === "comments") {
        const cA = comments.filter(c => c.songId === a.id).length;
        const cB = comments.filter(c => c.songId === b.id).length;
        return cB - cA;
      } else {
        // default newest
        return new Date(b.createdAt) - new Date(a.createdAt);
      }
    });

    // 3. Output UI
    const container = document.getElementById("music-cards-container");
    if (filteredSongs.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; background-color: var(--bg-secondary); border-radius: var(--border-radius-md); border: 1px solid var(--border-color);">
          <i class="fa-solid fa-music fa-3x" style="color: var(--accent-pink); margin-bottom: 16px;"></i>
          <h3 style="color: var(--text-secondary); margin-bottom: 8px;">일치하는 음악이 없습니다.</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem;">다른 검색어로 검색해보거나 새로운 유튜브 곡을 추가해 보세요!</p>
        </div>
      `;
    } else {
      container.innerHTML = filteredSongs.map(song => createMusicCardHTML(song)).join("");
    }
  }

  // Render Ranked top liked music view
  function renderTopLikesGrid() {
    const songs = DB.getSongs();
    
    // Sort by likes descending
    const sortedSongs = [...songs].sort((a, b) => b.likes.length - a.likes.length);

    const container = document.getElementById("top-likes-cards-container");
    if (sortedSongs.length === 0) {
      container.innerHTML = `<p style="grid-column: 1 / -1; text-align: center; color: var(--text-muted);">등록된 음악이 없습니다.</p>`;
    } else {
      container.innerHTML = sortedSongs.map((song, idx) => createMusicCardHTML(song, idx + 1)).join("");
    }
  }

  // Render Hashtags ranking cloud
  function renderHashtagRanking() {
    const songs = DB.getSongs();
    const tagCounts = {};

    // Gather frequency maps
    songs.forEach(song => {
      if (song.hashtags) {
        song.hashtags.forEach(tag => {
          // Normalize tag string cases
          const cleanTag = tag.trim();
          if (cleanTag) {
            tagCounts[cleanTag] = (tagCounts[cleanTag] || 0) + 1;
          }
        });
      }
    });

    // Sort tag lists by frequency descending
    const sortedTags = Object.keys(tagCounts).map(t => ({
      name: t,
      count: tagCounts[t]
    })).sort((a, b) => b.count - a.count);

    const container = document.getElementById("hashtags-cloud-container");
    if (sortedTags.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; width: 100%; color: var(--text-muted); padding: 40px;">
          <i class="fa-solid fa-tag fa-2x" style="margin-bottom: 10px;"></i>
          <p>등록된 해시태그가 존재하지 않습니다.</p>
        </div>
      `;
    } else {
      container.innerHTML = sortedTags.map(tag => `
        <div class="rank-tag" onclick="window.location.hash='#/home?tag=${encodeURIComponent(tag.name)}'">
          <span># ${tag.name}</span>
          <span class="tag-count">${tag.count}</span>
        </div>
      `).join("");
    }
  }

  // --- Like/Heart Toggle Logic ---
  window.toggleLike = function(songId) {
    const session = DB.getSession();
    if (!session) {
      // Prompt Login Modal
      openAuthModal("login");
      showToast("좋아요를 누르려면 로그인이 필요합니다.", "warning");
      return;
    }

    const songs = DB.getSongs();
    const songIndex = songs.findIndex(s => s.id === songId);

    if (songIndex > -1) {
      const song = songs[songIndex];
      const likeIndex = song.likes.indexOf(session.id);
      let actionResult = "liked";

      if (likeIndex > -1) {
        // Unlike
        song.likes.splice(likeIndex, 1);
        actionResult = "unliked";
      } else {
        // Like
        song.likes.push(session.id);
      }

      DB.saveSongs(songs);

      // Trigger alerts or toasts
      if (actionResult === "liked") {
        showToast(`'${song.title}' 음악을 좋아요 했습니다! ❤️`);
      } else {
        showToast("좋아요를 취소했습니다.");
      }

      // Live updates depending on active views
      if (currentView === "home") {
        renderHomeMusicGrid();
      } else if (currentView === "top-likes") {
        renderTopLikesGrid();
      } else if (currentView === "song-detail" && activeSongIdForComments === songId) {
        renderSongDetailPage(songId);
      }
    }
  };

  // --- Song Detail View Page (Iframe, tags, comments list) ---
  function renderSongDetailPage(songId) {
    activeSongIdForComments = songId;
    const songs = DB.getSongs();
    const song = songs.find(s => s.id === songId);

    if (!song) {
      navigateTo("#/home");
      showToast("선택한 음악 정보를 찾을 수 없습니다.", "error");
      return;
    }

    const session = DB.getSession();

    // 1. Render YouTube Iframe Embed
    const videoContainer = document.getElementById("detail-video-container");
    videoContainer.innerHTML = `
      <iframe src="https://www.youtube.com/embed/${song.youtubeId}?autoplay=1&enablejsapi=1" 
        title="${song.title} 플레이어" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen>
      </iframe>
    `;

    // 2. Metadata text filling
    document.getElementById("detail-artist-text").innerText = song.artist;
    document.getElementById("detail-title-text").innerText = song.title;
    document.getElementById("detail-description-text").innerText = song.description || "등록된 곡 소개글이 없습니다.";
    
    // Likes counter state
    document.getElementById("detail-likes-count").innerText = song.likes.length;
    
    const heartBtn = document.getElementById("detail-heart-btn");
    const isLiked = session && song.likes.includes(session.id);
    if (isLiked) {
      heartBtn.classList.add("liked");
    } else {
      heartBtn.classList.remove("liked");
    }

    // Dynamic clean-up event mapping for heart click on detail screen
    heartBtn.onclick = () => toggleLike(song.id);

    // 3. Render tags list with delete buttons
    const tagsListContainer = document.getElementById("detail-tags-list");
    if (song.hashtags && song.hashtags.length > 0) {
      tagsListContainer.innerHTML = song.hashtags.map(t => `
        <span class="manage-tag">
          #${t}
          ${session ? `<button class="delete-tag-btn" onclick="deleteHashtag('${song.id}', '${t}')" title="태그 삭제">&times;</button>` : ""}
        </span>
      `).join("");
    } else {
      tagsListContainer.innerHTML = `<span style="color: var(--text-muted); font-size: 0.85rem; font-style: italic;">#등록된_태그가_없습니다</span>`;
    }

    // Toggle add tag input area depending on auth state
    const addTagForm = document.getElementById("detail-add-tag-form");
    const addTagGuestMsg = document.getElementById("detail-tag-guest-msg");
    
    if (session) {
      addTagForm.style.display = "flex";
      addTagGuestMsg.style.display = "none";
      
      // Hook add tag trigger
      const addTagInput = document.getElementById("detail-new-tag-input");
      const addTagBtn = document.getElementById("detail-add-tag-btn");
      
      addTagInput.value = "";
      
      const submitTag = () => {
        const tagText = addTagInput.value.trim();
        if (tagText) {
          addHashtag(song.id, tagText);
          addTagInput.value = "";
        }
      };

      addTagBtn.onclick = submitTag;
      addTagInput.onkeypress = (e) => {
        if (e.key === "Enter") submitTag();
      };
    } else {
      addTagForm.style.display = "none";
      addTagGuestMsg.style.display = "block";
    }

    // 4. Render Comments listing
    renderCommentsSection(song.id);
  }

  // --- Add/Delete Hashtags Actions ---
  window.deleteHashtag = function(songId, tag) {
    const session = DB.getSession();
    if (!session) return;

    const songs = DB.getSongs();
    const songIndex = songs.findIndex(s => s.id === songId);

    if (songIndex > -1) {
      const song = songs[songIndex];
      song.hashtags = song.hashtags.filter(t => t.toLowerCase() !== tag.toLowerCase());
      
      DB.saveSongs(songs);
      showToast(`#${tag} 태그를 성공적으로 삭제했습니다.`);
      renderSongDetailPage(songId);
    }
  };

  function addHashtag(songId, tagString) {
    const session = DB.getSession();
    if (!session) return;

    const songs = DB.getSongs();
    const songIndex = songs.findIndex(s => s.id === songId);

    if (songIndex > -1) {
      const song = songs[songIndex];
      if (!song.hashtags) song.hashtags = [];

      // Split strings by commas or spaces for batch creation
      const inputTags = tagString.split(/[\s,]+/).map(t => t.replace(/#/g, "").trim()).filter(t => t.length > 0);
      let addedCount = 0;

      inputTags.forEach(cleanTag => {
        // Prevent duplicates
        const exists = song.hashtags.some(t => t.toLowerCase() === cleanTag.toLowerCase());
        if (!exists) {
          song.hashtags.push(cleanTag);
          addedCount++;
        }
      });

      if (addedCount > 0) {
        DB.saveSongs(songs);
        showToast(`${addedCount}개의 해시태그를 추가했습니다!`);
        renderSongDetailPage(songId);
      } else {
        showToast("이미 존재하는 해시태그이거나 잘못된 값입니다.", "warning");
      }
    }
  }

  // --- Comments Section Rendering & Operations ---
  function renderCommentsSection(songId) {
    const allComments = DB.getComments();
    const activeComments = allComments.filter(c => c.songId === songId);
    const users = DB.getUsers();
    const session = DB.getSession();

    // Update Counter text
    document.getElementById("detail-comments-count").innerText = activeComments.length;

    // Render avatar letter helper
    const activeAvatar = document.getElementById("comment-active-avatar");
    if (session) {
      const firstLetter = session.nickname ? Array.from(session.nickname)[0] : session.id[0].toUpperCase();
      activeAvatar.innerText = firstLetter;
      if (session.role === "admin") {
        activeAvatar.classList.add("admin-avatar");
      } else {
        activeAvatar.classList.remove("admin-avatar");
      }
    } else {
      activeAvatar.innerText = "?";
      activeAvatar.classList.remove("admin-avatar");
    }

    // Toggle Write comment wrapper form
    const commentForm = document.getElementById("detail-comment-form");
    const guestPrompt = document.getElementById("comment-guest-prompt");

    if (session) {
      commentForm.style.display = "block";
      guestPrompt.style.display = "none";
      
      // Clean comment box value
      document.getElementById("comment-text-input").value = "";
    } else {
      commentForm.style.display = "none";
      guestPrompt.style.display = "block";
    }

    // Build lists HTML
    const listContainer = document.getElementById("detail-comments-list");
    
    if (activeComments.length === 0) {
      listContainer.innerHTML = `
        <div style="text-align: center; padding: 30px; color: var(--text-muted); font-size: 0.9rem; font-style: italic;">
          첫 번째로 의견을 작성해보세요! 🌸
        </div>
      `;
    } else {
      // Sort comments chronological (oldest to newest for threads readability)
      const sortedComments = [...activeComments].sort((a,b) => new Date(a.createdAt) - new Date(b.createdAt));
      
      listContainer.innerHTML = sortedComments.map(comment => {
        const commentAuthor = users.find(u => u.id === comment.userId);
        const authorNickname = commentAuthor ? commentAuthor.nickname : "탈퇴한 회원";
        const authorRole = commentAuthor ? commentAuthor.role : "user";
        const firstLetter = authorNickname ? Array.from(authorNickname)[0] : "?";

        // Admin Badge
        let roleBadge = "";
        if (authorRole === "admin") {
          roleBadge = `<span class="comment-author-badge"><i class="fa-solid fa-crown fa-xs"></i> 관리자</span>`;
        }

        // Parse mentions (@Nickname -> formatted wrapper span)
        let formattedText = escapeHTML(comment.text);
        
        // Find users to parse their nicknames as tags
        users.forEach(u => {
          if (u.nickname) {
            const mentionTag = `@${u.nickname}`;
            // Use regex replacement for all occurrences
            const regex = new RegExp(escapeRegExp(mentionTag), "g");
            formattedText = formattedText.replace(regex, `<span class="mention">${mentionTag}</span>`);
          }
        });

        // Toggle delete button
        const canDelete = session && (session.id === comment.userId || session.role === "admin");
        const deleteButtonHTML = canDelete ? `
          <button class="comment-action-btn" onclick="deleteComment('${comment.id}')" title="댓글 삭제" style="color: var(--text-muted); margin-left: auto;">
            <i class="fa-regular fa-trash-can"></i> 삭제
          </button>
        ` : "";

        // Hook reply shortcut mapping to click
        const replyClickHTML = session ? `
          <button class="comment-action-btn" onclick="insertReplyMention('${authorNickname}')" title="답글 달기">
            <i class="fa-solid fa-reply"></i> 답글
          </button>
        ` : "";

        return `
          <div class="comment-bubble">
            <div class="comment-avatar ${authorRole === 'admin' ? 'admin-avatar' : ''}">
              ${firstLetter}
            </div>
            <div class="comment-content">
              <div class="comment-meta">
                <span class="comment-author">${authorNickname} ${roleBadge}</span>
                <span class="comment-time">${formatRelativeTime(comment.createdAt)}</span>
              </div>
              <div class="comment-text">${formattedText}</div>
              <div class="comment-actions">
                ${replyClickHTML}
                ${deleteButtonHTML}
              </div>
            </div>
          </div>
        `;
      }).join("");
    }
  }

  // --- Relative Mentions autocomplete UI implementation ---
  const commentInput = document.getElementById("comment-text-input");
  const suggestionsBox = document.getElementById("mention-users-list");
  
  if (commentInput && suggestionsBox) {
    commentInput.addEventListener("input", (e) => {
      const value = e.target.value;
      const caretPos = e.target.selectionStart;
      const textBeforeCaret = value.substring(0, caretPos);
      
      // Match trailing @name syntax
      const match = textBeforeCaret.match(/@([^\s]*)$/);
      
      if (match) {
        const query = match[1].toLowerCase();
        const users = DB.getUsers().filter(u => u.nickname && u.id !== "admin"); // Don't suggest admin usually
        
        const filteredUsers = users.filter(u => u.nickname.toLowerCase().includes(query));
        
        if (filteredUsers.length > 0) {
          suggestionsBox.innerHTML = filteredUsers.map(u => `
            <div class="mention-user-item" data-nickname="${u.nickname}">
              🌸 ${u.nickname} (${u.id})
            </div>
          `).join("");
          suggestionsBox.classList.add("show");
          
          // Map click
          const items = suggestionsBox.querySelectorAll(".mention-user-item");
          items.forEach(item => {
            item.onclick = () => {
              const nick = item.getAttribute("data-nickname");
              const replacement = `@${nick} `;
              
              const startText = textBeforeCaret.substring(0, textBeforeCaret.length - match[0].length);
              const endText = value.substring(caretPos);
              
              commentInput.value = startText + replacement + endText;
              suggestionsBox.classList.remove("show");
              commentInput.focus();
            };
          });
        } else {
          suggestionsBox.classList.remove("remove");
        }
      } else {
        suggestionsBox.classList.remove("show");
      }
    });

    // Close suggestions box if user clicks outside
    document.addEventListener("click", (e) => {
      if (!suggestionsBox.contains(e.target) && e.target !== commentInput) {
        suggestionsBox.classList.remove("show");
      }
    });
  }

  // Reply trigger mapping shortcut
  window.insertReplyMention = function(nickname) {
    const input = document.getElementById("comment-text-input");
    if (input) {
      input.value = `@${nickname} ` + input.value;
      input.focus();
      // Scroll to comment form smoothly
      input.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  };

  // --- Submit Comment & Live Push Notifications System ---
  const commentSubmitBtn = document.getElementById("comment-submit-btn");
  if (commentSubmitBtn) {
    commentSubmitBtn.onclick = () => {
      const session = DB.getSession();
      if (!session) {
        showToast("로그인이 필요한 요청입니다.", "warning");
        return;
      }

      const input = document.getElementById("comment-text-input");
      const text = input.value.trim();
      
      if (!text) {
        showToast("댓글 내용을 기입해주세요.", "warning");
        return;
      }

      const comments = DB.getComments();
      const newComment = {
        id: `comment_${Date.now()}`,
        songId: activeSongIdForComments,
        userId: session.id,
        text: text,
        createdAt: new Date().toISOString()
      };

      comments.push(newComment);
      DB.saveComments(comments);

      // Trigger Push Notification triggers
      triggerPushNotifications(activeSongIdForComments, session, text);

      showToast("댓글을 성공적으로 게시했습니다! 🌸");
      input.value = "";
      renderCommentsSection(activeSongIdForComments);
    };
  }

  // Live notifications compiler trigger
  function triggerPushNotifications(songId, commenterSession, commentText) {
    const songs = DB.getSongs();
    const song = songs.find(s => s.id === songId);
    if (!song) return;

    // Target: Anyone who liked the song, except the commenter themselves
    const likersToAlert = song.likes.filter(userId => userId !== commenterSession.id);
    
    if (likersToAlert.length > 0) {
      const notifications = DB.getNotifications();
      
      likersToAlert.forEach(targetUserId => {
        const newNotif = {
          id: `notif_${Date.now()}_${Math.floor(Math.random() * 1000)}`,
          targetUserId: targetUserId,
          triggerUserId: commenterSession.id,
          songId: songId,
          type: "new_comment",
          message: `${commenterSession.nickname}님이 회원님이 좋아요 한 '${song.title}'에 댓글을 남겼습니다: "${commentText.substring(0,18)}..."`,
          read: false,
          createdAt: new Date().toISOString()
        };

        notifications.push(newNotif);
      });

      DB.saveNotifications(notifications);
      
      // Instantly update counter just in case active recipient is online
      updateNotificationsCounter();
    }
  }

  // Delete Comment Action
  window.deleteComment = function(commentId) {
    const session = DB.getSession();
    if (!session) return;

    let comments = DB.getComments();
    const comment = comments.find(c => c.id === commentId);

    if (comment) {
      // Security check
      if (comment.userId !== session.id && session.role !== "admin") {
        showToast("본인이 남긴 글만 삭제가 가능합니다.", "error");
        return;
      }

      comments = comments.filter(c => c.id !== commentId);
      DB.saveComments(comments);
      
      showToast("댓글을 안전하게 삭제했습니다.");
      
      // Update UI
      if (activeSongIdForComments) {
        renderCommentsSection(activeSongIdForComments);
      }
    }
  };

  // --- Real-time Notifications dropdown rendering & counter badge ---
  function updateNotificationsCounter() {
    const session = DB.getSession();
    if (!session) return;

    const notifs = DB.getNotifications().filter(n => n.targetUserId === session.id && n.read === false);
    const badge = document.getElementById("notif-badge-count");

    if (notifs.length > 0) {
      badge.style.display = "flex";
      badge.innerText = notifs.length;
    } else {
      badge.style.display = "none";
    }
  }

  function renderNotificationsDropdownList() {
    const session = DB.getSession();
    if (!session) return;

    const notifs = DB.getNotifications().filter(n => n.targetUserId === session.id);
    const container = document.getElementById("notification-list-items");

    if (notifs.length === 0) {
      container.innerHTML = `
        <div class="notif-empty">
          <i class="fa-solid fa-bell-slash fa-2x" style="color: var(--accent-pink); margin-bottom: 10px;"></i>
          <p>새로운 소식이 없습니다.</p>
        </div>
      `;
      return;
    }

    // Display newest first
    const sortedNotifs = [...notifs].sort((a,b) => new Date(b.createdAt) - new Date(a.createdAt));

    container.innerHTML = sortedNotifs.map(notif => {
      const unreadClass = notif.read ? "" : "unread";
      return `
        <div class="notif-item ${unreadClass}" onclick="handleNotificationClick('${notif.id}', '${notif.songId}')">
          <div class="notif-item-icon">
            <i class="fa-solid fa-comment-dots"></i>
          </div>
          <div class="notif-item-content">
            <div>${escapeHTML(notif.message)}</div>
            <div class="notif-item-time">${formatRelativeTime(notif.createdAt)}</div>
          </div>
        </div>
      `;
    }).join("");
  }

  window.handleNotificationClick = function(notifId, songId) {
    // 1. Mark as read
    const notifs = DB.getNotifications();
    const notif = notifs.find(n => n.id === notifId);
    if (notif) {
      notif.read = true;
      DB.saveNotifications(notifs);
    }

    // 2. Hide dropdown
    document.getElementById("notification-dropdown").classList.remove("show");

    // 3. Navigate to song details page
    navigateTo(`#/song?id=${songId}`);
    showToast("해당 음악 상세 페이지로 이동합니다.");
  };

  // Hook notification clears
  const notifClearAllBtn = document.getElementById("notif-clear-all");
  if (notifClearAllBtn) {
    notifClearAllBtn.onclick = () => {
      const session = DB.getSession();
      if (!session) return;

      const notifs = DB.getNotifications();
      notifs.forEach(n => {
        if (n.targetUserId === session.id) {
          n.read = true;
        }
      });

      DB.saveNotifications(notifs);
      showToast("모든 알림을 확인 처리했습니다.");
      
      // Update UI
      updateNotificationsCounter();
      renderNotificationsDropdownList();
    };
  }

  // Notifications toggler trigger mapping
  const notifBtnIcon = document.getElementById("notif-btn-icon");
  if (notifBtnIcon) {
    notifBtnIcon.onclick = (e) => {
      e.stopPropagation();
      const dropdown = document.getElementById("notification-dropdown");
      const isShow = dropdown.classList.toggle("show");
      if (isShow) {
        renderNotificationsDropdownList();
      }
    };
  }

  // Close notifications if click outside
  document.addEventListener("click", (e) => {
    const dropdown = document.getElementById("notification-dropdown");
    if (dropdown && !dropdown.contains(e.target) && e.target !== notifBtnIcon) {
      dropdown.classList.remove("show");
    }
  });

  // --- User Profile Page Render ---
  function renderUserProfile() {
    const session = DB.getSession();
    if (!session) return;

    // Profile details card
    document.getElementById("profile-nickname").innerText = session.nickname;
    document.getElementById("profile-user-id").innerText = session.id;
    document.getElementById("profile-user-role").innerText = session.role === "admin" ? "최고관리자 👑" : "일반회원 🌸";
    
    // First letter avatar
    const firstLetter = session.nickname ? Array.from(session.nickname)[0] : session.id[0].toUpperCase();
    const avatarIcon = document.getElementById("profile-avatar-icon");
    avatarIcon.innerText = firstLetter;
    if (session.role === "admin") {
      avatarIcon.classList.add("admin-avatar");
    } else {
      avatarIcon.classList.remove("admin-avatar");
    }

    // Personal comments gathering
    const allComments = DB.getComments();
    const myComments = allComments.filter(c => c.userId === session.id);
    const songs = DB.getSongs();

    document.getElementById("profile-comments-count").innerText = myComments.length;
    const commentsList = document.getElementById("profile-comments-list-items");

    if (myComments.length === 0) {
      commentsList.innerHTML = `
        <div style="text-align: center; padding: 40px; color: var(--text-muted); font-size: 0.95rem;">
          <i class="fa-regular fa-comment-dots fa-2x" style="margin-bottom: 12px; color: var(--accent-pink);"></i>
          <p>작성한 댓글이 존재하지 않습니다. 곡 목록에서 다른 회원들과 대화를 나눠보세요!</p>
        </div>
      `;
    } else {
      // Sort newest comments first
      const sortedMyComments = [...myComments].sort((a,b) => new Date(b.createdAt) - new Date(a.createdAt));
      
      commentsList.innerHTML = sortedMyComments.map(comment => {
        const song = songs.find(s => s.id === comment.songId);
        const songTitle = song ? song.title : "삭제된 노래";
        const songArtist = song ? song.artist : "알수없음";

        return `
          <div class="my-comment-item" onclick="window.location.hash='#/song?id=${comment.songId}'">
            <div class="my-comment-song">
              <i class="fa-solid fa-music"></i> ${songArtist} - ${songTitle}
            </div>
            <div class="my-comment-text">${escapeHTML(comment.text)}</div>
            <div class="my-comment-time">${formatRelativeTime(comment.createdAt)}</div>
          </div>
        `;
      }).join("");
    }
  }

  // --- Admin Backoffice View Controls & Rendering ---
  function renderAdminDashboard() {
    const session = DB.getSession();
    if (!session || session.role !== "admin") return;

    const songs = DB.getSongs();
    const comments = DB.getComments();
    const users = DB.getUsers();

    // Fill metrics
    document.getElementById("admin-count-users").innerText = users.length;
    document.getElementById("admin-count-songs").innerText = songs.length;
    document.getElementById("admin-count-comments").innerText = comments.length;

    // Render respective panels depending on active tab
    renderAdminActiveTabPanel();
  }

  function renderAdminActiveTabPanel() {
    const users = DB.getUsers();
    const songs = DB.getSongs();
    const comments = DB.getComments();
    
    // Hide all sub-panels
    const panels = ["users-panel", "songs-panel", "comments-panel"];
    panels.forEach(p => {
      document.getElementById(`admin-panel-${p}`).classList.remove("active");
    });
    
    // Show active panel
    document.getElementById(`admin-panel-${activeAdminTab}`).classList.add("active");

    if (activeAdminTab === "users-panel") {
      // Render Users management table
      const body = document.getElementById("admin-table-users-body");
      body.innerHTML = users.map(user => {
        const deleteBtn = user.id === "admin" ? `
          <span style="font-size: 0.8rem; color: var(--text-muted); font-style: italic;">삭제 불가능</span>
        ` : `
          <button class="btn btn-danger btn-sm" onclick="adminDeleteUser('${user.id}')">탈퇴 시키기</button>
        `;

        return `
          <tr>
            <td><strong>${user.id}</strong></td>
            <td>${user.nickname || "-"}</td>
            <td><span class="tag" style="background-color: ${user.role === 'admin' ? 'var(--accent-pink-deep)' : 'var(--accent-pink-light)'}; color: ${user.role === 'admin' ? 'white' : 'var(--accent-pink-dark)'};">${user.role}</span></td>
            <td>${deleteBtn}</td>
          </tr>
        `;
      }).join("");
    } else if (activeAdminTab === "songs-panel") {
      // Render Songs management table
      const body = document.getElementById("admin-table-songs-body");
      body.innerHTML = songs.map(song => {
        let tagString = song.hashtags && song.hashtags.length > 0 
          ? song.hashtags.map(t => `#${t}`).join(", ") 
          : "없음";

        return `
          <tr>
            <td><code>${song.id}</code></td>
            <td><img src="https://img.youtube.com/vi/${song.youtubeId}/hqdefault.jpg" style="width: 60px; height: 34px; object-fit: cover; border-radius: 4px;" alt="커버"></td>
            <td><strong>${song.title}</strong></td>
            <td>${song.artist}</td>
            <td><div style="max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${tagString}">${tagString}</div></td>
            <td><span style="color: var(--heart-red);"><i class="fa-solid fa-heart"></i> ${song.likes.length}</span></td>
            <td>
              <button class="btn btn-danger btn-sm" onclick="adminDeleteSong('${song.id}')">곡 삭제</button>
            </td>
          </tr>
        `;
      }).join("");
    } else if (activeAdminTab === "comments-panel") {
      // Render Comments management table
      const body = document.getElementById("admin-table-comments-body");
      body.innerHTML = comments.map(comment => {
        const song = songs.find(s => s.id === comment.songId);
        const songTitle = song ? song.title : "삭제된 곡";

        return `
          <tr>
            <td><code>${comment.id}</code></td>
            <td>${songTitle}</td>
            <td><strong>${comment.userId}</strong></td>
            <td><div style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${escapeHTML(comment.text)}">${escapeHTML(comment.text)}</div></td>
            <td><span style="font-size: 0.8rem; color: var(--text-muted);">${new Date(comment.createdAt).toLocaleString()}</span></td>
            <td>
              <button class="btn btn-danger btn-sm" onclick="adminDeleteComment('${comment.id}')">삭제</button>
            </td>
          </tr>
        `;
      }).join("");
    }
  }

  // Admin delete actions hooks
  window.adminDeleteUser = function(userId) {
    if (userId === "admin") return;
    if (confirm(`정말로 아이디 '${userId}' 회원을 강제 탈퇴시키겠습니까?\n해당 유저가 쓴 글이나 정보가 더 이상 활성화되지 않습니다.`)) {
      let users = DB.getUsers();
      users = users.filter(u => u.id !== userId);
      DB.saveUsers(users);

      // Clean up session if they are deleted and currently active
      const session = DB.getSession();
      if (session && session.id === userId) {
        DB.saveSession(null);
      }

      showToast(`'${userId}' 회원을 탈퇴 처리했습니다.`);
      renderAdminDashboard();
    }
  };

  window.adminDeleteSong = function(songId) {
    if (confirm("정말로 해당 곡을 데이터베이스에서 삭제하시겠습니까?\n이 곡에 달린 모든 댓글과 좋아요 내역도 삭제됩니다.")) {
      // 1. Delete song
      let songs = DB.getSongs();
      songs = songs.filter(s => s.id !== songId);
      DB.saveSongs(songs);

      // 2. Delete linked comments
      let comments = DB.getComments();
      comments = comments.filter(c => c.songId !== songId);
      DB.saveComments(comments);

      // 3. Delete linked notifications
      let notifications = DB.getNotifications();
      notifications = notifications.filter(n => n.songId !== songId);
      DB.saveNotifications(notifications);

      showToast("곡 정보를 완전히 삭제 처리했습니다.");
      renderAdminDashboard();
    }
  };

  window.adminDeleteComment = function(commentId) {
    if (confirm("부적절한 댓글로 간주하여 완전히 강제 삭제 처리할까요?")) {
      let comments = DB.getComments();
      comments = comments.filter(c => c.id !== commentId);
      DB.saveComments(comments);

      showToast("댓글을 즉시 삭제했습니다.");
      renderAdminDashboard();
    }
  };

  // Register Admin panel tabs triggers click
  const adminTabItems = document.querySelectorAll(".admin-tab");
  adminTabItems.forEach(tab => {
    tab.onclick = () => {
      adminTabItems.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      
      activeAdminTab = tab.getAttribute("data-tab");
      renderAdminActiveTabPanel();
    };
  });

  // DB reset trigger
  const dbResetBtn = document.getElementById("admin-reset-db-btn");
  if (dbResetBtn) {
    dbResetBtn.onclick = () => {
      if (confirm("로컬 스토리지 내의 모든 데이터를 공장 초기 더미 데이터로 리셋할까요?\n진행 시 페이지가 리로드됩니다.")) {
        DB.resetToDefault();
        showToast("초기화 완료!");
      }
    };
  }

  // --- YouTube Import System Logic ---
  const fastImportBtn = document.getElementById("youtube-import-trigger");
  const fastImportBar = document.getElementById("fast-import-bar");
  const fastImportCancel = document.getElementById("youtube-import-cancel");
  const urlInput = document.getElementById("youtube-url-input");
  const extractBtn = document.getElementById("youtube-extract-btn");

  if (fastImportBtn && fastImportBar) {
    fastImportBtn.onclick = () => {
      const session = DB.getSession();
      if (!session) {
        showToast("음악을 추가하려면 먼저 로그인이 필요합니다.", "warning");
        openAuthModal("login");
        return;
      }
      fastImportBar.style.display = "block";
      urlInput.focus();
      // Scroll to import bar nicely
      fastImportBar.scrollIntoView({ behavior: "smooth", block: "center" });
    };

    fastImportCancel.onclick = () => {
      fastImportBar.style.display = "none";
      urlInput.value = "";
    };
  }

  // Extract ID trigger click
  if (extractBtn) {
    extractBtn.onclick = () => {
      const url = urlInput.value.trim();
      if (!url) {
        showToast("유튜브 동영상 링크 주소를 넣어주세요.", "warning");
        return;
      }

      const videoId = extractYouTubeVideoId(url);
      if (videoId) {
        // Open Detail Config Dialog modal
        openImportModal(videoId);
      } else {
        showToast("올바른 유튜브 링크 포맷이 아닙니다.\n주소를 확인하고 다시 입력해 주세요.", "error");
      }
    };
  }

  function extractYouTubeVideoId(url) {
    // Regex matching multiple youtube forms
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  // --- Modals Management System ---
  
  // A. Auth modal controls
  function openAuthModal(mode = "login") {
    const modal = document.getElementById("auth-modal");
    modal.classList.add("show");
    
    // Mode toggling
    toggleAuthModalMode(mode);
  }

  function closeAuthModal() {
    document.getElementById("auth-modal").classList.remove("show");
    // Clean inputs
    document.getElementById("login-id").value = "";
    document.getElementById("login-password").value = "";
    document.getElementById("signup-id").value = "";
    document.getElementById("signup-nickname").value = "";
    document.getElementById("signup-password").value = "";
    document.getElementById("signup-password-confirm").value = "";
  }

  function toggleAuthModalMode(mode) {
    const title = document.getElementById("auth-modal-title");
    const loginSec = document.getElementById("auth-login-section");
    const signupSec = document.getElementById("auth-signup-section");

    if (mode === "login") {
      title.innerText = "로그인";
      loginSec.style.display = "block";
      signupSec.style.display = "none";
    } else {
      title.innerText = "회원가입";
      loginSec.style.display = "none";
      signupSec.style.display = "block";
    }
  }

  // Trigger modal overlay close on backdrop click
  document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.onclick = (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("show");
      }
    };
  });

  // Modal triggers binding
  document.getElementById("header-login-btn").onclick = () => openAuthModal("login");
  document.getElementById("comment-login-trigger").onclick = () => openAuthModal("login");
  document.getElementById("auth-modal-close-btn").onclick = closeAuthModal;
  
  document.getElementById("switch-to-signup-btn").onclick = () => toggleAuthModalMode("signup");
  document.getElementById("switch-to-login-btn").onclick = () => toggleAuthModalMode("login");

  // Authentication Submission Logic
  document.getElementById("login-submit-btn").onclick = handleLoginSubmit;
  document.getElementById("signup-submit-btn").onclick = handleSignupSubmit;

  // Sign out mapping
  document.getElementById("header-logout-btn").onclick = () => {
    DB.saveSession(null);
    showToast("로그아웃 되었습니다. 좋은 하루 되세요! 🌸");
    
    // Redirect to home safely
    navigateTo("#/home");
    updateAuthLayout();
    
    if (currentView === "song-detail") {
      renderSongDetailPage(activeSongIdForComments);
    }
  };

  function handleLoginSubmit() {
    const id = document.getElementById("login-id").value.trim();
    const pass = document.getElementById("login-password").value.trim();

    if (!id || !pass) {
      showToast("아이디와 비밀번호를 모두 채워주세요.", "warning");
      return;
    }

    const users = DB.getUsers();
    const user = users.find(u => u.id === id && u.password === pass);

    if (user) {
      DB.saveSession(user);
      showToast(`${user.nickname}님, 반갑고 환영합니다! 🌸`);
      closeAuthModal();
      
      // Update Routing views
      handleRouting();
    } else {
      showToast("일치하는 계정 정보가 없습니다. 다시 시도해 주세요.", "error");
    }
  }

  function handleSignupSubmit() {
    const id = document.getElementById("signup-id").value.trim();
    const nickname = document.getElementById("signup-nickname").value.trim();
    const pass = document.getElementById("signup-password").value.trim();
    const passConfirm = document.getElementById("signup-password-confirm").value.trim();

    if (!id || !nickname || !pass || !passConfirm) {
      showToast("모든 항목을 올바르게 기입해 주세요.", "warning");
      return;
    }

    if (id.length < 3) {
      showToast("아이디는 최소 3자 이상이어야 합니다.", "warning");
      return;
    }

    if (pass.length < 4) {
      showToast("비밀번호는 최소 4자 이상이어야 합니다.", "warning");
      return;
    }

    if (pass !== passConfirm) {
      showToast("비밀번호 확인이 서로 일치하지 않습니다.", "error");
      return;
    }

    const users = DB.getUsers();
    
    // Duplicate check
    const idExists = users.some(u => u.id.toLowerCase() === id.toLowerCase());
    const nickExists = users.some(u => u.nickname.toLowerCase() === nickname.toLowerCase());

    if (idExists) {
      showToast("이미 존재하는 아이디입니다.", "error");
      return;
    }

    if (nickExists) {
      showToast("이미 등록된 별명/닉네임입니다.", "error");
      return;
    }

    // Save new user
    const newUser = {
      id: id,
      password: pass,
      nickname: nickname,
      role: "user"
    };

    users.push(newUser);
    DB.saveUsers(users);

    // Auto sign in user on success
    DB.saveSession(newUser);
    showToast("회원가입이 완료되었습니다! 반갑습니다. 🎉");
    closeAuthModal();
    
    handleRouting();
  }

  // B. Import YouTube details modal controls
  function openImportModal(videoId) {
    const modal = document.getElementById("import-details-modal");
    modal.classList.add("show");
    
    // Init values
    document.getElementById("import-youtube-id").value = videoId;
    document.getElementById("import-title").value = "";
    document.getElementById("import-artist").value = "";
    document.getElementById("import-description").value = "";
    document.getElementById("import-tags").value = "";
  }

  function closeImportModal() {
    document.getElementById("import-details-modal").classList.remove("show");
  }

  document.getElementById("import-modal-close-btn").onclick = closeImportModal;
  document.getElementById("import-cancel-btn").onclick = closeImportModal;

  document.getElementById("import-confirm-btn").onclick = () => {
    const videoId = document.getElementById("import-youtube-id").value;
    const title = document.getElementById("import-title").value.trim();
    const artist = document.getElementById("import-artist").value.trim();
    const desc = document.getElementById("import-description").value.trim();
    const rawTags = document.getElementById("import-tags").value.trim();

    if (!title || !artist) {
      showToast("제목과 가수는 필수 작성 항목입니다.", "warning");
      return;
    }

    // Process initial tags
    const hashtags = rawTags.split(/[\s,]+/).map(t => t.replace(/#/g, "").trim()).filter(t => t.length > 0);

    const songs = DB.getSongs();
    
    // Check duplicate video
    const videoExists = songs.some(s => s.youtubeId === videoId);
    if (videoExists) {
      showToast("이미 보관소에 등록되어 있는 유튜브 곡입니다.", "warning");
      closeImportModal();
      return;
    }

    const newSong = {
      id: `song_${Date.now()}`,
      title: title,
      artist: artist,
      youtubeId: videoId,
      description: desc || `${artist}의 인기 트랙입니다.`,
      hashtags: hashtags,
      likes: [],
      createdAt: new Date().toISOString()
    };

    songs.push(newSong);
    DB.saveSongs(songs);

    showToast(`'${title}' 음악이 정상적으로 등록되었습니다! 🌸`);
    
    // UI resets
    closeImportModal();
    fastImportBar.style.display = "none";
    urlInput.value = "";

    // Refresh active grid
    renderHomeMusicGrid();
  };

  // --- Miscellaneous Controls Listeners ---
  const searchInput = document.getElementById("music-search-input");
  if (searchInput) {
    searchInput.oninput = renderHomeMusicGrid;
  }

  const sortSelect = document.getElementById("music-sort-select");
  if (sortSelect) {
    sortSelect.onchange = renderHomeMusicGrid;
  }

  const clearTagFilterBtn = document.getElementById("clear-hashtag-filter-btn");
  if (clearTagFilterBtn) {
    clearTagFilterBtn.onclick = () => {
      activeHashtagFilter = null;
      navigateTo("#/home");
    };
  }

  const detailBackBtn = document.getElementById("detail-back-btn");
  if (detailBackBtn) {
    detailBackBtn.onclick = () => {
      // Go back to the previous view (Home)
      window.history.back();
    };
  }

  const logoBtn = document.getElementById("logo-btn");
  if (logoBtn) {
    logoBtn.onclick = () => navigateTo("#/home");
  }

  // Connect navigation item elements clicks to route mappings
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.onclick = () => {
      const view = item.getAttribute("data-view");
      navigateTo(`#/${view}`);
    };
  });

  // --- Utility Protection Helpers ---
  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag)
    );
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
  }

  // --- Initialization Trigger ---
  initRouter();
});
