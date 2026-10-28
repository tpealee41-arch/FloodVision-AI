import os
import io
import base64
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Override MODEL_PATH with an environment variable when needed.
# Load model from the backend folder
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    str(Path(__file__).resolve().parent / "FloodVision_UNet_BCEDice_best.keras"),
)
IMG_SIZE = 256
THRESHOLD = float(os.environ.get("FLOOD_THRESHOLD", "0.5"))

app = FastAPI(title="FloodVision AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your website origin.
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    path = Path(MODEL_PATH)
    if not path.exists():
        print(f"WARNING: model file not found at {path}. /health will report unavailable.")
        return
    # Notebook cell 12 loads this saved model with compile=False.
    model = tf.keras.models.load_model(str(path), compile=False)
    print("Loaded model:", path)
    print("Input:", model.input_shape, "Output:", model.output_shape)

@app.get("/")
def root():
    return {
        "service": "FloodVision AI API",
        "docs": "/docs",
        "health": "/health",
        "predict": "POST /predict (multipart field: file)",
    }

@app.get("/health")
def health():
    return {
        "status": "ok" if model is not None else "model_unavailable",
        "model_path": MODEL_PATH,
        "input_size": [IMG_SIZE, IMG_SIZE, 3],
        "threshold": THRESHOLD,
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Check MODEL_PATH and ensure the .keras file exists.",
        )
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    raw = await file.read()
    try:
        image = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file is not a readable image.")

    original_width, original_height = image.size
    # Matches the notebook preprocessing: RGB, 256x256, bilinear, float32 / 255.
    resized = image.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.BILINEAR)
    x = np.asarray(resized, dtype=np.float32) / 255.0
    x = np.expand_dims(x, axis=0)

    probabilities = model.predict(x, verbose=0)
    probs = np.asarray(probabilities)[0]
    if probs.ndim == 3 and probs.shape[-1] == 1:
        probs = probs[..., 0]
    if probs.ndim != 2:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected model output shape: {np.asarray(probabilities).shape}",
        )

    binary_mask = (probs >= THRESHOLD).astype(np.uint8)
    flood_percent = float(binary_mask.mean() * 100.0)

    # White = predicted flood; black = predicted non-flood. Resize to original dimensions.
    mask_image = Image.fromarray(binary_mask * 255, mode="L")
    mask_image = mask_image.resize(
        (original_width, original_height), Image.Resampling.NEAREST
    )
    buf = io.BytesIO()
    mask_image.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    mask_data_url = "data:image/png;base64," + encoded

    return {
        "mask": mask_data_url,
        "flood_percent": round(flood_percent, 2),
        "threshold": THRESHOLD,
        "input_width": original_width,
        "input_height": original_height,
        "model_input_size": [IMG_SIZE, IMG_SIZE],
        "summary": f"ตรวจพบพิกเซลที่โมเดลจัดเป็นพื้นที่น้ำท่วมประมาณ {flood_percent:.2f}% ของภาพ (threshold {THRESHOLD:.2f}; เป็นสัดส่วนพิกเซล ไม่ใช่พื้นที่จริงทางภูมิศาสตร์)",
    }
