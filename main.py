from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import yt_dlp
import os
import uuid
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Universal Downloader")

# Create directories
os.makedirs("downloads", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Templates
templates = Jinja2Templates(directory="templates")

# Supported platforms
SUPPORTED_PLATFORMS = {
    "youtube": "YouTube",
    "facebook": "Facebook", 
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "twitter": "X (Twitter)",
    "vimeo": "Vimeo",
    "dailymotion": "Dailymotion"
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "platforms": SUPPORTED_PLATFORMS
    })

@app.post("/download")
async def download_video(
    url: str = Form(...),
    format_type: str = Form(...)
):
    """
    Download video/audio from supported platforms
    """
    try:
        # Generate unique filename
        download_id = str(uuid.uuid4())
        
        # Configure yt-dlp options based on format
        if format_type == "mp4":
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'downloads/{download_id}.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
        else:  # mp3
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': f'downloads/{download_id}.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
        
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        download_dir = Path("downloads")
        files = list(download_dir.glob(f"{download_id}.*"))
        
        if not files:
            raise HTTPException(status_code=500, detail="Download failed - file not found")
        
        downloaded_file = files[0]
        
        # Convert to MP3 if requested (fallback if yt-dlp didn't convert)
        if format_type == "mp3" and downloaded_file.suffix.lower() != '.mp3':
            try:
                # Try to rename the file to .mp3 if it's already an audio format
                if downloaded_file.suffix.lower() in ['.webm', '.m4a', '.aac', '.ogg']:
                    mp3_file = downloaded_file.with_suffix('.mp3')
                    downloaded_file.rename(mp3_file)
                    downloaded_file = mp3_file
                    logger.info(f"Renamed {downloaded_file} to MP3 format")
                else:
                    # Try pydub conversion
                    from pydub import AudioSegment
                    logger.info(f"Converting {downloaded_file} to MP3")
                    
                    # Load the audio file
                    audio = AudioSegment.from_file(str(downloaded_file))
                    
                    # Create MP3 filename
                    mp3_file = downloaded_file.with_suffix('.mp3')
                    
                    # Export as MP3
                    audio.export(str(mp3_file), format="mp3", bitrate="192k")
                    
                    # Remove original file and use MP3
                    downloaded_file.unlink()
                    downloaded_file = mp3_file
                    
                    logger.info(f"Successfully converted to MP3: {mp3_file}")
                
            except Exception as e:
                logger.warning(f"MP3 conversion failed: {e}")
                # Just rename the file to .mp3
                try:
                    mp3_file = downloaded_file.with_suffix('.mp3')
                    downloaded_file.rename(mp3_file)
                    downloaded_file = mp3_file
                    logger.info(f"Renamed to MP3 format: {mp3_file}")
                except Exception as e2:
                    logger.warning(f"Could not rename to MP3: {e2}, returning original file")
        
        # Return the file
        return FileResponse(
            path=str(downloaded_file),
            filename=f"download_{download_id}.{downloaded_file.suffix[1:]}",
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "platforms": list(SUPPORTED_PLATFORMS.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)