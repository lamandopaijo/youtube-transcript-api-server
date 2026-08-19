from fastapi import FastAPI, HTTPException
import requests
import re
import html as html_lib

app = FastAPI()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        # 1. Menyamar sebagai Browser Google Chrome dari PC
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        # Buka halaman YouTube
        resp = requests.get(url, headers=headers)
        html = resp.text
        
        # 2. Taktik Sniper: Cari link rahasia API Subtitle di dalam tumpukan kode YouTube
        match = re.search(r'"baseUrl":"(https://www\.youtube\.com/api/timedtext[^"]+)"', html)
        if not match:
            raise Exception("Video ini tidak memiliki Subtitle/CC sama sekali.")
            
        # 3. Bersihkan Link (YouTube sering mengunci simbol & menjadi \u0026)
        raw_url = match.group(1)
        clean_url = raw_url.replace("\\u0026", "&").replace("\\/", "/")
        
        # 4. Buka brankas XML naskahnya
        xml_resp = requests.get(clean_url)
        xml_data = xml_resp.text
        
        # 5. Sedot semua teks di antara tag <text> ... </text>
        teks_kotor = re.findall(r'>([^<]+)</text>', xml_data)
        
        # 6. Bersihkan simbol HTML aneh (seperti &amp; atau &#39;)
        teks_bersih = [html_lib.unescape(t) for t in teks_kotor]
        
        # Gabungkan menjadi satu naskah panjang
        full_text = " ".join(teks_bersih)
        
        if not full_text.strip():
            raise Exception("Naskah kosong.")
            
        return {"status": "success", "transcript": full_text}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal menarik naskah: {str(e)}")
