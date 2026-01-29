import cv2
from face_encoder import get_face_embedding
from matcher import load_embeddings, find_match

def recognize():
    known_embeddings = load_embeddings()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not available")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        embedding = get_face_embedding(frame)
        label = "Unknown"

        if embedding is not None and len(known_embeddings) > 0:
            name, dist = find_match(embedding, known_embeddings)
            if name is not None:
                label = name

        cv2.putText(
            frame,
            label,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize()