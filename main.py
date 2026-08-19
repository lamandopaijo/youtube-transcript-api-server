from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/api/transcript")
def get_transcript(video_id: str):
    try:
        # Menyedot naskah secara otomatis dari YouTube
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['id', 'en'])
        
        # Menggabungkan potongan teks menjadi satu paragraf utuh
        full_text = " ".join([item['text'] for item in transcript_list])
        return {"status": "success", "transcript": full_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))