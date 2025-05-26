import cv2
from pathlib import Path
from ultralytics import YOLO
import os
import shutil

# 📁 Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMP_DIR = PROJECT_ROOT / 'backend' / 'videos' / 'temp'
OUTPUT_DIR = PROJECT_ROOT / 'backend' / 'videos' / 'processed'
PUBLIC_URL_PREFIX = "/videos/processed"

# 🧠 Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 🧠 Load YOLO model
MODEL_PATH = PROJECT_ROOT / 'backend' / 'pretrained' / 'ArmyDroneDetectionLarge.pt'
model = YOLO(MODEL_PATH)

def predict_video(input_path):
    print("🔍 Start Predicting...")
    cap = cv2.VideoCapture(input_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    stem = Path(input_path).stem
    temp_output = OUTPUT_DIR / f"{stem}_annotated_temp.mp4"
    final_output = OUTPUT_DIR / f"{stem}_annotated.mp4"
    public_url = f"{PUBLIC_URL_PREFIX}/{final_output.name}"

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.5, save=False, verbose=False)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Move to final public location
    shutil.move(temp_output, final_output)

    # Clean up original upload
    if os.path.exists(input_path):
        os.remove(input_path)

    print("✅ Prediction done. Output saved to:", final_output)
    return public_url
