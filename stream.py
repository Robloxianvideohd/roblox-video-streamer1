import os
import cv2
import base64
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow Roblox to fetch frames

# Load your video
VIDEO_PATH = "video.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)

# Frame size for Roblox SurfaceGui (32x32 pixels)
WIDTH, HEIGHT = 32, 32

def get_frame():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
        ret, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    # Encode frame as PNG and then base64
    _, buffer = cv2.imencode('.png', frame)
    frame_b64 = base64.b64encode(buffer).decode('utf-8')
    return frame_b64

@app.route("/frame")
def frame():
    data = get_frame()
    return Response(data, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides the port
    app.run(host="0.0.0.0", port=port)
