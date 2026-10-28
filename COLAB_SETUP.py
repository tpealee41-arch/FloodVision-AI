# Run this in a NEW Google Colab cell after connecting Google Drive.
# It starts an API that uses your trained FloodVision U-Net model.
# For access from your local website, expose port 8000 using a tunnel.
# Keep the tunnel URL private; anyone with it may be able to submit images.

from google.colab import drive
drive.mount('/content/drive')

!pip -q install fastapi "uvicorn[standard]" python-multipart pyngrok

import os, subprocess, time
from pathlib import Path

MODEL_PATH = "/content/drive/MyDrive/Machine learning/FloodVision_AI/FloodVision_UNet_BCEDice_best.keras"
assert Path(MODEL_PATH).exists(), f"Model file not found: {MODEL_PATH}"

# Upload/copy backend/app.py to /content/floodvision_backend_app.py first,
# or paste the backend/app.py content into a Colab file named /content/floodvision_backend_app.py.
# Then run:
# os.environ["MODEL_PATH"] = MODEL_PATH
# subprocess.Popen(["uvicorn", "floodvision_backend_app:app", "--host", "0.0.0.0", "--port", "8000"])
#
# To expose the port:
# from pyngrok import ngrok
# from getpass import getpass
# ngrok.set_auth_token(getpass("Paste your ngrok authtoken: "))
# public_url = ngrok.connect(8000, "http").public_url
# print("API health:", public_url + "/health")
# print("Put this in the website API field:", public_url + "/predict")
#
# Security note: stop the tunnel when finished; do not publish your token.
