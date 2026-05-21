/**
 * Music Vibe - LocalStorage Database Store
 */

const DEFAULT_USERS = [
  { id: "user1", password: "passwword1", nickname: "VibeMaster 🎵", role: "user" },
  { id: "user2", password: "password2", nickname: "MelodyQueen 🌸", role: "user" },
  { id: "admin", password: "passwordad", nickname: "Admin Pink 👑", role: "admin" }
];

const DEFAULT_SONGS = [
  {
    id: "song_1",
    title: "Dynamite",
    artist: "BTS (방탄소년단)",
    youtubeId: "gdZLi9oWNZg",
    description: "방탄소년단의 경쾌한 디스코 팝 장르의 곡으로, 전 세계에 활력과 희망의 메시지를 전합니다. 듣는 순간 몸이 들썩이는 신나는 리듬!",
    hashtags: ["Kpop", "BTS", "Disco", "Dance", "Happy"],
    likes: ["user2"], // Liked by user2
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString() // 5 days ago
  },
  {
    id: "song_2",
    title: "Hype Boy",
    artist: "NewJeans (뉴진스)",
    youtubeId: "11cta61wi0g",
    description: "뉴진스만의 독특하고 청량한 감성이 가득 담긴 메가 히트곡! 트렌디하면서도 중독성 강한 신스 비트와 보컬 멜로디가 일품입니다.",
    hashtags: ["NewJeans", "Kpop", "Fresh", "Trendy", "Dance"],
    likes: ["user1", "user2"], // Liked by user1, user2
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3).toISOString() // 3 days ago
  },
  {
    id: "song_3",
    title: "Blank Space",
    artist: "Taylor Swift",
    youtubeId: "e-ORhEE9VVg",
    description: "테일러 스위프트의 대표적인 신스팝 명곡. 매력적인 풍자와 스토리가 돋보이는 멜로디라인으로 전 세계 팬들의 귀를 사로잡은 히트작입니다.",
    hashtags: ["Pop", "TaylorSwift", "USA", "Retro"],
    likes: ["user1"],
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10).toISOString() // 10 days ago
  },
  {
    id: "song_4",
    title: "Bad Guy",
    artist: "Billie Eilish",
    youtubeId: "DyDfgMOUjCI",
    description: "빌리 아일리시의 매력적이고 미니멀한 일렉트로팝 베이스 사운드. 위트 있으면서도 몽환적인 음색이 리스너를 매혹시킵니다.",
    hashtags: ["Pop", "DarkPop", "Chilly", "BillieEilish"],
    likes: [],
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 12).toISOString()
  },
  {
    id: "song_5",
    title: "Uptown Funk (ft. Bruno Mars)",
    artist: "Mark Ronson",
    youtubeId: "OPf0YbXqDm0",
    description: "레트로 펑크와 디스코의 환상적인 조합! 마크 론슨의 세련된 프로듀싱과 브루노 마스의 폭발적인 에너지가 담긴 댄스 넘버입니다.",
    hashtags: ["Funk", "Retro", "BrunoMars", "Dance", "Energy"],
    likes: ["user1", "user2"],
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 15).toISOString()
  },
  {
    id: "song_6",
    title: "lofi hip hop radio - beats to relax/study to",
    artist: "Lofi Girl",
    youtubeId: "jfKfPfyJRdk",
    description: "공부할 때, 일할 때, 혹은 조용히 휴식을 취할 때 듣기 가장 좋은 24시간 실시간 음악 채널의 대표적인 Lofi 비트 음악 모음집.",
    hashtags: ["Lofi", "Study", "Relax", "Chill", "Calm"],
    likes: ["user2"],
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 20).toISOString()
  }
];

