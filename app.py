import requests
from flask import Flask, redirect, jsonify
import re
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # Logları aç

def get_current_atv_m3u8():
    url = "https://www.atv.com.tr/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.atv.com.tr/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP hatalarını yakala
        app.logger.info(f"ATV sayfası çekildi (Status: {response.status_code})")
        
        # Güncel M3U8 linkini bul
        m3u8_pattern = r'(https?://[^"\s]+\.m3u8(?:\?[^"\s]+)?)'
        matches = re.findall(m3u8_pattern, response.text)
        
        if matches:
            app.logger.info(f"Bulunan M3U8 linkleri: {matches}")
            return matches[0]  # İlk eşleşen linki döndür
        else:
            app.logger.error("M3U8 linki bulunamadı!")
            return None
    except Exception as e:
        app.logger.error(f"Hata: {str(e)}")
        return None

@app.route('/atv.m3u8')
def serve_m3u8():
    current_m3u8 = get_current_atv_m3u8()
    if current_m3u8:
        app.logger.info(f"Yönlendiriliyor: {current_m3u8}")
        return redirect(current_m3u8, code=302)
    else:
        return jsonify({"error": "M3U8 linki alınamadı"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug modu açık
