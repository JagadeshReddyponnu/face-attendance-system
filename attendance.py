import cv2
from datetime import datetime
from deepface import DeepFace
from face_encoder import get_face_embedding
from matcher import load_embeddings, find_match
from database import init_db, mark_attendance, last_entry, last_entry_today
from spoof_check import HeadMovementDetector

MIN_GAP_SECONDS = 60

def run():
    init_db()
    known_embeddings = load_embeddings()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        return

    spoof = HeadMovementDetector()
    current_name = None
    display_text = "Move Naturally"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = DeepFace.extract_faces(
            img_path=frame,
            enforce_detection=False
        )

        live = False

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
                        if (now - last_time).total_seconds() < MIN_GAP_SECONDS:
                            allow = False

                    if allow and current_name != name:
                        if today_last is None:
                            entry_type = "IN"
                        else:
                            entry_type = "OUT" if today_last == "IN" else "IN"

                        mark_attendance(name, entry_type)
                        display_text = f"{name} | {entry_type}"
                        current_name = name
        else:
            display_text = "Move Naturally"

        cv2.putText(
            frame,
            display_text,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0) if live else (0, 0, 255),
            2
        )

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()