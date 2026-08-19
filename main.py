from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

# 👉 PERUBAHAN KRUSIAL: Kita harus membuat/menginisialisasi objek "mesin" utamanya dulu di versi terbaru ini
yt_api = YouTubeTranscriptApi()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        # Gunakan mesin yt_api yang sudah diinisialisasi
        transcript_list = yt_api.list_transcripts(video_id)
        
        # Ambil bahasa APA SAJA yang pertama kali ditemukan di video tersebut
        transcript = next(iter(transcript_list))
        
        # Sedot teksnya dan gabungkan menjadi satu kalimat utuh
        full_text = " ".join([item['text'] for item in transcript.fetch()])
        
        return {"status": "success", "transcript": full_text}
        
    except Exception as e:
        # Jika benar-benar gagal (misal video tak ada suaranya)
        raise HTTPException(status_code=400, detail=f"Gagal menarik naskah: {str(e)}")
