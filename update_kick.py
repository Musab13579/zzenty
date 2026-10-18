from datetime import datetime

# HTML dosyamızı güncelleyen Python betiği
# Bu betik, Kick istatistiklerini (şimdilik örnek olarak güncel saat/tarih ve örnek verilerle) siteye işler.

now = datetime.now().strftime("%d.%m.%Y %H:%M")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zzenty - Kick Yayınları & İstatistikler</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        body {{
            background-color: #0b0e0f;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        header {{
            text-align: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #53fc18;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        p.subtitle {{
            color: #a0a0a0;
            font-size: 1.1rem;
        }}
        .container {{
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .card {{
            background: #191c1e;
            border: 1px solid #2a2e33;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }}
        .card h2 {{
            color: #53fc18;
            font-size: 1.4rem;
            margin-bottom: 12px;
            border-bottom: 1px solid #2a2e33;
            padding-bottom: 8px;
        }}
        .kick-btn {{
            display: inline-block;
            background-color: #53fc18;
            color: #000000;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            margin-top: 15px;
            transition: 0.2s;
        }}
        .kick-btn:hover {{
            background-color: #43ca13;
        }}
        footer {{
            margin-top: auto;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>

    <header>
        <h1>Zzenty</h1>
        <p class="subtitle">Kick Yayınlarım ve Son Video İstatistikleri</p>
    </header>

    <div class="container">
        <div class="card">
            <h2>Canlı Yayın & Kanal</h2>
            <p>Kick üzerindeki yayınlarımı ve son videolarımı buradan takip edebilirsin.</p>
            <a href="https://kick.com/zzenty" target="_blank" class="kick-btn">Kick Kanalıma Git</a>
        </div>

        <div class="card">
            <h2>Son Yayın Bilgileri</h2>
            <div id="stats">
                <p><strong>Son Oyun:</strong> Valorant / Just Chatting</p>
                <p><strong>Son Güncelleme:</strong> {now}</p>
                <p><strong>Durum:</strong> Python Otomasyonu Aktif 🚀</p>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Zzenty - Tüm hakları saklıdır.</p>
    </footer>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
  f.write(html_content)

print("index.html başarıyla güncellendi!")
