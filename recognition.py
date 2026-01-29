import cv2
import numpy as np
import os
from face_encoder import get_face_embedding

DATA_DIR = "data/registered_faces"

def register_user(name):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not available")
        return

    embeddings = []

    while len(embeddings) < 10:
        ret, frame = cap.read()
        if not ret:
            break

        embedding = get_face_embedding(frame)
        if embedding is not None:
            embeddings.append(embedding)

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(embeddings) == 0:
        print("No face captured")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    avg_embedding = np.mean(embeddings, axis=0)
    np.save(f"{DATA_DIR}/{name}.npy", avg_embedding)
    print("Saved")

if __name__ == "__main__":
    username = input("Enter username: ")
    register_user(username)