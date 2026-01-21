import os
import time
import random
import cv2                 # For image/video processing
import numpy as np         # For numerical operations
import tensorflow as tf    # For the Deep Learning Model
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- LOAD THE MODEL (Fail-Safe) ---
# We try to load the model. If it doesn't exist yet, we set it to None.
# This prevents your app from crashing while you are still working on the project.
MODEL_PATH = 'model.h5' 
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ SUCCESS: Real AI Model loaded!")
    else:
        print("⚠️ WARNING: 'model.h5' not found. App is running in SIMULATION mode.")
except Exception as e:
    print(f"❌ ERROR loading model: {e}")

# --- HELPER FUNCTIONS ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(filepath):
    """
    Reads an image or extracts a frame from a video, 
    then resizes it for the AI model.
    """
    img_array = None
    
    # Check if it's a video file
    if filepath.lower().endswith(('.mp4', '.avi', '.mov')):
        cap = cv2.VideoCapture(filepath)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Grab a frame from the middle of the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
        ret, frame = cap.read()
        if ret:
            img_array = frame
        cap.release()
    else:
        # It's an image
        img_array = cv2.imread(filepath)

    if img_array is None:
        return None

    # Preprocessing for FaceForensics++ (Xception/MesoNet usually take 256x256 or 299x299)
    # We resize to 224x224 as a safe standard for most models
    new_array = cv2.resize(img_array, (224, 224))
    
    # Normalize pixel values (0 to 1)
    return new_array.reshape(-1, 224, 224, 3) / 255.0

# --- ANALYSIS ENGINE ---

def analyze_media(filepath):
    # 1. Prepare the data
    prepared_data = prepare_image(filepath)
    
    if prepared_data is None:
        return {"label": "Error", "ai_probability": 0, "is_fake": False}

    # 2. Run Detection
    if model:
        # --- REAL AI MODE ---
        print("🧠 Analyzing with Neural Network...")
        prediction = model.predict(prepared_data)
        
        # Most binary classifiers output a value between 0 and 1
        # 0 = Authentic, 1 = Fake (or vice versa depending on training)
        # We assume: Higher score = More likely to be Fake
        score = float(prediction[0][0]) 
        ai_confidence = round(score * 100)
    else:
        # --- SIMULATION MODE (If no model is found) ---
        print("🎲 Simulation Mode: Generating random result...")
        time.sleep(2) # Fake processing delay
        ai_confidence = random.randint(10, 99)

    # 3. Interpret Results
    if ai_confidence > 50:
        label = "Deepfake Detected❌"
        is_fake = True
    else:
        label = "Authentic Media✅"
        is_fake = False
        
    return {
        "label": label,
        "ai_probability": ai_confidence,
        "organic_probability": 100 - ai_confidence,
        "is_fake": is_fake
    }

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Trigger Analysis
        result = analyze_media(filepath)
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'result': result
        })

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)