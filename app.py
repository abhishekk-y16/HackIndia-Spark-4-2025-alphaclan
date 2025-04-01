import cv2
import dlib
import numpy as np
import mediapipe as mp
import os
import time
from deepface import DeepFace
from flask import Flask, request, jsonify, render_template

# Create a folder to store reference faces
FACES_DB = "faces_db"
os.makedirs(FACES_DB, exist_ok=True)

# Face Detection
detector = dlib.get_frontal_face_detector()
def detect_faces(image_path, save_folder=FACES_DB):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    detected_faces = []
    for i, face in enumerate(faces):
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        face_img = img[y:y+h, x:x+w]
        face_filename = os.path.join(save_folder, f"face_{i}.jpg")
        cv2.imwrite(face_filename, face_img)
        detected_faces.append(face_filename)
    return detected_faces

# Face Recognition
def verify_identity(live_face, reference_faces):
    best_match = None
    best_distance = float("inf")
    for ref_face in reference_faces:
        try:
            result = DeepFace.verify(live_face, ref_face, model_name='Facenet')
            if result['verified'] and result['distance'] < best_distance:
                best_match = ref_face
                best_distance = result['distance']
                print(f"Match Found: {best_match}, Distance: {best_distance:.2f}")
        except Exception as e:
            print(f"Error comparing {live_face} with {ref_face}: {str(e)}")
    
    if best_match:
        print("Final Match Verified!")
    else:
        print("No Match Found.")
    
    return best_match, best_distance

# Flask API & Frontend Setup
app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files['image']
    if not file:
        return jsonify({"error": "No file uploaded"})
    
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    stored_faces = [os.path.join(FACES_DB, f) for f in os.listdir(FACES_DB)]
    best_match, distance = verify_identity(file_path, stored_faces)
    
    return jsonify({"verified": bool(best_match), "distance": distance})

if __name__ == '__main__':
    app.run(debug=False)

