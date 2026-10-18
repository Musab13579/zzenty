import json
from datetime import datetime
import urllib.request

# Kick kanal kullanıcı adın
CHANNEL_NAME = "r7-zenty"

# Varsayılan değerler
is_live = False
stream_title = "Yayın Kapalı"
category = "Belirtilmedi"
last_vod_title = "Henüz Geçmiş Yayın Yok"
last_vod_url = f"https://kick.com/{CHANNEL_NAME}"
last_vod_date = "-"

# Kick VOD & Kanal Bilgilerini Çekme
try:
  req = urllib.request.Request(
      f"https://kick.com/api/v1/channels/{CHANNEL_NAME}",
      headers={"User-Agent": "Mozilla/5.0"},
  )
  with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

    # Canlı yayın durumu
    if data.get("livestream"):
      is_live = True
      stream_title = data["livestream"].get("session_title", "Canlı Yayın")
      category = data["livestream"].get("categories", [{}])[0].get("name", "Oyun")

    # Son yayın videosu (VOD) bilgisi
    previous_stream = data.get("previous_livestreams", [])
    if previous_stream:
      last_stream = previous_stream[0]
      last_vod_title = last_stream.get("session_title", "Son Yayın")
      last_vod_date = last_stream.get("created_at", "")[
          :10
      ]  # YYYY-MM-DD formatı
      # Video ID varsa doğrudan video URL'si oluşturur
      vod_id = last_stream.get("id")
      if vod_id:
        last_vod_url = (
            f"https://kick.com/{CHANNEL_NAME}?video={last_stream.get('slug')}"
        )
except Exception as e:
  print(f"Kick verisi çekilirken hata oluştu: {e}")

# Durum rozeti
status_badge = (
    '<span style="background-color: #53fc18; color: #000; padding: 4px 10px;'
    ' border-radius: 6px; font-weight: bold;">🔴 CANLI YAYINDA</span>'
    if is_live
    else '<span style="background-color: #444; color: #fff; padding: 4px 10px;'
    ' border-radius: 6px;">YAYIN KAPALI</span>'
)

now = datetime.now().strftime("%d.%m.%Y %H:%M")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>zentyy - Kick Yayın İstatistikleri</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #0b0e0f; color: #ffffff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; }}
        header {{ text-align: center; margin-top: 20px; margin-bottom: 30px; }}
        h1 {{ color: #53fc18; font-size: 2.5rem; margin-bottom: 10px; }}
        p.subtitle {{ color: #a0a0a0; font-size: 1.1rem; }}
        .container {{ width: 100%; max-width: 800px; display: flex; flex-direction: column; gap: 20px; }}
        .card {{ background: #191c1e; border: 1px solid #2a2e33; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        .card h2 {{ color: #53fc18; font-size: 1.4rem; margin-bottom: 12px; border-bottom: 1px solid #2a2e33; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }}
        .kick-btn {{ display: inline-block; background-color: #53fc18; color: #000000; font-weight: bold; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 15px; }}
        .info-row {{ margin-bottom: 10px; font-size: 1.05rem; }}
        footer {{ margin-top: auto; padding: 20px; color: #666; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <header>
        <h1>zentyy</h1>
        <p class="subtitle">Kick Yayınlarım ve Son Geçmiş Yayın Bilgileri</p>
    </header>
    <div class="container">
        <!-- Canlı Yayın Durum Kartı -->
        <div class="card">
            <h2>Kanal Durumu {status_badge}</h2>
            <div class="info-row"><strong>Yayın Başlığı:</strong> {stream_title}</div>
            <div class="info-row"><strong>Kategori:</strong> {category}</div>
            <a href="https://kick.com/{CHANNEL_NAME}" target="_blank" class="kick-btn">Kick Kanalıma Git</a>
        </div>

        <!-- Son Yayın / VOD Kartı -->
        <div class="card">
            <h2>🎬 Son Yayın İstatistiği & Kaydı</h2>
            <div class="info-row"><strong>Son Yayın Adı:</strong> {last_vod_title}</div>
            <div class="info-row"><strong>Tarih:</strong> {last_vod_date}</div>
            <p style="margin-top: 10px;">Yayın kaydını izlemek için aşağıdaki butona tıklayabilirsin:</p>
            <a href="{last_vod_url}" target="_blank" class="kick-btn" style="background-color: #2a2e33; color: #fff;">Son Yayını İzle</a>
        </div>
    </div>
    <footer>
        <p>Son Otomatik Güncelleme: {now} | &copy; zentyy</p>
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
  f.write(html_content)

print("Kick verileri başarıyla çekildi ve index.html güncellendi!")
