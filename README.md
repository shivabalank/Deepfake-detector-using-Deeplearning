# Deepfake-detector-using-Deeplearning
A full-stack Deep Learning application designed to identify and visualize AI-generated facial manipulations in images and videos. This project was developed as a forensic tool to combat digital misinformation using the FaceForensics++ dataset standards.

2. PROJECT OVERVIEW:
With the rise of sophisticated AI, deepfakes have become nearly indistinguishable from reality. This project provides a user-friendly interface to upload media and receive an instant forensic analysis report. The backend utilizes a Convolutional Neural Network (CNN) to detect pixel-level artifacts and compression anomalies characteristic of AI-generated content.

3. KEY FEATURES:
A) Hybrid Detection: Supports both static images (.jpg, .png) and video files (.mp4, .avi).
B) Video Frame Sampling: Automatically extracts and analyzes keyframes from uploaded videos for consistent forensic checking.
C) Real-time Visualization: Features a dynamic Donut Chart visualization to show the probability split between "AI Component" and "Organic Content."
D)Interactive UI: A modern, glassmorphic interface with a seamless 3-stage workflow: Upload -> Analyze -> Report.
E)FaceForensics++ Integration: Based on the research benchmarks of the FF++ dataset, targeting manipulations like FaceSwap and Face2Face

4. TECH STACK:
A)Frontend: HTML5, CSS3 (Custom Animations), JavaScript, Chart.js.
B)Backend: Python, Flask.
C)AI/Machine Learning: TensorFlow/Keras, NumPy.
D)Computer Vision: OpenCV (for frame extraction and image preprocessing).

5. HOW IT WORKS:
A)Preprocessing: The system uses OpenCV to resize media to $224 \times 224$ pixels and normalizes pixel values to a range of $[0, 1]
B)Inference: The processed data is fed into a trained XceptionNet model.
C)Scoring: The model outputs a sigmoid probability score. If the score $P > 0.5$, the media is flagged as a Deepfake
D)Reporting: The results are sent via a JSON API to the frontend and displayed as an interactive percentage chart.

6. HOW TO EXEQUTE IN VS CODE:
A) After importing this file, Open terminal in VS Code
B) Write this command "cd DeepfakeDetector" can click enter.
C) then import the python liberaries by writing these commands "pip install flask tensorflow opencv-python numpy pandas scikit-learn".
D) Now run the code by this command "python app.py"
E) And finally, Open http://127.0.0.1:5000 in your browser. 
