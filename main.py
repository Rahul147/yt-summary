import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI()

def stream_captions(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        transcript_data = transcript.fetch()
        def generate():
            for entry in transcript_data:
                start = entry['start']
                duration = entry['duration']
                text = entry['text'].replace('\n', ' ')
                yield f"{start} --> {start + duration}\n{text}\n\n".encode('utf-8')
        return generate
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        return None

@app.get("/download_captions/")
async def get_captions(youtube_url: str):
    video_id = YouTube(youtube_url).video_id
    caption_stream = stream_captions(video_id)
    if caption_stream:
        return StreamingResponse(caption_stream(), media_type="text/plain")
    else:
        raise HTTPException(status_code=404, detail="Captions not found")

# The following is only needed if this script is run directly, e.g., not by Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

