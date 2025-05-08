import requests
from flask import Flask, redirect
import re

app = Flask(__name__)

def get_current_atv_m3u8():
    # ATV canlı yayın sayfasını çek
    url = "https://www.atv.com.tr/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # Sayfadan M3U8 linkini regex ile bul
    m3u8_pattern = r'https?://[^"\s]+\.m3u8(?:\?[^"\s]+)?'
    match = re.search(m3u8_pattern, response.text)
    
    if match:
        return match.group(0)
    else:
        return None

@app.route('/atv.m3u8')
def serve_m3u8():
    current_m3u8 = get_current_atv_m3u8()
    if current_m3u8:
        return redirect(current_m3u8, code=302)
    else:
        return "M3U8 bulunamadı", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
