import os
import shutil
import uuid
import sys

# Add parent folder to Python path to access analysis/ outside app/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from analysis.pose_analyzer import process_video_with_pose  # external folder

app = FastAPI(title="Dance Movement Analysis")

# Upload directory
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use mp4/mov/avi/mkv/webm.")

    # Create session directory
    session_id = str(uuid.uuid4())
    workdir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(workdir, exist_ok=True)

    input_path = os.path.join(workdir, "input" + os.path.splitext(file.filename)[1])
    output_path = os.path.join(workdir, "output.mp4")
    landmarks_json = os.path.join(workdir, "landmarks.json")

    # Save uploaded file
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Process video
        frame_count, fps = process_video_with_pose(input_path, output_path, landmarks_json)
    except Exception as e:
        shutil.rmtree(workdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    # Return video as downloadable file
    return FileResponse(output_path, media_type="video/mp4", filename="analysis_result.mp4")
