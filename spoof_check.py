import numpy as np
from collections import deque

WINDOW = 10
MOVEMENT_THRESHOLD = 35

class HeadMovementDetector:
    def __init__(self):
        self.centers = deque(maxlen=WINDOW)

    def is_live(self, box):
        x, y, w, h = box
        center = np.array([x + w // 2, y + h // 2])
        self.centers.append(center)

        if len(self.centers) < WINDOW:
            return False

        movement = 0
        for i in range(1, len(self.centers)):
            movement += np.linalg.norm(self.centers[i] - self.centers[i - 1])

        return movement > MOVEMENT_THRESHOLD