import json
from datetime import datetime
import urllib.request

# Kick kanal kullanıcı adın
CHANNEL_NAME = "r7-zenty"

is_live = False
stream_title = "Yayın Kapalı"
category = "Belirtilmedi"
viewer_count = 0
vods_html = ""

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

        vods_html += f"""
                <div class="vod-card">
                    {f'<img src="{vod_thumbnail}" alt="VOD">' if vod_thumbnail else ''}
                    <div class="vod-info">
                        <h3>{vod_title}</h3>
                        <p><strong>Tarih:</strong> {vod_date}</p>
                        <a href="https://kick.com/{CHANNEL_NAME}?video={vod_slug}" target="_blank" class="vod-btn">Yayını İzle</a>
                    </div>
                </div>
                """
    else:
      vods_html = "<p style='color: #888;'>Henüz geçmiş yayın bulunmuyor.</p>"

except Exception as e:
  print(f"Hata: {e}")
  vods_html = "<p style='color: #ff5555;'>Arşiv yüklenirken hata oluştu.</p>"

status_badge = (
    f'<span style="background-color: #53fc18; color: #000; padding: 4px 10px;'
    f' border-radius: 6px; font-weight: bold;">🔴 CANLI ({viewer_count}'
    ' İzleyici)</span>'
    if is_live
    else '<span style="background-color: #333; color: #fff; padding: 4px 10px;'
    ' border-radius: 6px; font-weight: bold;">YAYIN KAPALI</span>'
)

# Oynatıcı Alanı
player_html = f"""
<iframe src="https://player.kick.com/{CHANNEL_NAME}?muted=false" height="480" width="100%" frameborder="0" scrolling="no" allowfullscreen="true"></iframe>
"""

now = datetime.now().strftime("%d.%m.%Y %H:%M")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>zentyy - Canlı Yayın & Arşiv</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #0b0e0f; color: #ffffff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; }}
        header {{ text-align: center; margin-top: 10px; margin-bottom: 20px; }}
        h1 {{ color: #53fc18; font-size: 2.5rem; margin-bottom: 5px; }}
        p.subtitle {{ color: #a0a0a0; font-size: 1.1rem; }}
        .container {{ width: 100%; max-width: 1000px; display: flex; flex-direction: column; gap: 20px; }}
        .card {{ background: #191c1e; border: 1px solid #2a2e33; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        .card h2 {{ color: #53fc18; font-size: 1.3rem; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2e33; padding-bottom: 8px; }}
        
        .player-box {{ width: 100%; border-radius: 8px; overflow: hidden; background: #000; }}
        
        .action-buttons {{ display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap; }}
        .kick-btn {{ flex: 1; display: inline-block; background-color: #53fc18; color: #000000; font-weight: bold; padding: 12px; border-radius: 8px; text-decoration: none; text-align: center; transition: 0.2s; }}
        .kick-btn:hover {{ background-color: #42cb12; }}
        .chat-btn {{ flex: 1; display: inline-block; background-color: #2a2e33; color: #ffffff; font-weight: bold; padding: 12px; border-radius: 8px; text-decoration: none; text-align: center; transition: 0.2s; }}
        .chat-btn:hover {{ background-color: #383e46; }}

        .vod-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
        .vod-card {{ background: #141719; border: 1px solid #2a2e33; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }}
        .vod-card img {{ width: 100%; height: 140px; object-fit: cover; background: #000; }}
        .vod-info {{ padding: 12px; display: flex; flex-direction: column; flex-grow: 1; }}
        .vod-info h3 {{ font-size: 1rem; color: #fff; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        .vod-info p {{ font-size: 0.85rem; color: #aaa; margin-bottom: 10px; }}
        .vod-btn {{ margin-top: auto; background-color: #2a2e33; color: #fff; text-align: center; padding: 8px; border-radius: 6px; text-decoration: none; font-size: 0.9rem; font-weight: bold; transition: 0.2s; }}
        .vod-btn:hover {{ background-color: #53fc18; color: #000; }}

        .info-row {{ margin-bottom: 6px; font-size: 1.05rem; color: #ccc; }}
        footer {{ margin-top: auto; padding: 20px; color: #666; font-size: 0.9rem; text-align: center; }}
    </style>
</head>
<body>
    <header>
        <h1>zentyy</h1>
        <p class="subtitle">Canlı Yayın Oynatıcısı ve Video Arşivi</p>
    </header>
    
    <div class="container">
        <!-- Canlı Yayın Kartı -->
        <div class="card">
            <h2>Canlı Yayın Oynatıcısı {status_badge}</h2>
            <div class="player-box">
                {player_html}
            </div>
            <div style="margin-top: 15px;" class="info-row"><strong>Anlık Başlık:</strong> {stream_title}</div>
            <div class="info-row"><strong>Kategori:</strong> {category}</div>
            
            <div class="action-buttons">
                <a href="https://kick.com/{CHANNEL_NAME}" target="_blank" class="kick-btn">Kick'te Takip Et</a>
                <a href="https://kick.com/{CHANNEL_NAME}/chatroom" target="_blank" class="chat-btn">💬 Sohbet Penceresini Aç & Mesaj Yaz</a>
            </div>
        </div>

        <!-- Geçmiş Yayınlar / VOD Arşivi -->
        <div class="card">
            <h2>🎬 Geçmiş Yayınlar ve Arşiv (VODs)</h2>
            <div class="vod-grid">
                {vods_html}
            </div>
        </div>
    </div>

    <footer>
        <p>Otomatik Güncelleme: {now} | &copy; zentyy</p>
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
  f.write(html_content)

print("Güncelleme başarıyla tamamlandı!")
