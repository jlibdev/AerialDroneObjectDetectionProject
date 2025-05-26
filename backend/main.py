from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil, os, uuid, cv2
import utils

app = FastAPI()

# 1️⃣ Enable CORS so your React dev server can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow any origin
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2️⃣ Videos folder & static mount
VIDEO_DIR = "videos/temp"
PROCESSED_DIR = "videos/processed"
os.makedirs(VIDEO_DIR, exist_ok=True)
app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    filename = video.filename or "video.mp4"
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "mp4"
    video_id = str(uuid.uuid4())
    filename = f"{video_id}.{ext}"
    filepath = os.path.join(VIDEO_DIR, filename)
    

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
        
    pred_path = utils.predict_video(filepath)
    
    print(f"/videos/{filename}")
    print(pred_path)

    return {"videoUrl": pred_path}
