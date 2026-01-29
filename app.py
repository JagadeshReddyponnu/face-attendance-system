from fastapi import FastAPI
import cv2
from datetime import datetime
from deepface import DeepFace
from face_encoder import get_face_embedding
from matcher import load_embeddings, find_match
from database import init_db, mark_attendance, last_entry, last_entry_today
from spoof_check import HeadMovementDetector

app = FastAPI()
init_db()
known_embeddings = load_embeddings()
spoof = HeadMovementDetector()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/attendance")
def mark():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return {"error": "camera not available"}

    current_name = None
    result = "not verified"

    for _ in range(60):
        ret, frame = cap.read()
        if not ret:
            break

        detections = DeepFace.extract_faces(
            img_path=frame,
            enforce_detection=False
        )

        if detections:
            region = detections[0]["facial_area"]
            box = (region["x"], region["y"], region["w"], region["h"])
            live = spoof.is_live(box)

            if live:
                embedding = get_face_embedding(frame)
                if embedding is not None:
                    name, dist = find_match(embedding, known_embeddings)
                    if name is not None:
                        last = last_entry(name)
                        today_last = last_entry_today(name)
                        now = datetime.now()

                        allow = True
                        if last:
                            last_time = datetime.fromisoformat(last[0])
                            if (now - last_time).total_seconds() < 60:
                                allow = False

                        if allow:
                            if today_last is None:
                                entry_type = "IN"
                            else:
                                entry_type = "OUT" if today_last == "IN" else "IN"

                            mark_attendance(name, entry_type)
                            result = f"{name} {entry_type}"
                            break

    cap.release()
    return {"result": result}