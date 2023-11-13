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


def download_captions_with_youtube_transcript_api(video_id, output_path):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        transcript_data = transcript.fetch()
        with open(output_path, 'w', encoding='utf-8') as file:
            for entry in transcript_data:
                start = entry['start']
                duration = entry['duration']
                text = entry['text'].replace('\n', ' ')
                file.write(f"{start} --> {start + duration}\n{text}\n\n")
        print(f"Auto-generated English captions downloaded successfully to {output_path}")
        return True
    except (TranscriptsDisabled, NoTranscriptFound):
        print("Auto-generated captions not available with youtube-transcript-api.")
        return False
    except Exception as e:
        print(f"An error occurred with youtube-transcript-api: {e}")
        return False

def download_captions_with_pytube(url, output_path):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url)
        captions = yt.captions
        if 'a.en' in captions:
            # Generate the SRT (SubRip text file format) of the caption
            srt_caption = captions['a.en'].generate_srt_captions()
            # Save the SRT caption to a file
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(srt_caption)
            print(f"Auto-generated English captions downloaded successfully to {output_path} with pytube")
            return True
        else:
            print("Auto-generated English captions not found with pytube.")
            return False
    except Exception as e:
        print(f"An error occurred with pytube: {e}")
        return False

def download_captions(video_id, url, output_path):
    if not download_captions_with_youtube_transcript_api(video_id, output_path):
        download_captions_with_pytube(url, output_path)

def main():
    # Read the URL from the YOUTUBE_URL environment variable
    youtube_url = os.getenv('YOUTUBE_URL')

    # Set the output path for the captions
    output_path = os.getenv('CAPTION_PATH', '/data/captions.srt')

    if youtube_url:
        video_id = YouTube(youtube_url).video_id
        print(f"Downloading captions for: {youtube_url}")
        download_captions(video_id, youtube_url, output_path)
    else:
        print("No YouTube URL provided. Set the YOUTUBE_URL environment variable.")
"""
if __name__ == "__main__":
    main()
"""
