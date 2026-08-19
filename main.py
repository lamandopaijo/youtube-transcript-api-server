from fastapi import FastAPI
import requests
import re
import html

app = FastAPI()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        resp = requests.get(url, headers=headers)
        html_text = resp.text
        
        match = re.search(r'"baseUrl":"(https://www\.youtube\.com/api/timedtext[^"]+)"', html_text)
        if not match:
            # 👉 PERUBAHAN: Kembalikan status 200 OK biasa, Android tidak akan panik!
            return {"status": "error", "transcript": "Video ini tidak memiliki Subtitle/CC sama sekali."}
            
        raw_url = match.group(1)
        clean_url = raw_url.replace("\\u0026", "&").replace("\\/", "/")
        
        xml_resp = requests.get(clean_url)
        teks_kotor = re.findall(r'>([^<]+)</text>', xml_resp.text)
        
        # Bersihkan simbol aneh
        teks_bersih = [html.unescape(t) for t in teks_kotor]
        full_text = " ".join(teks_bersih)
        
        if not full_text.strip():
            return {"status": "error", "transcript": "Naskah kosong."}
            
        return {"status": "success", "transcript": full_text}
        
    except Exception as e:
        # 👉 Jangan gunakan raise HTTPException lagi, cukup kembalikan teks
        return {"status": "error", "transcript": f"Error: {str(e)}"}
