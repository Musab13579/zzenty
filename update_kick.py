import json
from datetime import datetime
import urllib.request

# Kick kanal kullanıcı adın
CHANNEL_NAME = "r7-zenty"

is_live = False
stream_title = "Yayın Kapalı"
category = "Belirtilmedi"
viewer_count = 0
vods_data_list = []

# Kick API'sinden Verileri Çekme
try:
  req = urllib.request.Request(
      f"https://kick.com/api/v1/channels/{CHANNEL_NAME}",
      headers={"User-Agent": "Mozilla/5.0"},
  )
  with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

    # Canlı yayın kontrolü
    if data.get("livestream"):
      is_live = True
      livestream_data = data["livestream"]
      stream_title = livestream_data.get("session_title", "Canlı Yayın")
      category = livestream_data.get("categories", [{}])[0].get("name", "Oyun")
      viewer_count = livestream_data.get("viewer_count", 0)

    # Geçmiş Yayınlar (VOD) Listesi
    previous_streams = data.get("previous_livestreams", [])
    if previous_streams:
      for vod in previous_streams:
        vod_title = vod.get("session_title", "Kayıtsız Yayın")
        vod_date = vod.get("created_at", "")[:10]
        vod_slug = vod.get("slug", "")
        vod_thumbnail = (
            vod.get("thumbnail", {}).get("url", "")
            if vod.get("thumbnail")
            else ""
        )
        vods_data_list.append({
            "title": vod_title,
            "date": vod_date,
            "slug": vod_slug,
            "thumbnail": vod_thumbnail,
        })
except Exception as e:
  print(f"Hata: {e}")

status_badge = (
    f'<span style="background-color: #53fc18; color: #000; padding: 4px 10px;'
    f' border-radius: 6px; font-weight: bold;">🔴 CANLI ({viewer_count}'
    ' İzleyici)</span>'
    if is_live
    else '<span style="background-color: #333; color: #fff; padding: 4px 10px;'
    ' border-radius: 6px; font-weight: bold;">YAYIN KAPALI</span>'
)

# İlk açılışta oynatıcıda ne olacağı (Canlıysa canlı, değilse son VOD veya kanal)
default_embed_src = f"https://player.kick.com/{CHANNEL_NAME}?muted=false"
if not is_live and vods_data_list:
  # Eğer canlı değilse en son VOD'u oynatıcıya verelim
  default_embed_src = (
      f"https://player.kick.com/video/{vods_data_list[0]['slug']}?muted=false"
  )

# VOD kartlarını oluştur (Tıklandığında sayfadan gitmeyip üstteki oynatıcıda açılmasını sağlayan sihirli JavaScript fonksiyonu ile)
vods_html = ""
if vods_data_list:
  for vod in vods_data_list:
    vod_slug = vod["slug"]
    vod_title = vod["title"]
    vod_date = vod["date"]
    vod_thumbnail = vod["thumbnail"]

    vods_html += f"""
        <div class="vod-card" onclick="playVod('https://player.kick.com/video/{vod_slug}?muted=false', '{vod_title.replace("'", "\\'")}')">
            {f'<img src="{vod_thumbnail}" alt="VOD">' if vod_thumbnail else ''}
            <div class="vod-info">
                <h3>{vod_title}</h3>
                <p><strong>Tarih:</strong> {vod_date}</p>
                <span class="vod-btn">Sitede İzle 🎬</span>
            </div>
        </div>
        """
else:
  vods_html = "<p style='color: #888;'>Henüz geçmiş yayın bulunmuyor.</p>"

