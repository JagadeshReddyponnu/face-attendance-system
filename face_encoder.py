import cv2
import numpy as np
from deepface import DeepFace

def get_face_embedding(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = DeepFace.represent(
        img_path=rgb,
        model_name="Facenet",
        enforce_detection=False
    )
    return np.array(result[0]["embedding"])