import numpy as np
import os

DATA_DIR = "data/registered_faces"
THRESHOLD = 10.0

def load_embeddings():
    data = {}
    if not os.path.exists(DATA_DIR):
        return data

    for file in os.listdir(DATA_DIR):
        if file.endswith(".npy"):
            name = file.replace(".npy", "")
            data[name] = np.load(os.path.join(DATA_DIR, file))
    return data

def find_match(embedding, known_embeddings):
    min_dist = float("inf")
    identity = None

    for name, known_emb in known_embeddings.items():
        dist = np.linalg.norm(embedding - known_emb)
        if dist < min_dist:
            min_dist = dist
            identity = name

    if min_dist < THRESHOLD:
        return identity, min_dist
    return None, min_dist