now = datetime.now().strftime("%d.%m.%Y %H:%M")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>zentyy - Canlı Yayın & Video Arşivi</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #0b0e0f; color: #ffffff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; }}
        header {{ text-align: center; margin-top: 10px; margin-bottom: 20px; }}
        h1 {{ color: #53fc18; font-size: 2.5rem; margin-bottom: 5px; }}
        p.subtitle {{ color: #a0a0a0; font-size: 1.1rem; }}
        .container {{ width: 100%; max-width: 1100px; display: flex; flex-direction: column; gap: 20px; }}
        .card {{ background: #191c1e; border: 1px solid #2a2e33; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        .card h2 {{ color: #53fc18; font-size: 1.3rem; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2e33; padding-bottom: 8px; }}
        
        /* Yayın ve Sohbet Düzeni */
        .main-grid {{ display: flex; gap: 20px; flex-wrap: wrap; }}
        .player-section {{ flex: 2; min-width: 320px; display: flex; flex-direction: column; gap: 12px; }}
        .player-box {{ width: 100%; height: 450px; border-radius: 8px; overflow: hidden; background: #000; }}
        .player-box iframe {{ width: 100%; height: 100%; border: none; }}
        
        /* Özel Sitede Yorum / Sohbet Alanı */
        .chat-section {{ flex: 1; min-width: 280px; background: #141719; border: 1px solid #2a2e33; border-radius: 8px; display: flex; flex-direction: column; height: 520px; }}
        .chat-header {{ background: #1f2327; padding: 12px; font-weight: bold; color: #53fc18; border-bottom: 1px solid #2a2e33; }}
        .chat-messages {{ flex: 1; padding: 12px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }}
        .chat-msg {{ background: #1f2327; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; border-left: 3px solid #53fc18; }}
        .chat-msg .user {{ font-weight: bold; color: #53fc18; margin-bottom: 2px; font-size: 0.8rem; }}
        .chat-input-area {{ padding: 10px; border-top: 1px solid #2a2e33; display: flex; gap: 8px; }}
        .chat-input-area input {{ flex: 1; background: #0b0e0f; border: 1px solid #2a2e33; border-radius: 6px; padding: 8px; color: #fff; outline: none; }}
        .chat-input-area button {{ background: #53fc18; color: #000; border: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
        .chat-input-area button:hover {{ background: #42cb12; }}

        /* VOD / Arşiv Izgarası */
        .vod-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 15px; }}
        .vod-card {{ background: #141719; border: 1px solid #2a2e33; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; cursor: pointer; transition: 0.2s; }}
        .vod-card:hover {{ border-color: #53fc18; transform: translateY(-3px); }}
        .vod-card img {{ width: 100%; height: 130px; object-fit: cover; background: #000; }}
        .vod-info {{ padding: 12px; display: flex; flex-direction: column; flex-grow: 1; }}
        .vod-info h3 {{ font-size: 0.95rem; color: #fff; margin-bottom: 6px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        .vod-info p {{ font-size: 0.8rem; color: #aaa; margin-bottom: 10px; }}
        .vod-btn {{ margin-top: auto; background-color: #2a2e33; color: #53fc18; text-align: center; padding: 6px; border-radius: 6px; font-size: 0.85rem; font-weight: bold; }}

        .info-row {{ font-size: 1rem; color: #ccc; }}
        footer {{ margin-top: auto; padding: 20px; color: #666; font-size: 0.9rem; text-align: center; }}
    </style>
</head>
<body>
    <header>
        <h1>zentyy</h1>
        <p class="subtitle">Canlı Yayın, Site İçi Arşiv ve Özel Sohbet Paneli</p>
    </header>
    
    <div class="container">
        <!-- Oynatıcı ve Sohbet Alanı -->
        <div class="card">
            <h2>Yayın Oynatıcısı & Sohbet {status_badge}</h2>
            <div class="main-grid">
                <!-- Sol Taraf: Video Oynatıcı -->
                <div class="player-section">
                    <div class="player-box">
                        <iframe id="videoPlayer" src="{default_embed_src}" allowfullscreen="true"></iframe>
                    </div>
                    <div class="info-row"><strong>Oynatılan:</strong> <span id="currentPlayingTitle">{stream_title}</span></div>
                    <div class="info-row"><strong>Kategori:</strong> {category}</div>
                </div>

                <!-- Sağ Taraf: Sitede Görünen Özel Sohbet/Yorum Kutusu -->
                <div class="chat-section">
                    <div class="chat-header">💬 Zentyy Canlı Sohbet</div>
                    <div class="chat-messages" id="chatMessages">
                        <div class="chat-msg">
                            <div class="user">Sistem Botu</div>
                            Zentyy platformuna hoş geldin! Sohbetten mesaj yazabilirsin.
                        </div>
                    </div>
                    <div class="chat-input-area">
                        <input type="text" id="chatInput" placeholder="Mesaj yaz..." onkeypress="handleKeyPress(event)">
                        <button onclick="sendMessage()">Gönder</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Geçmiş Yayınlar / VOD Arşivi -->
        <div class="card">
            <h2>🎬 Geçmiş Yayınlar (İzlemek için tıklayın, yukarıda oynasın)</h2>
            <div class="vod-grid">
                {vods_html}
            </div>
        </div>
    </div>

    <footer>
        <p>Otomatik Güncelleme: {now} | &copy; zentyy</p>
    </footer>

    <script>
        // VOD'a tıklandığında sayfadan gitmeden yukarıdaki oynatıcıda oynatır
        function playVod(url, title) {{
            document.getElementById('videoPlayer').src = url;
            document.getElementById('currentPlayingTitle').innerText = title;
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Sitedeki özel sohbet fonksiyonu
        function sendMessage() {{
            const input = document.getElementById('chatInput');
            const messagesContainer = document.getElementById('chatMessages');
            const text = input.value.trim();
            
            if(text !== "") {{
                const msgDiv = document.createElement('div');
                msgDiv.className = 'chat-msg';
                msgDiv.innerHTML = `<div class="user">İzleyici</div>${{escapeHtml(text)}}`;
                messagesContainer.appendChild(msgDiv);
                input.value = "";
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }}
        }}

        function handleKeyPress(event) {{
            if(event.key === 'Enter') {{
                sendMessage();
            }}
        }}

        function escapeHtml(text) {{
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
  f.write(html_content)

print("Gelişmiş site içi oynatıcı ve özel sohbet sistemi kuruldu!")
