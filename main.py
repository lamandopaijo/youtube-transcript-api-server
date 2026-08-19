from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        # 🔥 TAKTIK SAPU JAGAT: Daftar prioritas bahasa (Dari Indonesia sampai bahasa dunia)
        # Mesin akan mencoba dari kiri ke kanan. Jika 'id' gagal, coba 'en', dst.
        bahasa_prioritas = [
            'id', 'en', 'ms', 'ja', 'ko', 'zh-Hans', 'zh-Hant', 
            'hi', 'th', 'vi', 'ru', 'fr', 'de', 'es', 'pt', 
            'ar', 'tr', 'it', 'nl', 'pl', 'tl'
        ]
        
        # Sedot naskah langsung tanpa menggunakan list_transcripts yang error!
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=bahasa_prioritas)
        
        # Gabungkan teksnya menjadi satu paragraf panjang
        full_text = " ".join([item['text'] for item in transcript_data])
        
        return {"status": "success", "transcript": full_text}
        
    except Exception as e:
        # Error hanya akan muncul jika video SAMA SEKALI tidak punya subtitle dari 20 bahasa di atas
        raise HTTPException(status_code=400, detail=f"Gagal menarik naskah: {str(e)}")
