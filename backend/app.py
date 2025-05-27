from fastapi import FastAPI, UploadFile , Request , File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid,  shutil
from fastapi.responses import StreamingResponse
from pathlib import Path
import cv2
from ultralytics import YOLO
import cv2
from pathlib import Path
from ultralytics import YOLO
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    if VIDEO_DIR.exists():
        shutil.rmtree(VIDEO_DIR)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    print("Cleaned video folder at startup")
    
    yield 
    
    print("Server shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [] # Specify Later

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

VIDEO_DIR = Path("videos")

MODEL_PATH = PROJECT_ROOT / 'backend' / 'pretrained' / 'ArmyDroneDetectionLarge.pt'

model = YOLO(MODEL_PATH)


def compress_video_ffmpeg(input_path, output_path, crf=23, preset="medium"):
    ffmpeg_path = get_ffmpeg_exe()
    subprocess.run([
        ffmpeg_path, "-y", "-i", str(input_path),
        "-vcodec", "libx264", "-crf", str(crf), "-preset", preset,"-movflags", "faststart",
        str(output_path)
    ], check=True)
    

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    for file in VIDEO_DIR.glob("*"):
        try:
            file.unlink()
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print("Generating Video...")
    ext = video.filename.rsplit(".", 1)[-1] if "." in video.filename else "mp4"
    video_id = str(uuid.uuid4())
    filename = f"{video_id}.{ext}"
    input_path = VIDEO_DIR / filename

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    temp_output = VIDEO_DIR / f"{video_id}_annotated_raw.mp4"
    compressed_output = VIDEO_DIR / f"{video_id}_annotated.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.5, save=False, verbose=False)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
    
    compress_video_ffmpeg(temp_output, compressed_output)
    
    input_path.unlink(missing_ok=True)

    return {"videoUrl": compressed_output.name}

@app.get("/video/{filename}")
async def get_video(filename: str, request: Request):
    video_path = VIDEO_DIR / filename

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    file_size = video_path.stat().st_size
    headers = {}

    range_header = request.headers.get("range")
    if range_header:
        start = int(range_header.replace("bytes=", "").split("-")[0])
        end = min(start + 1024 * 1024, file_size - 1)
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        headers["Accept-Ranges"] = "bytes"
        headers["Content-Length"] = str(end - start + 1)
        status_code = 206
        file = open(video_path, "rb")
        file.seek(start)
        content = file.read(end - start + 1)
    else:
        headers["Content-Length"] = str(file_size)
        status_code = 200
        content = open(video_path, "rb").read()

    return StreamingResponse(
        iter([content]),
        media_type="video/mp4",
        headers=headers,
        status_code=status_code,
    )