const DEFAULT_COMMENTS = [
  {
    id: "comment_1",
    songId: "song_1", // Dynamite
    userId: "user2",
    text: "이 노래는 진짜 우울할 때 들으면 바로 기분이 100% 핑크빛으로 풀려요! 💖🌸 역시 방탄!",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString() // 48 hours ago
  },
  {
    id: "comment_2",
    songId: "song_2", // Hype Boy
    userId: "user1",
    text: "Hype Boy 너만 원해!! 댄스 챌린지 따라 하다가 발목 삘 뻔했지만 너무 신납니다 👍👍 @MelodyQueen 🌸 님도 춤 춰보셨나요?",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString() // 24 hours ago
  },
  {
    id: "comment_3",
    songId: "song_2", // Hype Boy
    userId: "user2",
    text: "@VibeMaster 🎵 앗 저는 매일 방에서 혼자 춘답니다 크크 💃 너무 신나요!",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 20).toISOString() // 20 hours ago
  },
  {
    id: "comment_4",
    songId: "song_5", // Uptown Funk
    userId: "user1",
    text: "Uptown Funk you up! 브루노 마스 내한공연 때의 떼창이 생각나네요. 펑크 감성 최고!!",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString() // 12 hours ago
  }
];

const DEFAULT_NOTIFICATIONS = [
  {
    id: "notif_1",
    targetUserId: "user1",
    triggerUserId: "user2",
    songId: "song_2", // Hype Boy
    type: "new_comment",
    message: "MelodyQueen 🌸님이 회원님이 좋아요 한 'Hype Boy'에 댓글을 남겼습니다.",
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 20).toISOString()
  }
];

// Initialize localStorage databases if not present
function initDatabase() {
  if (!localStorage.getItem("vibe_users")) {
    localStorage.setItem("vibe_users", JSON.stringify(DEFAULT_USERS));
  }
  if (!localStorage.getItem("vibe_songs")) {
    localStorage.setItem("vibe_songs", JSON.stringify(DEFAULT_SONGS));
  }
  if (!localStorage.getItem("vibe_comments")) {
    localStorage.setItem("vibe_comments", JSON.stringify(DEFAULT_COMMENTS));
  }
  if (!localStorage.getItem("vibe_notifications")) {
    localStorage.setItem("vibe_notifications", JSON.stringify(DEFAULT_NOTIFICATIONS));
  }
  
  // Set current user session as null initially if not set
  if (!localStorage.getItem("vibe_session")) {
    localStorage.setItem("vibe_session", JSON.stringify(null));
  }
}

// Global DB access helper
const DB = {
  getUsers: () => JSON.parse(localStorage.getItem("vibe_users") || "[]"),
  saveUsers: (users) => localStorage.setItem("vibe_users", JSON.stringify(users)),

  getSongs: () => JSON.parse(localStorage.getItem("vibe_songs") || "[]"),
  saveSongs: (songs) => localStorage.setItem("vibe_songs", JSON.stringify(songs)),

  getComments: () => JSON.parse(localStorage.getItem("vibe_comments") || "[]"),
  saveComments: (comments) => localStorage.setItem("vibe_comments", JSON.stringify(comments)),

  getNotifications: () => JSON.parse(localStorage.getItem("vibe_notifications") || "[]"),
  saveNotifications: (notifs) => localStorage.setItem("vibe_notifications", JSON.stringify(notifs)),

  getSession: () => JSON.parse(localStorage.getItem("vibe_session") || "null"),
  saveSession: (user) => localStorage.setItem("vibe_session", JSON.stringify(user)),

  resetToDefault: () => {
    localStorage.setItem("vibe_users", JSON.stringify(DEFAULT_USERS));
    localStorage.setItem("vibe_songs", JSON.stringify(DEFAULT_SONGS));
    localStorage.setItem("vibe_comments", JSON.stringify(DEFAULT_COMMENTS));
    localStorage.setItem("vibe_notifications", JSON.stringify(DEFAULT_NOTIFICATIONS));
    localStorage.setItem("vibe_session", JSON.stringify(null));
    window.location.reload();
  }
};

// Initialize on load
initDatabase();
