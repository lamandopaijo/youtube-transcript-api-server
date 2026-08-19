from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        # Ambil daftar semua subtitle yang ada di video tersebut
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Ambil bahasa APA SAJA yang pertama kali ditemukan (bebas bahasa apapun)
        transcript = next(iter(transcript_list))
        
        # Sedot teksnya dan gabungkan
        full_text = " ".join([item['text'] for item in transcript.fetch()])
        
        return {"status": "success", "transcript": full_text}
        
    except Exception as e:
        # Jika benar-benar gagal (misal video tidak ada suaranya sama sekali)
        raise HTTPException(status_code=400, detail=f"Gagal menarik naskah: {str(e)}")
