# FloodVision AI — connected web + inference API

This project is based on `flood.ipynb`. The notebook defines a TensorFlow/Keras U-Net with:
- Input: RGB image, 256×256
- Preprocessing: resize with bilinear interpolation, float32 / 255
- Output: one sigmoid channel (binary flood probability)
- Threshold: 0.5
- Model path used by the notebook: `Machine learning/FloodVision_AI/FloodVision_UNet_BCEDice_best.keras`

## Project structure
- `index.html`: web frontend
- `backend/app.py`: FastAPI inference API
- `backend/requirements.txt`: Python packages
- `backend/COLAB_SETUP.py`: starter notes for running the API from Colab

## Important: model file
The notebook contains code to train/load the model, but the `.keras` weights file itself was not included with the uploaded notebook. Run the relevant notebook cells so this file exists in your Google Drive:
`/content/drive/MyDrive/Machine learning/FloodVision_AI/FloodVision_UNet_BCEDice_best.keras`

The API loads that exact path by default. If you host the API elsewhere, set the environment variable `MODEL_PATH` to the actual path of the `.keras` file. The custom BCE+Dice loss is not needed for inference because the API loads with `compile=False`.

## Run the API on a machine that has the model file
```bash
cd backend
pip install -r requirements.txt
# Set MODEL_PATH if it is not at the default location
uvicorn app:app --host 0.0.0.0 --port 8000
```
Test `http://localhost:8000/health`; then open the website and enter:
`http://localhost:8000/predict`
If the frontend and API are not on the same origin, configure CORS appropriately for production.

## Use Colab as a temporary backend
1. Open Colab and mount Drive.
2. Ensure the model file above exists.
3. Copy `backend/app.py` into a Colab file at `/content/app.py` (or upload the `backend` folder).
4. Install dependencies:
   `!pip -q install fastapi "uvicorn[standard]" python-multipart`
5. Start the API in a cell:
   ```python
   import os
   os.environ["MODEL_PATH"] = "/content/drive/MyDrive/Machine learning/FloodVision_AI/FloodVision_UNet_BCEDice_best.keras"
   !uvicorn app:app --host 0.0.0.0 --port 8000
   ```
6. To let a website outside Colab access it, expose port 8000 using a secure tunnel such as ngrok (requires an account/token). Then enter the tunnel URL plus `/predict` in the website.

Colab runtimes are temporary; the URL changes and API stops when the runtime disconnects. For a stable deployment, host the API on a server that can run TensorFlow and access the model file.

## API contract
`POST /predict`, multipart form field `file` (image).
Example response:
```json
{
  "mask": "data:image/png;base64,...",
  "flood_percent": 12.34,
  "threshold": 0.5,
  "input_width": 1920,
  "input_height": 1080,
  "model_input_size": [256, 256],
  "summary": "..."
}
```
`GET /health` reports whether the model loaded.

## Interpretation notes
- This is binary segmentation: white = model predicts flooded; black = model predicts non-flooded.
- `flood_percent` is the proportion of predicted pixels in the resized model output, not a geospatial flood-area measurement.
- This model does not separately classify buildings, roads, or water categories.
- The API returns a binary mask resized to the input image's dimensions for display. Inference itself runs at 256×256.
